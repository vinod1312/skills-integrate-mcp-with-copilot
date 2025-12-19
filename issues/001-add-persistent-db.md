# 001 — Add persistent database and migrations

- **Priority:** High
- **Related local file:** `src/app.py`

## Summary
Replace the in-memory `activities` store in `src/app.py` with a persistent database and add migrations. This provides durability and enables later features (auth, roles, imports/exports).

## Acceptance criteria
- App uses a database for activities, participants, and users.
- CRUD endpoints operate against the DB (existing endpoints updated).
- Migrations are included (Alembic or equivalent) and runnable.
- A lightweight dev DB (SQLite) works out of the box; PG supported via env config.

## Implementation notes
- Suggested stack: SQLModel or SQLAlchemy + Alembic (or TortoiseORM + aerich).
- Add models: `Activity`, `Participant` (or `Membership`), `User`.
- Add basic tests for persistence.

## References / evidence
- Local: `src/app.py` currently holds an in-memory dict.
- Inspiration: hitobito's `app/models/*` and `db/migrate/*` patterns.
