"""FastAPI application for the local LifeOS dashboard."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from . import __version__
from .adapters import (
    DashboardSource,
    GoogleCalendarIcalDashboardSource,
    LocalGitHubDashboardSource,
    SampleDashboardSource,
    TodoistDashboardSource,
    TrelloFlowDashboardSource,
)
from .command_center import CommandCenterError, CommandCenterService, CommandJob
from .service import DashboardService

PACKAGE_ROOT = Path(__file__).resolve().parent
APP_ROOT = PACKAGE_ROOT.parent
load_dotenv(APP_ROOT / ".env", override=False)


class CommandJobRequest(BaseModel):
    destination: str
    prompt_type: str
    mode: str = "draft"
    custom_prompt: str = ""
    confirm_send: bool = False


class PauseRequest(BaseModel):
    paused: bool


class SavedPromptRequest(BaseModel):
    name: str
    prompt: str


def _cache_path(environment_name: str, filename: str) -> Path:
    configured = os.getenv(environment_name)
    if configured:
        return Path(configured).expanduser()
    return APP_ROOT / ".local" / filename


def _environment_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().casefold() not in {"0", "false", "no", "off"}


def build_default_source() -> DashboardSource:
    sample_source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
    source: DashboardSource = sample_source
    configured_root = os.getenv("LIFEOS_REPOSITORY_ROOT")
    repo_root = Path(configured_root).expanduser() if configured_root else PACKAGE_ROOT.parents[2]
    if (repo_root / ".git").exists() and (repo_root / "memory").exists():
        source = LocalGitHubDashboardSource(
            repo_root,
            source,
            auto_sync=_environment_flag("LIFEOS_GITHUB_AUTO_SYNC", True),
            sync_branch=os.getenv("LIFEOS_GITHUB_SYNC_BRANCH", "main"),
        )
    source = TrelloFlowDashboardSource.from_environment(
        source, cache_path=_cache_path("TRELLO_CACHE_PATH", "trello_flow_cache.json")
    )
    source = TodoistDashboardSource.from_environment(
        source, cache_path=_cache_path("TODOIST_CACHE_PATH", "todoist_commitments_cache.json")
    )
    return GoogleCalendarIcalDashboardSource.from_environment(
        source, cache_path=_cache_path("GOOGLE_CALENDAR_CACHE_PATH", "google_calendar_cache.json")
    )


def create_app(source: DashboardSource | None = None) -> FastAPI:
    active_source = source or build_default_source()
    service = DashboardService(active_source)
    command_center = CommandCenterService(
        APP_ROOT,
        database_path=_cache_path("COMMAND_CENTER_DATABASE_PATH", "command_center.sqlite3"),
    )
    application = FastAPI(
        title="LifeOS Dashboard",
        description="Local read-mostly LifeOS command window",
        version=__version__,
    )
    application.state.dashboard_service = service
    application.state.command_center = command_center
    application.mount("/static", StaticFiles(directory=PACKAGE_ROOT / "static"), name="static")
    templates = Jinja2Templates(directory=PACKAGE_ROOT / "templates")

    @application.get("/", response_class=HTMLResponse)
    async def dashboard_home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"app_version": __version__},
        )

    @application.get("/api/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__, "mode": service.mode}

    @application.get("/api/dashboard")
    async def dashboard_data() -> dict[str, object]:
        return service.get_snapshot()

    @application.get("/api/command-center")
    async def command_center_status() -> dict[str, object]:
        return command_center.status()

    @application.get("/api/command-center/canonical-prompt/{destination}")
    async def canonical_prompt_preview(destination: str) -> dict[str, str]:
        try:
            return await run_in_threadpool(command_center.canonical_prompt, destination)
        except CommandCenterError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @application.post("/api/command-center/pause")
    async def command_center_pause(request: PauseRequest) -> dict[str, object]:
        command_center.set_paused(request.paused)
        return command_center.status()

    @application.post("/api/command-center/prompts")
    async def save_command_prompt(request: SavedPromptRequest) -> dict[str, object]:
        try:
            command_center.save_prompt(request.name, request.prompt)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return command_center.status()

    @application.put("/api/command-center/prompts/{prompt_id}")
    async def update_command_prompt(prompt_id: int, request: SavedPromptRequest) -> dict[str, object]:
        try:
            updated = command_center.update_prompt(prompt_id, request.name, request.prompt)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if updated is None:
            raise HTTPException(status_code=404, detail="Saved prompt not found.")
        return command_center.status()

    @application.delete("/api/command-center/prompts/{prompt_id}")
    async def delete_command_prompt(prompt_id: int) -> dict[str, object]:
        if not command_center.delete_prompt(prompt_id):
            raise HTTPException(status_code=404, detail="Saved prompt not found.")
        return command_center.status()

    @application.post("/api/command-center/run")
    async def command_center_run(request: CommandJobRequest) -> dict[str, object]:
        job = CommandJob(
            destination=request.destination,
            prompt_type=request.prompt_type,  # type: ignore[arg-type]
            mode=request.mode,  # type: ignore[arg-type]
            custom_prompt=request.custom_prompt,
            confirm_send=request.confirm_send,
        )
        result = await run_in_threadpool(command_center.execute, job)
        return result.to_dict()

    return application


app = create_app()
