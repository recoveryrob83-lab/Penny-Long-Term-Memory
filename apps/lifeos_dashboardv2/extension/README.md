# LifeOS V2 local courier extension

Load this directory unpacked from `chrome://extensions` with Developer mode enabled. It requests only the active tab, tabs, local extension storage, ChatGPT conversation pages, and `127.0.0.1:8765`. No credentials are stored. The popup registers an exact current ChatGPT URL under a configured route label; replacement requires confirmation.

The service worker polls the local server once per minute. It fails closed on server errors, pause, emergency stop, missing route, URL mismatch, occupied composer, or selector failure. It uses bounded composer selectors and validates the exact inserted payload before a single click. After any possible send it verifies only user-authored message nodes for an exact payload match; it never reads assistant messages. A failed pre-send attempt returns to Pending while under three attempts. Any post-send ambiguity becomes Uncertain and is never replayed.
