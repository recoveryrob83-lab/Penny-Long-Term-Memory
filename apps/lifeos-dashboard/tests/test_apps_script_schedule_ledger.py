from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "apps-script"
    / "scheduler_ledger_web_app.gs"
)


def test_apps_script_deletes_rows_instead_of_leaving_blank_holes() -> None:
    script = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "compactBlankScheduleRows_(sheet);" in script
    assert "sheet.deleteRow(rowNumber);" in script
    assert "sheet.getRange(rowNumber, 1, 1, 18).clearContent();" not in script


def test_apps_script_compacts_existing_blank_rows_bottom_up() -> None:
    script = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "for (let index = blankRows.length - 1; index >= 0; index -= 1)" in script
    assert "sheet.deleteRow(blankRows[index]);" in script
