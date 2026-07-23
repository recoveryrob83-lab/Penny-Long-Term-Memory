"""FastAPI application for the local LifeOS dashboard."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
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
from .department_inspection import DepartmentInspectionSource
from .service import DashboardService
from .worker_route_management import RouteAwareWorkerOperationsService
from .worker_runtime import WorkerRuntimeError

PACKAGE_ROOT = Path(__file__).resolve().parent
APP_ROOT = PACKAGE_ROOT.parent
load_dotenv(APP_ROOT / ".env", override=False)


class CommandJobRequest(BaseModel):
    destination: str
    prompt_type: str
    mode: str = "draft"
    custom_prompt: str = ""
    confirm_send: bool = False
    default_destination: str | None = None
    confirm_destination: bool = False


class PauseRequest(BaseModel):
    paused: bool


class SavedPromptRequest(BaseModel):
    name: str
    prompt: str
    default_destination: str | None = None
    origin_type: str | None = None
    origin_prompt_key: str | None = None


class ScheduledJobRequest(BaseModel):
    name: str
    destination: str
    prompt_type: str
    custom_prompt: str = ""
    mode: str = "draft"
    confirm_send: bool = False
    default_destination: str | None = None
    confirm_destination: bool = False
    source_type: str
    source_prompt_id: int | None = None
    cadence: str
    schedule_date: str
    schedule_time: str
    weekdays: list[int] = Field(default_factory=list)
    timezone: str = "America/Chicago"
    enabled: bool = True


class ScheduleEnabledRequest(BaseModel):
    enabled: bool


class WorkerAdvisoryRunRequest(BaseModel):
    advisory_id: str
    confirm_send: bool = False
    timeout_seconds: int = Field(default=600, ge=60, le=900)


class WorkerCourierSelfTestRequest(BaseModel):
    confirm_send: bool = False
    timeout_seconds: int = Field(default=300, ge=60, le=900)


class WorkerRouteCaptureRequest(BaseModel):
    worker_id: str
    expected_route_revision: int = Field(ge=0)
    confirm_capture: bool = False


class WorkerReviewRequest(BaseModel):
    run_id: str
    state: str
    actor: str = "Engineering HQ"
    reason: str


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


def _repository_root() -> Path | None:
    configured_root = os.getenv("LIFEOS_REPOSITORY_ROOT")
    candidate = (
        Path(configured_root).expanduser()
        if configured_root
        else PACKAGE_ROOT.parents[2]
    )
    if (candidate / ".git").exists() and (candidate / "memory").exists():
        return candidate
    return None


def build_default_source() -> DashboardSource:
    sample_source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
    source: DashboardSource = sample_source
    repo_root = _repository_root()
    if repo_root is not None:
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


def create_app(
    source: DashboardSource | None = None,
    *,
    start_scheduler: bool | None = None,
    inspection_source: DepartmentInspectionSource | None = None,
) -> FastAPI:
    active_source = source or build_default_source()
    service = DashboardService(active_source)
    scheduler_enabled = (
        _environment_flag("LIFEOS_LEGACY_SCHEDULER_ENABLED", False)
        if start_scheduler is None
        else start_scheduler
    )
    command_center = CommandCenterService(
        APP_ROOT,
        database_path=_cache_path("COMMAND_CENTER_DATABASE_PATH", "command_center.sqlite3"),
    )
    repository_root = _repository_root() if source is None else None
    worker_operations = (
        RouteAwareWorkerOperationsService(command_center, repository_root)
        if repository_root is not None
        else None
    )
    department_inspection = inspection_source or DepartmentInspectionSource(
        repository_root if source is None else None
    )
    application = FastAPI(
        title="LifeOS Dashboard",
        description="Local read-mostly LifeOS command window",
        version=__version__,
    )
    application.state.dashboard_service = service
    application.state.command_center = command_center
    application.state.worker_operations = worker_operations
    application.state.department_inspection = department_inspection
    application.mount("/static", StaticFiles(directory=PACKAGE_ROOT / "static"), name="static")
    templates = Jinja2Templates(directory=PACKAGE_ROOT / "templates")

    @application.on_event("startup")
    async def start_command_scheduler() -> None:
        if scheduler_enabled:
            command_center.start_scheduler()

    @application.on_event("shutdown")
    async def stop_command_scheduler() -> None:
        command_center.stop_scheduler()

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

    @application.get("/api/department-inspection")
    async def department_inspection_data() -> dict[str, object]:
        return await run_in_threadpool(department_inspection.load)

    @application.get("/api/command-center")
    async def command_center_status() -> dict[str, object]:
        return command_center.status()

    @application.get("/api/worker-operations")
    async def worker_operations_status() -> dict[str, object]:
        if worker_operations is None:
            raise HTTPException(
                status_code=503,
                detail="Worker Operations requires a local LifeOS repository checkout.",
            )
        return await run_in_threadpool(worker_operations.status)

    @application.post("/api/worker-operations/routes/capture")
    async def capture_worker_route(
        request: WorkerRouteCaptureRequest,
    ) -> dict[str, object]:
        if worker_operations is None:
            raise HTTPException(
                status_code=503,
                detail="Worker Operations requires a local LifeOS repository checkout.",
            )
        try:
            result = await run_in_threadpool(
                worker_operations.routes.capture_active_route,
                request.worker_id,
                expected_route_revision=request.expected_route_revision,
                confirm_capture=request.confirm_capture,
            )
            result["operations"] = worker_operations.status()
            return result
        except WorkerRuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @application.post("/api/worker-operations/run")
    async def run_worker_advisory(request: WorkerAdvisoryRunRequest) -> dict[str, object]:
        if worker_operations is None:
            raise HTTPException(
                status_code=503,
                detail="Worker Operations requires a local LifeOS repository checkout.",
            )
        try:
            return await run_in_threadpool(
                worker_operations.run_advisory,
                request.advisory_id,
                confirm_send=request.confirm_send,
                timeout_seconds=request.timeout_seconds,
            )
        except WorkerRuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @application.post("/api/worker-operations/self-test")
    async def worker_courier_self_test(
        request: WorkerCourierSelfTestRequest,
    ) -> dict[str, object]:
        if worker_operations is None:
            raise HTTPException(
                status_code=503,
                detail="Worker Operations requires a local LifeOS repository checkout.",
            )
        try:
            return await run_in_threadpool(
                worker_operations.courier_self_test,
                confirm_send=request.confirm_send,
                timeout_seconds=request.timeout_seconds,
            )
        except WorkerRuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @application.post("/api/worker-operations/review")
    async def review_worker_run(request: WorkerReviewRequest) -> dict[str, object]:
        if worker_operations is None:
            raise HTTPException(
                status_code=503,
                detail="Worker Operations requires a local LifeOS repository checkout.",
            )
        try:
            return await run_in_threadpool(
                worker_operations.review,
                request.run_id,
                request.state,
                actor=request.actor,
                reason=request.reason,
            )
        except WorkerRuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

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
            command_center.save_prompt(
                request.name,
                request.prompt,
                default_destination=request.default_destination,
                origin_type=request.origin_type,
                origin_prompt_key=request.origin_prompt_key,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return command_center.status()

    @application.put("/api/command-center/prompts/{prompt_id}")
    async def update_command_prompt(
        prompt_id: int, request: SavedPromptRequest
    ) -> dict[str, object]:
        try:
            updated = command_center.update_prompt(
                prompt_id,
                request.name,
                request.prompt,
                default_destination=request.default_destination,
                origin_type=request.origin_type,
                origin_prompt_key=request.origin_prompt_key,
            )
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

    @application.post("/api/command-center/schedules")
    async def create_command_schedule(request: ScheduledJobRequest) -> dict[str, object]:
        try:
            command_center.create_schedule(request.model_dump())
        except (ValueError, CommandCenterError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return command_center.status()

    @application.put("/api/command-center/schedules/{schedule_id}")
    async def update_command_schedule(
        schedule_id: int, request: ScheduledJobRequest
    ) -> dict[str, object]:
        try:
            updated = command_center.update_schedule(schedule_id, request.model_dump())
        except (ValueError, CommandCenterError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if updated is None:
            raise HTTPException(status_code=404, detail="Scheduled job not found.")
        return command_center.status()

    @application.post("/api/command-center/schedules/{schedule_id}/enabled")
    async def set_command_schedule_enabled(
        schedule_id: int, request: ScheduleEnabledRequest
    ) -> dict[str, object]:
        try:
            updated = command_center.set_schedule_enabled(schedule_id, request.enabled)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if updated is None:
            raise HTTPException(status_code=404, detail="Scheduled job not found.")
        return command_center.status()

    @application.delete("/api/command-center/schedules/{schedule_id}")
    async def delete_command_schedule(schedule_id: int) -> dict[str, object]:
        if not command_center.delete_schedule(schedule_id):
            raise HTTPException(status_code=404, detail="Scheduled job not found.")
        return command_center.status()

    @application.post("/api/command-center/run")
    async def command_center_run(request: CommandJobRequest) -> dict[str, object]:
        job = CommandJob(
            destination=request.destination,
            prompt_type=request.prompt_type,  # type: ignore[arg-type]
            mode=request.mode,  # type: ignore[arg-type]
            custom_prompt=request.custom_prompt,
            confirm_send=request.confirm_send,
            default_destination=request.default_destination,
            confirm_destination=request.confirm_destination,
        )
        result = await run_in_threadpool(command_center.execute, job)
        return result.to_dict()

    return application


app = create_app()
