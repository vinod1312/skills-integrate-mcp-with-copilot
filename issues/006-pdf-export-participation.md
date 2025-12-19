# 006 — PDF export for participation lists and certificates

- **Priority:** Low
- **Related local file:** `src/app.py`

## Summary
Add PDF export for participation lists and simple certificates or printable reports.

## Acceptance criteria
- Organizers can download a PDF of participants for an activity.
- PDF includes participant names, emails, and participation status.

## Implementation notes
- Use WeasyPrint or ReportLab for server-side PDF generation.
- Export pipeline can reuse CSV export as source.

## References / evidence
- hitobito contains `app/domain/export/pdf/participation/person_and_event.rb` as a reference.
