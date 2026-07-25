from pathlib import Path

from lifeos_dashboard.worker_activation_readiness import (
    WorkerActivationReadinessService,
)

from .test_worker_activation_readiness import _finding, _write_database


def test_current_engineering_profile_and_review_procedure_match_contract(
    tmp_path: Path,
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    database_path = tmp_path / "command-center.sqlite3"
    _write_database(database_path)
    before_database = database_path.read_bytes()
    profile_path = repository_root / "projects/engineering/workers/engineering_worker.md"
    procedure_path = (
        repository_root
        / "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
    )
    before_profile = profile_path.read_bytes()
    before_procedure = procedure_path.read_bytes()
    service = WorkerActivationReadinessService(repository_root, database_path)

    report = service.report("engineering_worker")

    assert _finding(report, "profile.metadata").state == "PASS"
    assert _finding(report, "profile.sections").state == "PASS"
    assert _finding(report, "profile.retirement").state == "PASS"
    assert _finding(report, "review.worker_title").state == "PASS"
    assert _finding(report, "review.procedure_metadata").state == "PASS"
    assert _finding(report, "review.procedure_sections").state == "PASS"
    assert report.activation_authorized is False
    assert database_path.read_bytes() == before_database
    assert profile_path.read_bytes() == before_profile
    assert procedure_path.read_bytes() == before_procedure
