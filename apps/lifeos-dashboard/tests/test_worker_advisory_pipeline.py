from dataclasses import dataclass, field
from pathlib import Path

import pytest

from lifeos_dashboard.worker_advisory_pipeline import (
    AdvisoryWakePipeline,
    build_wake_job,
    parse_advisory_index,
    parse_execution_ready_advisory,
)
from lifeos_dashboard.worker_command_center import WorkerExecutionResult
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

INDEX = (
    "# Advisory Index\n\n"
    "## Open / Unacknowledged Advisories\n\n"
    "- ADV-20260720-046 — OPEN — Posted Board: "
    "`coordination/boards/engineering.md` — Target Department: Engineering HQ — "
    "Run a bounded Worker pilot.\n"
    "- ADV-20260718-042 — OPEN — Posted Board: "
    "`coordination/boards/main-assistant.md` — Target Department: Engineering HQ — "
    "Existing HQ-targeted advisory.\n"
)

BOARD = """# Engineering HQ Advisory Board

### ADV-20260720-046 — Reconcile Worker readiness records

- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Target Department and Owner: Engineering HQ
- Target Worker ID: `engineering_worker`
- Task Class: `bounded_engineering_maintenance`
- Authorization Class: `BOUNDED_WRITE`
- Procedure ID: `engineering_bounded_maintenance`
- Procedure Version: 1
- Authorization Source: `ENGINEERING_HQ`
- Parameters JSON: `{"targets":["projects/engineering/status.md"]}`
- Source References JSON: `["projects/engineering/status.md"]`
- Requested Read Scopes JSON: `["projects/engineering/status.md"]`
- Requested Write Scopes JSON: `["projects/engineering/status.md"]`
- Requested Tools JSON: `["GitHub"]`
- Completion Condition: Exact target updated, read back, and reported for Immediate HQ review.

#### Assignment

Read the canonical advisory and perform only the bounded work.
"""

HQ_BOARD = """# Chief of Staff Board

### ADV-20260718-042 — Existing HQ-targeted advisory

- Lifecycle State: OPEN
- Priority: HIGH
- Target Department and Owner: Engineering HQ
"""


@dataclass
class FakeCenter:
    seen: set[str] = field(default_factory=set)
    calls: list[object] = field(default_factory=list)

    def execute(self, job, *, trigger="manual", timeout_seconds=120):
        del timeout_seconds
        self.calls.append((job, trigger))
        key = job.envelope.idempotency_key
        if key in self.seen:
            return WorkerExecutionResult(
                status="refused",
                destination="Engineering_Worker",
                mode=job.mode,
                reason="This Worker task revision already has a successful send record.",
            )
        self.seen.add(key)
        return WorkerExecutionResult(
            status="succeeded",
            destination="Engineering_Worker",
            mode=job.mode,
            reason="Synthetic reference-only wake delivered.",
        )


def write_repo(root: Path, *, board: str = BOARD, index: str = INDEX) -> None:
    (root / "coordination/boards").mkdir(parents=True)
    (root / "coordination/ADVISORY_INDEX.md").write_text(index, encoding="utf-8")
    (root / "coordination/boards/engineering.md").write_text(board, encoding="utf-8")
    (root / "coordination/boards/main-assistant.md").write_text(HQ_BOARD, encoding="utf-8")


def test_index_returns_open_routing_records() -> None:
    records = parse_advisory_index(INDEX)
    assert [record.advisory_id for record in records] == ["ADV-20260720-046", "ADV-20260718-042"]
    assert records[0].board_path == "coordination/boards/engineering.md"


def test_non_worker_advisory_is_not_wake_candidate() -> None:
    records = parse_advisory_index(INDEX)
    resolved = parse_execution_ready_advisory(HQ_BOARD, records[1])
    assert resolved is None


def test_execution_ready_advisory_builds_deterministic_reference_only_job() -> None:
    advisory = parse_execution_ready_advisory(BOARD, parse_advisory_index(INDEX)[0])
    assert advisory is not None
    job = build_wake_job(advisory)
    assert job.envelope.worker_id == "engineering_worker"
    assert job.envelope.run_id == "RUN-ADV-20260720-046-R1"
    assert job.envelope.idempotency_key == "engineering_worker:ADV-20260720-046:1"
    assert "Reconcile Worker readiness records" not in job.instruction
    assert "Do not execute from this transport text" in job.instruction
    assert "Do not close the advisory unless" in job.instruction


def test_pipeline_discovers_only_worker_target_and_dispatches(tmp_path: Path) -> None:
    write_repo(tmp_path)
    center = FakeCenter()
    pipeline = AdvisoryWakePipeline(tmp_path, center)

    discovered = pipeline.discover()
    first = pipeline.dispatch("ADV-20260720-046")
    duplicate = pipeline.dispatch("ADV-20260720-046")

    assert [item.advisory_id for item in discovered] == ["ADV-20260720-046"]
    assert first.result.status == "succeeded"
    assert duplicate.result.status == "refused"
    assert len(center.calls) == 2


def test_source_index_target_conflict_fails_closed(tmp_path: Path) -> None:
    conflicted = BOARD.replace(
        "Target Department and Owner: Engineering HQ",
        "Target Department and Owner: Business HQ",
    )
    write_repo(tmp_path, board=conflicted)

    with pytest.raises(WorkerRuntimeError, match="conflicts with the Advisory Index"):
        AdvisoryWakePipeline(tmp_path, FakeCenter()).discover()


def test_missing_execution_field_fails_closed(tmp_path: Path) -> None:
    malformed = BOARD.replace("- Procedure Version: 1\n", "")
    write_repo(tmp_path, board=malformed)

    with pytest.raises(WorkerRuntimeError, match="missing fields"):
        AdvisoryWakePipeline(tmp_path, FakeCenter()).discover()


def test_repository_escape_fails_closed(tmp_path: Path) -> None:
    write_repo(tmp_path)
    pipeline = AdvisoryWakePipeline(tmp_path, FakeCenter(), advisory_index_path="../outside.md")

    with pytest.raises(WorkerRuntimeError, match="escapes the repository root"):
        pipeline.discover()


def test_invalid_json_shape_fails_closed(tmp_path: Path) -> None:
    malformed = BOARD.replace(
        '- Requested Tools JSON: `["GitHub"]`',
        '- Requested Tools JSON: `{"tool":"GitHub"}`',
    )
    write_repo(tmp_path, board=malformed)

    with pytest.raises(WorkerRuntimeError, match="wrong JSON shape"):
        AdvisoryWakePipeline(tmp_path, FakeCenter()).discover()
