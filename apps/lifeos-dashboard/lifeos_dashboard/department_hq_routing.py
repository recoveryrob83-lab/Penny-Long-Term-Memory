"""Fail-closed Package F department-to-HQ destination resolution.

This module resolves canonical department HQ titles and an explicitly registered department-owned
HQ review procedure. Resolution does not create a Worker, register a private route, authorize a
send, or broaden any department's authority.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Mapping

from .room_titles import CANONICAL_HQ_TITLES
from .worker_runtime import WorkerRuntimeError


class DepartmentHqRoutingError(WorkerRuntimeError):
    """Raised when an owning department cannot resolve one safe exact HQ destination."""


@dataclass(frozen=True)
class DepartmentHqRoute:
    """Resolved pointer-only destination metadata for one owning department."""

    department_key: str
    hq_chat_title: str
    automation_title: str
    review_procedure_path: str


_DEPARTMENT_ALIASES: dict[str, str] = {
    "maintenance": "logistics",
    "maintenance-hq": "logistics",
    "logistics": "logistics",
    "life-os-maintenance": "logistics",
    "engineering": "engineering",
    "engineering-hq": "engineering",
    "business": "business",
    "business-hq": "business",
    "office-leaks": "office-leaks",
    "officeleaks": "office-leaks",
    "office-leaks-hq": "office-leaks",
    "office-leaks-consulting": "office-leaks",
    "finance": "finance",
    "finance-hq": "finance",
    "chief-of-staff": "main",
    "chief-of-staff-hq": "main",
    "chief-staff": "main",
    "main": "main",
    "main-assistant": "main",
    "wellness": "wellness",
    "wellness-hq": "wellness",
}

_ENV_PREFIX_BY_KEY: dict[str, str] = {
    "logistics": "MAINTENANCE",
    "engineering": "ENGINEERING",
    "business": "BUSINESS",
    "office-leaks": "OFFICE_LEAKS",
    "finance": "FINANCE",
    "main": "CHIEF_OF_STAFF",
    "wellness": "WELLNESS",
}

_DEFAULT_REVIEW_PROCEDURES: dict[str, str] = {
    "engineering": "projects/engineering/procedures/engineering_hq_worker_review_receipt.md",
}

_HUB_ALIASES = {
    "hub",
    "lifeos",
    "lifeos-hq",
    "life-os-hq",
}


def _normalize_token(value: str) -> str:
    token = str(value or "").strip().casefold().replace("_", " ")
    return re.sub(r"[^a-z0-9]+", "-", token).strip("-")


def canonical_department_key(value: str) -> str:
    """Return the executable canonical department key for one explicit known alias."""

    token = _normalize_token(value)
    if not token:
        raise DepartmentHqRoutingError("Owning department cannot be empty.")
    if token in _HUB_ALIASES:
        raise DepartmentHqRoutingError("LifeOS_HQ is a shared meeting room, not an owning department.")
    key = _DEPARTMENT_ALIASES.get(token)
    if key is None or key not in _ENV_PREFIX_BY_KEY:
        raise DepartmentHqRoutingError(f"Unknown owning department: {value!r}.")
    return key


def _environment(environment: Mapping[str, str] | None) -> Mapping[str, str]:
    return os.environ if environment is None else environment


def _exact_title_override(
    *,
    environment: Mapping[str, str],
    variable_name: str,
    expected_title: str,
) -> str:
    configured = str(environment.get(variable_name) or "").strip()
    if not configured:
        return expected_title
    if configured != expected_title:
        raise DepartmentHqRoutingError(
            f"{variable_name} must equal the canonical exact title {expected_title!r}."
        )
    return configured


def resolve_hq_chat_title(
    owning_department: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> str:
    """Resolve one canonical department HQ chat title without creating route authority."""

    key = canonical_department_key(owning_department)
    expected = CANONICAL_HQ_TITLES[key]
    prefix = _ENV_PREFIX_BY_KEY[key]
    return _exact_title_override(
        environment=_environment(environment),
        variable_name=f"LIFEOS_{prefix}_HQ_CHAT_TITLE",
        expected_title=expected,
    )


def resolve_hq_automation_title(
    owning_department: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> str:
    """Resolve one canonical exact automation destination title."""

    key = canonical_department_key(owning_department)
    expected = CANONICAL_HQ_TITLES[key]
    prefix = _ENV_PREFIX_BY_KEY[key]
    return _exact_title_override(
        environment=_environment(environment),
        variable_name=f"LIFEOS_{prefix}_HQ_AUTOMATION_TITLE",
        expected_title=expected,
    )


def _review_procedure_path(
    department_key: str,
    *,
    environment: Mapping[str, str],
) -> str:
    prefix = _ENV_PREFIX_BY_KEY[department_key]
    variable_name = f"LIFEOS_{prefix}_HQ_REVIEW_PROCEDURE"
    configured = str(environment.get(variable_name) or "").strip()
    value = configured or _DEFAULT_REVIEW_PROCEDURES.get(department_key, "")
    if not value:
        raise DepartmentHqRoutingError(
            f"{variable_name} is required before {CANONICAL_HQ_TITLES[department_key]} "
            "can receive an owning-HQ review wake."
        )

    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        path.is_absolute()
        or not path.parts
        or path.parts[0] != "projects"
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix.casefold() != ".md"
    ):
        raise DepartmentHqRoutingError(
            f"{variable_name} must be one safe repository-relative Markdown path under projects/."
        )
    return path.as_posix()


def resolve_department_hq_route(
    owning_department: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> DepartmentHqRoute:
    """Resolve exact HQ titles plus an explicit department-owned review procedure.

    Non-Engineering departments remain held until their review procedure is explicitly registered.
    This is a destination-resolution gate only; callers still own route availability, execution lock,
    pause, duplicate-suppression, and send-confirmation checks.
    """

    values = _environment(environment)
    key = canonical_department_key(owning_department)
    return DepartmentHqRoute(
        department_key=key,
        hq_chat_title=resolve_hq_chat_title(owning_department, environment=values),
        automation_title=resolve_hq_automation_title(owning_department, environment=values),
        review_procedure_path=_review_procedure_path(key, environment=values),
    )


__all__ = [
    "DepartmentHqRoute",
    "DepartmentHqRoutingError",
    "canonical_department_key",
    "resolve_department_hq_route",
    "resolve_hq_automation_title",
    "resolve_hq_chat_title",
]
