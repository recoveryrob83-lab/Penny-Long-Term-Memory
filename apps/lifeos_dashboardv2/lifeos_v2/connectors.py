"""Small, read-only Overview adapters.  They never issue provider mutations."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


def stamp() -> str:
    return datetime.now(UTC).isoformat()


def iso(value: str | None) -> str:
    if not value:
        return ""
    return value.replace("Z", "+00:00")


@dataclass
class NormalizedRecord:
    source_system: str; source_id: str; source_container_id: str = ""; source_container_name: str = ""
    title: str = ""; summary: str = ""; state: str = ""; due_at: str = ""; start_at: str = ""
    updated_at: str = ""; source_url: str = ""; fetched_at: str = ""; source_error: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]: return asdict(self)


@dataclass
class RefreshResult:
    source_system: str; status: str; fetched_at: str; last_success_at: str | None; records: list[dict[str, Any]]
    error: str | None = None; recovery_hint: str = ""; cached: bool = False
    def to_dict(self) -> dict[str, Any]: return asdict(self)


class Connector:
    name = "connector"; credentials: tuple[str, ...] = ()
    def __init__(self, config: dict[str, Any], transport=None): self.config, self.transport, self.last_success = config, transport or self._get, None
    def configured(self) -> bool: return all(os.getenv(key) for key in self.credentials)
    def health(self) -> dict[str, str]: return {"status": "configured" if self.configured() else "configuration_required"}
    def get_last_success(self) -> str | None: return self.last_success
    def describe_error(self, error: Exception) -> tuple[str, str]:
        if isinstance(error, urllib.error.HTTPError):
            if error.code in (401, 403): return "authentication_required", "Check the read-only credential and source permissions."
            if error.code == 429: return "rate_limited", "Wait for the provider limit, then refresh again."
        return "unavailable", "Check network access and the configured source."
    def _get(self, url: str, headers: dict[str, str] | None = None) -> Any:
        request = urllib.request.Request(url, headers=headers or {}, method="GET")
        with urllib.request.urlopen(request, timeout=12) as response: return json.loads(response.read().decode("utf-8"))
    def refresh(self) -> RefreshResult: raise NotImplementedError


class TodoistConnector(Connector):
    name, credentials = "todoist", ("TODOIST_API_TOKEN",)
    def refresh(self) -> RefreshResult:
        now = stamp()
        if not self.configured(): return RefreshResult(self.name, "configuration_required", now, self.last_success, [], "Todoist token is not configured.", "Set TODOIST_API_TOKEN outside the repository.")
        records = []
        try:
            for project in self.config["projects"]:
                url = "https://api.todoist.com/rest/v1/tasks?" + urllib.parse.urlencode({"project_id": project["id"]})
                for item in self.transport(url, {"Authorization": "Bearer " + os.environ["TODOIST_API_TOKEN"]}):
                    try:
                        if not item.get("content"): raise ValueError("task content is required")
                        due = item.get("due") or {}; records.append(NormalizedRecord("todoist", str(item["id"]), str(project["id"]), project["name"], item.get("content", ""), item.get("description", ""), "active", due.get("datetime") or due.get("date", ""), "", iso(item.get("updated_at")), item.get("url", ""), now, extra={"priority": item.get("priority"), "labels": item.get("labels", []), "section_id": item.get("section_id") or "", "parent_id": item.get("parent_id") or "", "recurrence": due.get("string") or "", "deadline": (item.get("deadline") or {}).get("date", "")}).to_dict())
                    except Exception as bad: records.append(NormalizedRecord("todoist", str(item.get("id", "unknown")), str(project["id"]), project["name"], source_error="Malformed Todoist task: " + type(bad).__name__, fetched_at=now).to_dict())
            self.last_success = now; return RefreshResult(self.name, "ok", now, now, records)
        except Exception as error:
            status, hint = self.describe_error(error); return RefreshResult(self.name, status, now, self.last_success, records, "Todoist refresh failed.", hint)


class CalendarConnector(Connector):
    name, credentials = "calendar", ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")
    def refresh(self) -> RefreshResult:
        now = stamp()
        if not self.configured(): return RefreshResult(self.name, "configuration_required", now, self.last_success, [], "Google Calendar OAuth is not configured.", "Set read-only OAuth credentials outside the repository.")
        # Refresh-token exchange deliberately uses POST only to the OAuth token issuer; all Calendar data calls are GET.
        try:
            token_request = urllib.request.Request("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({"client_id": os.environ["GOOGLE_CLIENT_ID"], "client_secret": os.environ["GOOGLE_CLIENT_SECRET"], "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode(), method="POST")
            with urllib.request.urlopen(token_request, timeout=12) as response: access_token = json.loads(response.read())["access_token"]
            start = (datetime.now(UTC) - timedelta(days=int(os.getenv("OVERVIEW_PAST_DAYS", "1")))).isoformat(); end = (datetime.now(UTC) + timedelta(days=int(os.getenv("OVERVIEW_FUTURE_DAYS", "14")))).isoformat()
            records = []
            for calendar in self.config["calendars"]:
                if not calendar.get("enabled", True): continue
                query = urllib.parse.urlencode({"timeMin": start, "timeMax": end, "singleEvents": "true", "orderBy": "startTime", "showDeleted": "true"})
                url = "https://www.googleapis.com/calendar/v3/calendars/" + urllib.parse.quote(calendar["id"], safe="") + "/events?" + query
                for item in self.transport(url, {"Authorization": "Bearer " + access_token}).get("items", []):
                    try:
                        start_value = item.get("start", {}).get("dateTime", ""); all_day = item.get("start", {}).get("date", "")
                        records.append(NormalizedRecord("calendar", str(item["id"]), calendar["id"], calendar["name"], item.get("summary", ""), item.get("description", ""), item.get("status", ""), "", all_day or iso(start_value), iso(item.get("updated")), item.get("htmlLink", ""), now, extra={"all_day": bool(all_day), "end": item.get("end", {}).get("date") or iso(item.get("end", {}).get("dateTime")), "recurring_event_id": item.get("recurringEventId", ""), "response_status": next((a.get("responseStatus") for a in item.get("attendees", []) if a.get("self")), "")}).to_dict())
                    except Exception as bad: records.append(NormalizedRecord("calendar", str(item.get("id", "unknown")), calendar["id"], calendar["name"], source_error="Malformed Calendar event: " + type(bad).__name__, fetched_at=now).to_dict())
            self.last_success = now; return RefreshResult(self.name, "ok", now, now, records)
        except Exception as error:
            status, hint = self.describe_error(error); return RefreshResult(self.name, status, now, self.last_success, [], "Calendar refresh failed.", hint)


class TrelloConnector(Connector):
    name, credentials = "trello", ("TRELLO_API_KEY", "TRELLO_API_TOKEN")
    def refresh(self) -> RefreshResult:
        now = stamp()
        if not self.configured(): return RefreshResult(self.name, "configuration_required", now, self.last_success, [], "Trello credentials are not configured.", "Set TRELLO_API_KEY and TRELLO_API_TOKEN outside the repository.")
        records = []
        try:
            auth = urllib.parse.urlencode({"key": os.environ["TRELLO_API_KEY"], "token": os.environ["TRELLO_API_TOKEN"]})
            for board in self.config["boards"]:
                if not board.get("enabled", False): continue
                manifest = self.transport(f"https://api.trello.com/1/boards/{board['id']}/lists?" + auth)
                allowed = {str(x["id"]): x["name"] for x in manifest if not x.get("closed")}
                cards = self.transport(f"https://api.trello.com/1/boards/{board['id']}/cards?fields=id,name,desc,labels,due,dueComplete,url,dateLastActivity,closed,idList,idMembers&" + auth)
                for item in cards:
                    try:
                        list_id = str(item.get("idList", ""));
                        if list_id not in allowed: continue
                        records.append(NormalizedRecord("trello", str(item["id"]), list_id, allowed[list_id], item.get("name", ""), item.get("desc", "")[:500], "closed" if item.get("closed") else "open", iso(item.get("due")), "", iso(item.get("dateLastActivity")), item.get("url", ""), now, extra={"board_id": board["id"], "board_name": board["name"], "due_complete": bool(item.get("dueComplete")), "labels": [x.get("name") or x.get("color", "") for x in item.get("labels", [])], "member_count": len(item.get("idMembers", []))}).to_dict())
                    except Exception as bad: records.append(NormalizedRecord("trello", str(item.get("id", "unknown")), source_error="Malformed Trello card: " + type(bad).__name__, fetched_at=now).to_dict())
            self.last_success = now; return RefreshResult(self.name, "ok", now, now, records)
        except Exception as error:
            status, hint = self.describe_error(error); return RefreshResult(self.name, status, now, self.last_success, records, "Trello refresh failed.", hint)


class DriveConnector(Connector):
    name, credentials = "drive", ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")
    def refresh(self) -> RefreshResult:
        now = stamp()
        if not self.configured(): return RefreshResult(self.name, "configuration_required", now, self.last_success, [], "Google Drive OAuth is not configured.", "Set read-only OAuth credentials outside the repository.")
        # The token exchange mirrors Calendar; metadata GETs never read document bodies.
        try:
            token_request = urllib.request.Request("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({"client_id": os.environ["GOOGLE_CLIENT_ID"], "client_secret": os.environ["GOOGLE_CLIENT_SECRET"], "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode(), method="POST")
            with urllib.request.urlopen(token_request, timeout=12) as response: access_token = json.loads(response.read())["access_token"]
            records=[]
            for item in self.config["shortcuts"]:
                try:
                    url = "https://www.googleapis.com/drive/v3/files/" + urllib.parse.quote(item["id"], safe="") + "?fields=id,name,mimeType,modifiedTime,webViewLink"
                    meta = self.transport(url, {"Authorization": "Bearer " + access_token}); records.append(NormalizedRecord("drive", str(meta["id"]), "", "Curated Drive shortcuts", item.get("label") or meta.get("name", ""), "", "available", "", "", iso(meta.get("modifiedTime")), meta.get("webViewLink") or item.get("url", ""), now, extra={"type": item.get("type", meta.get("mimeType", ""))}).to_dict())
                except Exception as bad: records.append(NormalizedRecord("drive", str(item["id"]), title=item.get("label", ""), source_error="Drive shortcut unavailable: " + type(bad).__name__, fetched_at=now).to_dict())
            self.last_success = now; return RefreshResult(self.name, "ok", now, now, records)
        except Exception as error:
            status, hint = self.describe_error(error); return RefreshResult(self.name, status, now, self.last_success, records, "Drive refresh failed.", hint)


class ConnectorManager:
    def __init__(self, config_dir: Path):
        read = lambda n: json.loads((config_dir / n).read_text(encoding="utf-8"))
        self.connectors = [TodoistConnector(read("todoist_projects.json")), CalendarConnector(read("calendars.json")), TrelloConnector(read("trello_boards.json")), DriveConnector(read("drive_shortcuts.example.json"))]; self.cache: dict[str, RefreshResult] = {}
    def refresh_all(self, force: bool = False) -> list[RefreshResult]:
        seconds = int(os.getenv("CONNECTOR_CACHE_SECONDS", "300")); results=[]
        for connector in self.connectors:
            cached=self.cache.get(connector.name)
            fresh=cached and datetime.fromisoformat(cached.fetched_at) + timedelta(seconds=seconds) > datetime.now(UTC)
            if cached and fresh and not force: results.append(RefreshResult(**{**cached.to_dict(), "status":"cached", "cached":True})); continue
            result=connector.refresh()
            if result.status == "ok": self.cache[connector.name]=result
            elif cached: result=RefreshResult(connector.name, "stale", result.fetched_at, cached.last_success_at, cached.records, result.error, result.recovery_hint)
            results.append(result)
        return results
