from lifeos_dashboard.department_inspection import DepartmentInspectionSource


def test_scope_ids_remain_stable_while_labels_are_canonical() -> None:
    scopes = {
        item["id"]: item["label"]
        for item in DepartmentInspectionSource._scope_payload()
    }

    assert scopes["main-assistant"] == "Chief of Staff HQ"
    assert scopes["logistics"] == "Life OS Maintenance HQ"
    assert scopes["engineering"] == "Engineering HQ"
    assert scopes["system"] == "System"
