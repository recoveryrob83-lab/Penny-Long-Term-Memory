"""Small local API for the future dashboard and extension."""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from .contracts import CommandState, Route
from .reader import AdvisoryReader
from .runtime import CourierService, RuntimeStore


class RouteInput(BaseModel):
    route_name: str
    target: str
    chatgpt_url: HttpUrl
    health: str = "AVAILABLE"


class TelemetryInput(BaseModel):
    note: str = ""


class HeartbeatInput(BaseModel):
    version: str = ""


class ReadinessInput(BaseModel):
    route_name: str
    url: str = ""
    content_script: bool = False
    composer_ready: bool = False
    composer_empty: bool = False
    send_control: bool = False
    test_armed: bool = False


def create_app(root: Path, persistence_path: Path, index_path: str = "coordination/ADVISORY_INDEX.md") -> FastAPI:
    reader = AdvisoryReader(root, index_path, "https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory/blob/main")
    service = CourierService(RuntimeStore(persistence_path))
    from .connectors import ConnectorManager
    from .github_status import GitHubStatusVerifier
    connector_manager = ConnectorManager(Path(__file__).parent.parent / "config")
    github_verifier = GitHubStatusVerifier()
    app = FastAPI(title="LifeOS V2 Courier", version="0.1.0")
    dashboard_root = Path(__file__).parent / "dashboard"
    app.mount("/static", StaticFiles(directory=dashboard_root), name="static")

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(dashboard_root / "index.html")

    def snapshot() -> tuple[list, dict[str, str]]:
        advisories, errors = reader.read()
        service.reconcile(advisories)
        return advisories, errors

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "paused": service.paused}

    @app.get("/status")
    def status() -> dict:
        advisories, errors = snapshot()
        return {"paused": service.paused, "advisory_count": len(advisories), "parse_errors": errors, "command_count": len(service.commands()), "events": service.store.data.get("events", []), "extension": service.store.data.get("extension", {}), "tab_readiness": service.readiness()}

    @app.get("/dashboard/overview")
    def overview(force: bool = False) -> dict:
        """Read-only live model when configured; deterministic fixtures otherwise."""
        import os
        from .dashboard_data import overview_from_connectors, overview_model
        configured = any(os.getenv(key) for key in ("TODOIST_API_TOKEN", "TRELLO_API_KEY", "GOOGLE_REFRESH_TOKEN"))
        fixture_mode = os.getenv("LIFEOS_FIXTURE_MODE", "auto").lower()
        if fixture_mode == "true" or (fixture_mode == "auto" and not configured): return overview_model()
        return overview_from_connectors([item.to_dict() for item in connector_manager.refresh_all(force)], github_verifier.verify())

    @app.get("/dashboard/inspector")
    def inspector() -> dict:
        """Bounded configured-path read model; it never writes source records."""
        from .dashboard_data import inspector_model
        return inspector_model(root)

    @app.get("/advisories")
    def advisories() -> dict:
        items, errors = snapshot()
        return {"items": [item.to_dict() for item in items], "parse_errors": errors}

    @app.get("/advisories/{advisory_id}")
    def advisory(advisory_id: str) -> dict:
        items, _ = snapshot()
        found = next((item for item in items if item.advisory_id == advisory_id), None)
        if not found:
            raise HTTPException(404, "Advisory not found")
        return found.to_dict()

    @app.get("/routes")
    def routes() -> dict:
        return {"items": service.routes()}

    @app.post("/routes", status_code=201)
    def routes_create(payload: RouteInput) -> dict:
        route = Route(payload.route_name, payload.target, str(payload.chatgpt_url), datetime.now(UTC).isoformat(), health=payload.health)
        return service.register_route(route)

    @app.delete("/routes/{route_name}", status_code=204)
    def routes_delete(route_name: str) -> None:
        if not service.delete_route(route_name):
            raise HTTPException(404, "Route not found")

    @app.get("/commands")
    def commands() -> dict:
        return {"items": service.commands()}

    @app.get("/commands/{command_id}")
    def command(command_id: str) -> dict:
        found = next((item for item in service.commands() if item["command_id"] == command_id), None)
        if not found:
            raise HTTPException(404, "Command not found")
        return found

    @app.get("/extension/commands/{route_name}")
    def extension_command(route_name: str) -> dict:
        return {"paused": service.paused, "command": service.eligible_command(route_name)}

    @app.post("/commands/{command_id}/begin")
    def begin(command_id: str) -> dict:
        command = service.begin_attempt(command_id)
        if not command:
            raise HTTPException(409, "Command is not eligible for dispatch")
        return command

    @app.post("/extension/heartbeat")
    def heartbeat(payload: HeartbeatInput) -> dict:
        return service.heartbeat(payload.version)

    @app.post("/extension/readiness")
    def readiness(payload: ReadinessInput) -> dict:
        return service.report_readiness(**payload.model_dump())

    def telemetry(state: CommandState) -> Callable:
        def handler(command_id: str, payload: TelemetryInput) -> dict:
            changed = service.update_telemetry(command_id, state, payload.note)
            if not changed:
                raise HTTPException(404, "Command not found")
            return changed
        return handler

    app.post("/commands/{command_id}/ack")(telemetry(CommandState.DELIVERED))
    app.post("/commands/{command_id}/fail")(telemetry(CommandState.FAILED))
    app.post("/commands/{command_id}/uncertain")(telemetry(CommandState.UNCERTAIN))

    @app.post("/system/pause")
    def pause() -> dict:
        service.pause()
        return {"paused": True}

    @app.post("/system/resume")
    def resume() -> dict:
        service.resume()
        snapshot()
        return {"paused": False}

    return app
