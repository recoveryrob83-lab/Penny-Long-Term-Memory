"""FastAPI application for the local LifeOS dashboard."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import __version__
from .adapters import (
    DashboardSource,
    LocalGitHubDashboardSource,
    SampleDashboardSource,
    TrelloFlowDashboardSource,
)
from .service import DashboardService

PACKAGE_ROOT = Path(__file__).resolve().parent
APP_ROOT = PACKAGE_ROOT.parent
load_dotenv(APP_ROOT / ".env", override=False)


def build_default_source() -> DashboardSource:
    """Build the live source chain, falling back source-by-source when needed."""
    sample_source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
    source: DashboardSource = sample_source

    configured_root = os.getenv("LIFEOS_REPOSITORY_ROOT")
    repo_root = (
        Path(configured_root).expanduser()
        if configured_root
        else PACKAGE_ROOT.parents[2]
    )
    if (repo_root / ".git").exists() and (repo_root / "memory").exists():
        source = LocalGitHubDashboardSource(repo_root, source)

    configured_cache = os.getenv("TRELLO_CACHE_PATH")
    cache_path = (
        Path(configured_cache).expanduser()
        if configured_cache
        else APP_ROOT / ".local" / "trello_flow_cache.json"
    )
    return TrelloFlowDashboardSource.from_environment(source, cache_path=cache_path)


def create_app(source: DashboardSource | None = None) -> FastAPI:
    """Create a configured dashboard application."""
    active_source = source or build_default_source()
    service = DashboardService(active_source)

    application = FastAPI(
        title="LifeOS Dashboard",
        description="Local read-mostly LifeOS command window",
        version=__version__,
    )
    application.state.dashboard_service = service

    application.mount(
        "/static",
        StaticFiles(directory=PACKAGE_ROOT / "static"),
        name="static",
    )
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
        return {
            "status": "ok",
            "version": __version__,
            "mode": service.mode,
        }

    @application.get("/api/dashboard")
    async def dashboard_data() -> dict[str, object]:
        return service.get_snapshot()

    return application


app = create_app()
