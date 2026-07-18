from pathlib import Path


STATIC_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard" / "static"


def test_completed_debug_recurrence_is_hidden_from_upcoming() -> None:
    script = (STATIC_ROOT / "command-history.js").read_text(encoding="utf-8")

    assert 'return completed && ["scheduled", "paused"].includes(stateFilter.value);' in script
    assert "article.remove();" in script
    assert "No upcoming scheduled jobs match these filters." in script
    assert "visibleDefinitions" in script
