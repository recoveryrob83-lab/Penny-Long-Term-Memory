from pathlib import Path


STATIC_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard" / "static"


def test_command_center_loads_catalog_metadata_and_selected_preview() -> None:
    script = (STATIC_ROOT / "command-center.js").read_text(encoding="utf-8")

    assert "data.canonical_prompts" in script
    assert "destinationToken" in script
    assert "selectedCanonicalKey" in script
    assert "originPromptKey: selectedCanonicalKey" in script
    assert "custom_prompt: prompt" in script


def test_scheduler_snapshots_canonical_prompt_and_preserves_key() -> None:
    script = (STATIC_ROOT / "command-scheduler.js").read_text(encoding="utf-8")

    assert 'source_type: canonical ? `canonical:${canonicalKey}` : source' in script
    assert "custom_prompt: prompt" in script
    assert "canonicalPromptKeyFromSchedule" in script
    assert 'sourceType.startsWith("canonical:")' in script
