# Prompt Launcher

Updated: 2026-07-08
Owner: Engineering Classroom
Status: Scaffolded learning project

## Purpose

Prompt Launcher is a simple Python-based desktop utility learning project.

The first goal is to load a JSON prompt library, display prompt buttons, and copy selected prompt text to the clipboard.

Longer term, this project may grow into a standardized Life OS prompt builder.

## Important Boundary

This is an Engineering Classroom learning project.

It is not Chief Engineering Penny operational infrastructure, not Life Logistics automation, and not a production Life OS system.

Do not connect it to GitHub, advisories, or production automation until Rob explicitly chooses to promote it beyond classroom work.

## v0.1 Scope

- Load `prompt_library.json`.
- Show one button per static prompt.
- Copy selected prompt text to clipboard.
- Keep the app local and simple.
- No GitHub integration.
- No advisory loading.
- No production automation.

## Files

- `prompt_launcher.py` — placeholder Python entrypoint for Rob to build in Engineering Classroom.
- `prompt_library.json` — valid skeleton JSON prompt library.
- `README.md` — project purpose, scope, and roadmap.

## Future Roadmap

- Template prompts with variables.
- Advisory prompt builder.
- GitHub advisory list integration.
- Categories, search, and favorites.
- Standard Life OS boot/prompt library.

## Suggested Next Classroom Step

Run the placeholder script locally, confirm it loads `prompt_library.json`, then build the simplest possible UI loop.

Possible first implementation path:

1. Add one sample prompt to `prompt_library.json`.
2. Build a minimal Tkinter window.
3. Render one button per prompt.
4. Copy prompt text to clipboard when a button is clicked.
5. Add basic error handling for malformed JSON.
