from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

import lifeos_dashboard as package
from lifeos_dashboard import worker_hq_review_resume_runtime as resume
from lifeos_dashboard.worker_result_contract import artifact_checksum
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

REPO_ROOT = Path(__file__).resolve().parents[3]
BOARD_PATH = REPO_ROOT / "coordination" / "boards" / "engineering.md"
RUN_ID = "RUN-ADV-20260726-053-R1"
WORKER_ID = "maintenance_worker"
REPORT_PATH = (
    "projects/life-logistics-hq/worker-results/maintenance_worker/"
    f"{RUN_ID}/report-002.json"
)
PRIOR_PATH = (
    "projects/life-logistics-hq/worker-results/maintenance_worker/"
    f"{RUN_ID}/hq-review-001.json"
)
REVIEW_PATH = (
    "projects/life-logistics-hq/worker-results/maintenance_worker/"
    f"{RUN_ID}/hq-review-002.json"
)


class _DatabaseService:
    def __init__(self, database: Path, root: Path | None = None) -> None:
        self.database = database
        self.root = root or database.parent

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _row(self, run_id: str) -> sqlite3.Row:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM execution_history WHERE run_id = ?",
                (run_id,),
            ).fetchone()
        assert row is not None
        return row

    def _safe_path(self, relative_path: str) -> Path:
        return self.root / relative_path

    @staticmethod
    def _hq_chat_title(owning_department: str) -> str:
        assert owning_department == "maintenance"
        return "Maintenance HQ"

    @staticmethod
    def _validate_review_semantics(payload: dict[str, object]) -> None:
        assert payload["review_state"] in {
            "VERIFIED",
            "REJECTED",
            "REPAIR_REQUIRED",
            "ROB_VALIDATION_REQUIRED",
        }

    @staticmethod
    def _runtime_state(review_state: str) -> str:
        return {
            "VERIFIED": "HQ_VERIFIED",
            "REJECTED": "HQ_REJECTED",
            "REPAIR_REQUIRED": "REPORT_REPAIR_PENDING",
            "ROB_VALIDATION_REQUIRED": "ROB_VALIDATION_REQUIRED",
        }[review_state]

    @staticmethod
    def _git_review_evidence(
        review_path: str,
        payload: dict[str, object],
    ) -> tuple[str, str, str]:
        assert review_path == REVIEW_PATH
        return "c" * 40, "d" * 40, artifact_checksum(payload)


def _authorization() -> resume.HqReviewResumeAuthorization:
    return resume.HqReviewResumeAuthorization(
        advisory_id="ADV-20260728-054",
        advisory_revision=2,
        owner="engineering",
        phase="PHASE_2_ENGINEERING_RUNTIME_ENABLEMENT",
        approval_reference="ROB-DIRECT-HQ-REVIEW-RESUME-RUNTIME-20260728",
        run_id=RUN_ID,
        attempt=2,
        review_path=REVIEW_PATH,
        procedure_path=(
            "projects/life-logistics-hq/procedures/"
            "maintenance_hq_worker_review_receipt.md"
        ),
        procedure_version=2,
        procedure_checksum="sha256:" + "1" * 64,
        procedure_commit_sha="1" * 40,
        procedure_blob_sha="2" * 40,
        report_path=REPORT_PATH,
        report_checksum="sha256:" + "3" * 64,
        report_commit_sha="3" * 40,
        report_blob_sha="4" * 40,
        prior_review_path=PRIOR_PATH,
        prior_review_state="REPAIR_REQUIRED",
        prior_review_checksum="sha256:" + "5" * 64,
        prior_review_commit_sha="5" * 40,
        prior_review_blob_sha="6" * 40,
        write_scopes=tuple(sorted(resume._EXPECTED_WRITE_SCOPES)),
    )


