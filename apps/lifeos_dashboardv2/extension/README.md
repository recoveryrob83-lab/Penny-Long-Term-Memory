# LifeOS V2 local courier extension

Load this directory unpacked from `chrome://extensions` with Developer mode enabled. It requests only the active tab, tabs, local extension storage, ChatGPT conversation pages, and `127.0.0.1:8765`. No credentials are stored. The popup registers an exact current ChatGPT URL under a configured route label; replacement requires confirmation.

The service worker polls the local server once per minute. It fails closed on server errors, pause, emergency stop, missing route, URL mismatch, occupied composer, or selector failure. It uses bounded composer selectors and validates the exact inserted payload before a single click. After any possible send it verifies only user-authored message nodes for an exact payload match; it never reads assistant messages. A failed pre-send attempt returns to Pending while under three attempts. Any post-send ambiguity becomes Uncertain and is never replayed.

On ChatGPT versions that show Voice mode for an empty composer, readiness accepts the bounded Voice control as evidence that the composer can transition to Send. Dispatch still requires a visible enabled Send control after exact insertion; Voice is never clicked.

## User-assisted browser acceptance

When Codex cannot attach to the user's Chrome or Edge tab, use a dedicated non-production chat and a local fixture advisory. Capture the exact registered URL, popup confirmation, visible user-authored test wake, and dashboard/`/commands` output. Codex can validate the local runtime and persistence, but must record the external-browser limitation rather than claim direct browser control. If no content-script response is available after dispatch has begun, the command is `UNCERTAIN` and must not be replayed.
