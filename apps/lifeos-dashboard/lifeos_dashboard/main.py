"""FastAPI application for the local LifeOS dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import __version__
from .adapters import DashboardSource, SampleDashboardSource
from .service import DashboardService

PACKAGE_ROOT = Path(__file__).resolve().parent


def create_app(source: DashboardSource | None = None) -> FastAPI:
    """Create a configured dashboard application."""
    active_source = source or SampleDashboardSource(
        PACKAGE_ROOT / "data" / "sample_dashboard.json"
    )
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