def _database(tmp_path: Path) -> tuple[Path, _DatabaseService]:
    database = tmp_path / "command-center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history(
                id INTEGER PRIMARY KEY,
                run_id TEXT NOT NULL,
                worker_id TEXT NOT NULL,
                owning_department TEXT NOT NULL,
                mode TEXT NOT NULL,
                prompt_type TEXT NOT NULL,
                result_state TEXT,
                report_path TEXT,
                report_checksum TEXT,
                report_commit_sha TEXT,
                report_blob_sha TEXT,
                hq_wake_state TEXT,
                hq_wake_target TEXT,
                hq_wake_marker TEXT,
                hq_wake_user_turn_id TEXT,
                hq_wake_returned_to_source INTEGER,
                hq_wake_sent_at REAL,
                hq_review_path TEXT,
                hq_review_checksum TEXT,
                hq_review_commit_sha TEXT,
                hq_review_blob_sha TEXT,
                hq_review_state TEXT,
                hq_review_reason TEXT,
                hq_review_evidence_json TEXT,
                hq_review_ingested_at REAL,
                ready_for_consumption INTEGER,
                requires_rob_validation INTEGER
            )
            """
        )
        authorization = _authorization()
        connection.execute(
            """
            INSERT INTO execution_history(
                run_id, worker_id, owning_department, mode, prompt_type,
                result_state, report_path, report_checksum, report_commit_sha,
                report_blob_sha, hq_wake_state, hq_wake_target, hq_wake_marker,
                hq_wake_user_turn_id, hq_wake_returned_to_source, hq_wake_sent_at,
                hq_review_path, hq_review_checksum, hq_review_commit_sha,
                hq_review_blob_sha, hq_review_state, hq_review_reason,
                hq_review_evidence_json, hq_review_ingested_at,
                ready_for_consumption, requires_rob_validation
            ) VALUES (
                ?, ?, 'maintenance', 'send', 'worker',
                'REPORT_REPAIR_PENDING', ?, ?, ?, ?,
                'HQ_WAKE_SUBMITTED', 'Maintenance HQ', 'HQ-REVIEW-A1',
                'conversation-turn-25', 1, 100.0,
                ?, ?, ?, ?, 'REPAIR_REQUIRED', 'Procedure v1 was inapplicable.',
                '["prior"]', 101.0, 0, 0
            )
            """,
            (
                RUN_ID,
                WORKER_ID,
                authorization.report_path,
                authorization.report_checksum,
                authorization.report_commit_sha,
                authorization.report_blob_sha,
                authorization.prior_review_path,
                authorization.prior_review_checksum,
                authorization.prior_review_commit_sha,
                authorization.prior_review_blob_sha,
            ),
        )
    service = _DatabaseService(database, tmp_path)
    resume._ensure_resume_columns(service)
    return database, service


def _attempt_two_payload() -> dict[str, object]:
    authorization = _authorization()
    return {
        "schema_id": "lifeos_worker_hq_review",
        "schema_version": 1,
        "artifact_type": "hq_review",
        "attempt": 2,
        "run_id": RUN_ID,
        "worker_id": WORKER_ID,
        "reviewing_hq": "Maintenance HQ",
        "report_path": REPORT_PATH,
        "review_state": "VERIFIED",
        "report_integrity_state": "valid",
        "authority_compliance_state": "compliant",
        "work_verification_state": "verified",
        "evidence_checked": [
            authorization.advisory_id,
            authorization.procedure_path,
            authorization.report_path,
            authorization.prior_review_path,
        ],
        "reason": "The bounded repair report and preserved holds are independently verified.",
        "ready_for_consumption": True,
        "requires_rob_validation": False,
    }


def test_parser_accepts_canonical_revision_two_authority() -> None:
    authorization = resume.parse_resume_authorization(
        BOARD_PATH.read_text(encoding="utf-8")
    )

    assert authorization.advisory_revision == 2
    assert authorization.run_id == RUN_ID
    assert authorization.attempt == 2
    assert authorization.review_path == REVIEW_PATH
    assert set(authorization.write_scopes) == resume._EXPECTED_WRITE_SCOPES


def test_parser_rejects_material_revision_drift() -> None:
    board = BOARD_PATH.read_text(encoding="utf-8").replace(
        "- Advisory Revision: 2",
        "- Advisory Revision: 3",
        1,
    )

    with pytest.raises(WorkerRuntimeError, match="revision is not authorized"):
        resume.parse_resume_authorization(board)


def test_resume_columns_are_additive_and_claim_is_one_shot(tmp_path: Path) -> None:
    database, service = _database(tmp_path)
    authorization = _authorization()
    row = service._row(RUN_ID)

    first = resume._claim_resume_wake(service, row, authorization)
    assert first is not None
    assert resume._claim_resume_wake(service, service._row(RUN_ID), authorization) is None

    resume._release_pretransport_claim(service, int(row["id"]), first)
    second = resume._claim_resume_wake(service, service._row(RUN_ID), authorization)
    assert second is not None

    with sqlite3.connect(database) as connection:
        columns = {
            item[1]
            for item in connection.execute(
                "PRAGMA table_info(execution_history)"
            ).fetchall()
        }
    assert set(resume._RESUME_COLUMNS).issubset(columns)


def test_attempt_two_ingestion_preserves_attempt_one_and_suppresses_duplicate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database, service = _database(tmp_path)
    authorization = _authorization()
    review_file = tmp_path / REVIEW_PATH
    review_file.parent.mkdir(parents=True)
    payload = _attempt_two_payload()
    review_file.write_text(json.dumps(payload), encoding="utf-8")

    claimed_at = resume._claim_resume_wake(
        service,
        service._row(RUN_ID),
        authorization,
    )
    assert claimed_at is not None
    with service._connect() as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                hq_review_resume_state = 'SUBMITTED',
                hq_review_resume_wake_target = 'Maintenance HQ',
                hq_review_resume_wake_marker = 'HQ-REVIEW-RESUME',
                hq_review_resume_wake_user_turn_id = 'conversation-turn-99',
                hq_review_resume_wake_receipt_json = '{}',
                hq_review_resume_wake_returned_to_source = 1,
                hq_review_resume_wake_sent_at = 200.0
            WHERE run_id = ?
            """,
            (RUN_ID,),
        )

    monkeypatch.setattr(resume, "_authorization", lambda service: authorization)

    receipt = resume._ingest_resume_review(service, RUN_ID)
    assert receipt.review_state == "VERIFIED"
    assert receipt.result_state == "HQ_VERIFIED"
    assert receipt.duplicate_suppressed is False

    row = service._row(RUN_ID)
    assert row["hq_review_path"] == REVIEW_PATH
    assert row["hq_review_resume_review_path"] == REVIEW_PATH
    assert row["ready_for_consumption"] == 1
    prior = json.loads(row["hq_review_prior_evidence_json"])
    assert prior["hq_review_path"] == PRIOR_PATH
    assert prior["hq_review_state"] == "REPAIR_REQUIRED"

    duplicate = resume._ingest_resume_review(service, RUN_ID)
    assert duplicate.duplicate_suppressed is True

    with sqlite3.connect(database) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?",
            (RUN_ID,),
        ).fetchone()[0]
    assert count == 1


