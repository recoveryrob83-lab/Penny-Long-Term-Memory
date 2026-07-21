"""Compatibility shim for the superseded browser-response receiver runtime.

Package E now separates dispatch, immutable Worker reporting, deterministic ingestion,
and Department HQ review. Browser dispatch therefore does not wait for or reconcile
assistant chat responses. The receiver implementation remains available for historical
rows and focused tests, but it is not installed on live Worker Operations dispatch.
"""
from __future__ import annotations


def install_worker_response_receiver() -> bool:
    """Keep legacy automatic chat-response reconciliation disabled."""

    return False


__all__ = ["install_worker_response_receiver"]
