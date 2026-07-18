"""Protected canonical prompt definitions for the Automation Command Center.

`memory/CONTEXT_REMINDER.md` remains the canonical command vocabulary. This
module is the executable catalog consumed by the local dashboard. Saved prompts
remain editable snapshots; definitions in this catalog are read-only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

PromptScope = Literal["department", "target_department", "current_department"]


@dataclass(frozen=True)
class CanonicalPromptDefinition:
    key: str
    label: str
    category: str
    description: str
    scope: PromptScope
    read_only: bool


CATALOG: tuple[CanonicalPromptDefinition, ...] = (
    CanonicalPromptDefinition("boot", "Boot", "Boot / Sync", "Load the canonical operating kernel and role-routed department context.", "department", True),
    CanonicalPromptDefinition("quick_boot", "Quick Boot", "Boot / Sync", "Run a concise read-only department boot and synchronization.", "department", True),
    CanonicalPromptDefinition("full_boot", "Fresh / Full Boot", "Boot / Sync", "Run a clean replacement boot without relying on stale chat memory.", "department", True),
    CanonicalPromptDefinition("sync", "Sync", "Boot / Sync", "Compare current chat context with authoritative files and report meaningful drift.", "current_department", True),
    CanonicalPromptDefinition("nightly", "Nightly", "Daily Operations", "Run the department's read-only end-of-day synchronization.", "current_department", True),
    CanonicalPromptDefinition("advisory", "Advisory", "Advisory", "Draft one routed advisory for the selected target department without posting it.", "target_department", True),
    CanonicalPromptDefinition("sync_advisory", "Sync Advisory", "Advisory", "Inspect advisory state for drift without changing durable records.", "current_department", True),
    CanonicalPromptDefinition("read_advisory", "Read Advisory", "Advisory", "Read and interpret one advisory without acknowledging or changing it.", "current_department", True),
    CanonicalPromptDefinition("consume_advisory", "Consume Advisory", "Advisory", "Process one advisory only after its identity and bounded authority are explicit.", "current_department", False),
)

_BY_KEY = {definition.key: definition for definition in CATALOG}


def definition_for(key: str) -> CanonicalPromptDefinition:
    try:
        return _BY_KEY[key]
    except KeyError as exc:
        raise ValueError(f"Unknown canonical prompt: {key}") from exc


def catalog_metadata() -> list[dict[str, object]]:
    return [asdict(definition) for definition in CATALOG]


def render_prompt(key: str, *, destination_label: str, boot_prompt: str) -> str:
    """Render one protected prompt for the selected Command Center destination."""
    definition_for(key)
    label = destination_label

    if key == "boot":
        return boot_prompt.rstrip() + "\n"
    if key == "quick_boot":
        return f"""/BOOT @GitHub

Department: {label}

Load the canonical global operating kernel and this HQ's role-routed context. Remain read-only. Then report current status, active priorities, owned open loops, advisory dependencies, meaningful drift, and the single best next action.
"""
    if key == "full_boot":
        body = boot_prompt.rstrip()
        if body.startswith("@GitHub boot and sync."):
            body = body[len("@GitHub boot and sync."):].lstrip()
        return f"""/FRESHBOOT @GitHub

This is a clean replacement boot for {label}. Do not rely on prior chat memory as authoritative.

{body}
"""
    if key == "sync":
        return f"""/SYNC @GitHub

Current HQ: {label}

Compare this chat's current context with the authoritative global kernel and this HQ's owned files. Report meaningful drift, stale assumptions, active priorities, open loops, dependencies, and the smallest useful next action. Remain read-only and do not create maintenance work merely for visibility.
"""
    if key == "nightly":
        return f"""/NIGHTLY @GitHub

Current HQ: {label}

Run the canonical read-only end-of-day synchronization for this HQ. Read the current calendar day's relevant notebook entries, review completed work, unfinished owned loops, stale local documentation, advisory state, blockers, and the next handoff needed. Do not modify GitHub or external systems unless Rob separately authorizes a bounded action.
"""
    if key == "advisory":
        return f"""/ADVISORY @GitHub

Target department: {label}

Draft one concise formal advisory under the canonical source-board and Advisory Index contract. Identify the real source owner, target, request, boundaries, dependencies, duplicate check, requested response, and closure condition. Do not post the advisory or change durable state unless Rob explicitly authorizes sending it.
"""
    if key == "sync_advisory":
        return f"""/SYNCADVISORY @GitHub

Current HQ: {label}

Read the Advisory Index and only the relevant canonical source boards. Report open, stale, duplicate, inconsistent, misrouted, or closure-ready advisory state. Remain read-only. Do not acknowledge, process, implement, close, or rewrite advisory records.
"""
    if key == "read_advisory":
        return f"""/READADVISORY @GitHub

Current HQ: {label}

Ask Rob for the advisory ID or an unambiguous advisory reference if it is not already present in the conversation. Then read the Advisory Index and canonical source board and summarize the request, current status, relevance, required action, boundaries, dependencies, and recommended response. Remain read-only. Do not acknowledge, process, implement, close, or modify GitHub.
"""
    return f"""/CONSUMEADVISORY @GitHub

Current HQ: {label}

Before changing durable state, identify the advisory ID, this HQ's requested response, the exact department-owned files that would change, and the statement authorizing those bounded changes. If any element is missing or ownership conflicts, stop and ask Rob. Once authority is explicit, perform only the authorized department-level documentation work, record this target's acknowledgement or ingestion on the canonical source board, reconcile the Advisory Index, preserve per-target state, and close nothing unless all closure conditions are satisfied. Report exact paths and state changes.
"""