def test_attempt_two_ingestion_refuses_missing_prior_correlation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, service = _database(tmp_path)
    authorization = _authorization()
    review_file = tmp_path / REVIEW_PATH
    review_file.parent.mkdir(parents=True)
    review_file.write_text(json.dumps(_attempt_two_payload()), encoding="utf-8")

    resume._claim_resume_wake(service, service._row(RUN_ID), authorization)
    with service._connect() as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                hq_review_resume_state = 'SUBMITTED',
                hq_review_resume_wake_returned_to_source = 1,
                hq_review_checksum = 'sha256:changed'
            WHERE run_id = ?
            """,
            (RUN_ID,),
        )
    monkeypatch.setattr(resume, "_authorization", lambda service: authorization)

    with pytest.raises(WorkerRuntimeError, match="authorized review-resume evidence"):
        resume._ingest_resume_review(service, RUN_ID)


def test_runtime_source_uses_existing_budget_lock_and_same_row() -> None:
    source = (
        REPO_ROOT
        / "apps"
        / "lifeos-dashboard"
        / "lifeos_dashboard"
        / "worker_hq_review_resume_runtime.py"
    ).read_text(encoding="utf-8")

    assert "reserve_send_budget" in source
    assert "append_send_budget_evidence" in source
    assert "command_center._run_lock" in source
    assert "UPDATE execution_history" in source
    assert "CREATE TABLE" not in source
    assert "artifact_path(" in source
    assert "Authorized Later Review Path" in source


def test_resume_cycle_requires_current_successful_git_sync() -> None:
    succeeded = SimpleNamespace(
        occurred_at=101.0,
        action="git_sync",
        status="succeeded",
        detail="Git repository is current.",
    )
    skipped = SimpleNamespace(
        occurred_at=102.0,
        action="git_sync",
        status="succeeded",
        detail="Local repository has uncommitted changes; Git sync was skipped.",
    )

    orchestrator = SimpleNamespace(
        _last_cycle_started_at=100.0,
        _events=[succeeded],
    )
    assert package._successful_git_sync_for_cycle(orchestrator) is True

    orchestrator._events = [succeeded, skipped]
    assert package._successful_git_sync_for_cycle(orchestrator) is False


def test_resume_cycle_scans_existing_run_without_worker_discovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str]] = []
    row = {
        "result_state": "REPORT_REPAIR_PENDING",
        "hq_review_state": "REPAIR_REQUIRED",
    }
    orchestrator = SimpleNamespace(
        operations=SimpleNamespace(
            command_center=SimpleNamespace(paused=False),
            hq_review=object(),
        ),
        _last_error=None,
        _cycle_lock=threading.Lock(),
        _row=lambda run_id: row,
        _event=lambda *args, **kwargs: None,
        status=lambda: {"direct_resume": True},
    )

    monkeypatch.setattr(
        package,
        "_base_orchestrator_run_once",
        lambda self: {"base_cycle": True},
    )
    monkeypatch.setattr(
        package,
        "_successful_git_sync_for_cycle",
        lambda self: True,
    )
    monkeypatch.setattr(resume, "_ensure_resume_columns", lambda service: None)
    monkeypatch.setattr(
        resume,
        "_send_resume_wake",
        lambda self, run_id, advisory_id: calls.append(("wake", run_id)),
    )
    monkeypatch.setattr(
        resume,
        "_ingest_resume_if_present",
        lambda self, run_id, advisory_id: calls.append(("ingest", run_id)),
    )

    result = package._composed_orchestrator_run_once(orchestrator)

    assert result == {"direct_resume": True}
    assert calls == [("wake", RUN_ID), ("ingest", RUN_ID)]
