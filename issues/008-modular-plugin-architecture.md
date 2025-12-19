# 008 — Modular / plugin architecture (wagons-like)

- **Priority:** Low
- **Related local file:** `src/app.py`

## Summary
Introduce a simple modular structure to let features be added/removed (inspired by hitobito's "wagons").

## Acceptance criteria
- Codebase organized so features (auth, exports) can be developed as isolated modules/app packages.
- Clear extension points and docs for adding new modules.

## Implementation notes
- Start with a folder-per-feature layout under `src/` and documented registration hooks.

## References / evidence
- hitobito documents modular "wagons" in `doc/architecture/wagons/README.md`.
