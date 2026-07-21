from lifeos_dashboard import worker_advisory_pipeline
from lifeos_dashboard.worker_response_receiver_runtime import (
    install_worker_response_receiver,
)


def test_legacy_chat_response_reconciliation_is_not_installed() -> None:
    assert install_worker_response_receiver() is False
    assert not getattr(
        worker_advisory_pipeline,
        "_lifeos_worker_report_requirement_installed",
        False,
    )
