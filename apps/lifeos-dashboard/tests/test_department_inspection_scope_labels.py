from lifeos_dashboard.department_inspection import DepartmentInspectionSource


def test_scope_ids_remain_stable_while_labels_are_canonical() -> None:
    scopes = {
        item["id"]: item["label"]
        for item in DepartmentInspectionSource._scope_payload()
    }

    assert scopes["main-assistant"] == "Chief_of_Staff_HQ"
    assert scopes["logistics"] == "Maintenance_HQ"
    assert scopes["engineering"] == "Engineering_HQ"
    assert scopes["business"] == "Business_HQ"
    assert scopes["office-leaks"] == "Office_Leaks_HQ"
    assert scopes["finance"] == "Finance_HQ"
    assert scopes["wellness"] == "Wellness_HQ"
    assert scopes["system"] == "System"
