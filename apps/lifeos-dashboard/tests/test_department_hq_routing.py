import pytest

from lifeos_dashboard.department_hq_routing import (
    DepartmentHqRoutingError,
    canonical_department_key,
    resolve_department_hq_route,
    resolve_hq_automation_title,
    resolve_hq_chat_title,
)
from lifeos_dashboard.worker_hq_review import WorkerHqReviewService
import lifeos_dashboard.worker_hq_review_runtime  # noqa: F401 - installs the runtime patch


@pytest.mark.parametrize(
    ("alias", "expected_key", "expected_title", "prefix"),
    [
        ("maintenance", "logistics", "Maintenance_HQ", "MAINTENANCE"),
        ("Engineering_HQ", "engineering", "Engineering_HQ", "ENGINEERING"),
        ("business", "business", "Business_HQ", "BUSINESS"),
        ("office leaks", "office-leaks", "Office_Leaks_HQ", "OFFICE_LEAKS"),
        ("finance", "finance", "Finance_HQ", "FINANCE"),
        ("chief_of_staff", "main", "Chief_of_Staff_HQ", "CHIEF_OF_STAFF"),
        ("wellness", "wellness", "Wellness_HQ", "WELLNESS"),
    ],
)
def test_supported_departments_resolve_from_canonical_titles(
    alias: str,
    expected_key: str,
    expected_title: str,
    prefix: str,
) -> None:
    environment = {
        f"LIFEOS_{prefix}_HQ_REVIEW_PROCEDURE": (
            f"projects/test-fixtures/{expected_key}-hq-review.md"
        )
    }

    route = resolve_department_hq_route(alias, environment=environment)

    assert canonical_department_key(alias) == expected_key
    assert route.department_key == expected_key
    assert route.hq_chat_title == expected_title
    assert route.automation_title == expected_title
    assert route.review_procedure_path.endswith("-hq-review.md")


def test_engineering_keeps_its_registered_default_review_procedure() -> None:
    route = resolve_department_hq_route("engineering", environment={})

    assert route.hq_chat_title == "Engineering_HQ"
    assert route.automation_title == "Engineering_HQ"
    assert route.review_procedure_path == (
        "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
    )


def test_nonengineering_route_requires_explicit_review_procedure() -> None:
    with pytest.raises(DepartmentHqRoutingError, match="HQ_REVIEW_PROCEDURE is required"):
        resolve_department_hq_route("maintenance", environment={})


def test_exact_canonical_title_override_is_accepted() -> None:
    environment = {
        "LIFEOS_MAINTENANCE_HQ_CHAT_TITLE": "Maintenance_HQ",
        "LIFEOS_MAINTENANCE_HQ_AUTOMATION_TITLE": "Maintenance_HQ",
        "LIFEOS_MAINTENANCE_HQ_REVIEW_PROCEDURE": (
            "projects/life-logistics-hq/procedures/maintenance_hq_worker_review.md"
        ),
    }

    route = resolve_department_hq_route("maintenance", environment=environment)

    assert route.hq_chat_title == "Maintenance_HQ"
    assert route.automation_title == "Maintenance_HQ"


@pytest.mark.parametrize(
    ("function", "variable_name"),
    [
        (resolve_hq_chat_title, "LIFEOS_FINANCE_HQ_CHAT_TITLE"),
        (resolve_hq_automation_title, "LIFEOS_FINANCE_HQ_AUTOMATION_TITLE"),
    ],
)
def test_wrong_department_title_override_fails_closed(function, variable_name: str) -> None:
    with pytest.raises(DepartmentHqRoutingError, match="canonical exact title"):
        function("finance", environment={variable_name: "Engineering_HQ"})


@pytest.mark.parametrize("department", ["LifeOS_HQ", "hub", "", "unknown-department"])
def test_hub_empty_and_unknown_owners_fail_closed(department: str) -> None:
    with pytest.raises(DepartmentHqRoutingError):
        canonical_department_key(department)


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "../maintenance-review.md",
        "/projects/maintenance-review.md",
        "coordination/maintenance-review.md",
        "projects/life-logistics-hq/procedures/maintenance-review.json",
    ],
)
def test_review_procedure_path_must_be_safe_repository_markdown(unsafe_path: str) -> None:
    with pytest.raises(DepartmentHqRoutingError, match="repository-relative Markdown"):
        resolve_department_hq_route(
            "maintenance",
            environment={"LIFEOS_MAINTENANCE_HQ_REVIEW_PROCEDURE": unsafe_path},
        )


def test_runtime_patch_replaces_engineering_only_base_title_resolver() -> None:
    assert WorkerHqReviewService._hq_chat_title("maintenance") == "Maintenance_HQ"
    assert WorkerHqReviewService._hq_chat_title("office-leaks") == "Office_Leaks_HQ"
