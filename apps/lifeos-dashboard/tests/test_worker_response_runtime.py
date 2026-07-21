from types import SimpleNamespace
from pathlib import Path

from lifeos_dashboard.worker_operations import WorkerOperationsService
from worker_response_test_support import response_text, setup_run, transport_result


class FakePipeline:
    def __init__(self, active, result) -> None:
        self.active = active
        self.result = result

    def discover(self):
        return (self.active,)

    def dispatch(self, advisory_id, **kwargs):
        assert advisory_id == self.active.advisory_id
        assert kwargs["confirm_send"] is True
        return SimpleNamespace(
            advisory=self.active,
            job=SimpleNamespace(envelope=self.active.envelope()),
            result=self.result,
        )


def test_worker_operations_run_reconciles_same_row_before_return(
    tmp_path: Path,
) -> None:
    _receiver, active, entry, database = setup_run(tmp_path)
    service = object.__new__(WorkerOperationsService)
    service.pipeline = FakePipeline(active, transport_result(active, response_text()))
    service.command_center = SimpleNamespace(
        store=SimpleNamespace(database_path=database)
    )
    service.repository_root = tmp_path
    service.worker_center = SimpleNamespace(
        runtime=SimpleNamespace(worker=lambda *_args, **_kwargs: entry)
    )
    service.status = lambda: {"history": "refreshed"}

    payload = service.run_advisory(
        active.advisory_id,
        confirm_send=True,
        timeout_seconds=600,
    )

    assert payload["result"]["transport_status"] == "succeeded"
    assert payload["result"]["status"] == "succeeded"
    assert payload["result"]["receiver_outcome"] == "IMPLEMENT"
    assert payload["result"]["hq_review_required"] is True
    assert payload["receiver"]["state"] == "accepted"
    assert payload["status"] == {"history": "refreshed"}
