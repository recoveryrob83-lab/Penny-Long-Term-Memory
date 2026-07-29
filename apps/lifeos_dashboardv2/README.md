# LifeOS V2 — Slice One Server and Contracts

This is the local, restart-safe courier foundation only. It has no dashboard or browser-extension implementation.

## Run

From this directory, run `python -m uvicorn lifeos_v2.main:app --port 8765`. Set `LIFEOS_V2_REPOSITORY_ROOT` to the repository root and optionally `LIFEOS_V2_PERSISTENCE_PATH`. `.env.example` intentionally contains names only.

## API

- `GET /health`, `GET /status`
- `GET /advisories`, `GET /advisories/{id}`
- `GET, POST /routes`, `DELETE /routes/{route_name}`
- `GET /commands`, `GET /commands/{id}`
- `POST /commands/{id}/ack|fail|uncertain`
- `POST /system/pause`, `POST /system/resume`

The Markdown reader follows only active Advisory Index entries and their referenced board files. A record is accepted only when it has the approved V2 fields, including explicit scope and updated time. One bad record is returned under `parse_errors` and cannot block valid records.

Commands are keyed by the immutable `advisory_id-r{revision}` identity in a local JSON file. Telemetry changes command transport state only; it never changes advisory truth. Pause makes polling observational; resume rereads current source truth and suppresses stale pending commands rather than replaying a queue.
