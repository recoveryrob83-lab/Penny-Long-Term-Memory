from pathlib import Path


STATIC_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard" / "static"


def test_completed_debug_recurrence_is_hidden_from_upcoming() -> None:
    script = (STATIC_ROOT / "command-history.js").read_text(encoding="utf-8")

    assert 'return completed && ["scheduled", "paused"].includes(stateFilter.value);' in script
    assert "article.remove();" in script
    assert "No upcoming scheduled jobs match these filters." in script
    assert "visibleDefinitions" in script


def test_clear_completed_removes_definitions_and_preserves_history() -> None:
    script = (STATIC_ROOT / "command-history.js").read_text(encoding="utf-8")

    assert 'button.id = "cc-clear-completed";' in script
    assert 'button.textContent = `Clear completed (${completedSchedules.length})`;' in script
    assert 'schedule.cadence === "once" && schedule.last_status === "succeeded"' in script
    assert "Debug recurrence test completed after two attempts." in script
    assert 'fetch(`/api/command-center/schedules/${schedule.id}`, {method: "DELETE"})' in script
    assert "Run history was preserved." in script
    assert "its local schedule definition was kept" in script


def test_scheduler_ledger_health_is_visible() -> None:
    script = (STATIC_ROOT / "command-history.js").read_text(encoding="utf-8")

    assert '"Ledger off"' in script
    assert '"Ledger ready"' in script
    assert '"Ledger synced"' in script
    assert '"Ledger error"' in script
    assert "schedule_ledger" in script


def test_overdue_one_time_remains_paused_and_visible() -> None:
    script = (STATIC_ROOT / "command-scheduler.js").read_text(encoding="utf-8")

    assert '["succeeded", "failed", "refused"].includes(schedule.last_status)' in script
    assert 'Boolean(schedule.last_status)' not in script
    assert 'return !schedule.enabled && !isFinishedOneTime(schedule);' in script


def test_no_future_run_cards_sort_by_recent_change() -> None:
    script = (STATIC_ROOT / "command-scheduler.js").read_text(encoding="utf-8")

    assert 'if (leftNext !== rightNext) return leftNext - rightNext;' in script
    assert 'if (!Number.isFinite(leftNext)) {' in script
    assert 'return recentTime(right) - recentTime(left) || Number(right.id) - Number(left.id);' in script
