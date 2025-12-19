# 005 — Import / export CSV pipelines (people, participants)

- **Priority:** Low
- **Related local file:** `src/app.py`

## Summary
Provide CSV import/export for people and participation lists to ease administrative tasks and migration from other systems.

## Acceptance criteria
- CSV export for participant lists per activity.
- CSV import for batch-creating people/participants with validation and dry-run mode.

## Implementation notes
- Add import domain logic and background task support for large files.
- Provide validation errors and logs for administrators.

## References / evidence
- hitobito includes `app/domain/import/person.rb` and multiple `app/helpers/sheet/*` helpers for exports.
