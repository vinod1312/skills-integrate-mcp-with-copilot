# 004 — Invitations and participation workflow

- **Priority:** Medium
- **Related local file:** `src/app.py`

## Summary
Add invitation flows, RSVPs, guest lists, and explicit participation records separate from simple signups.

## Acceptance criteria
- API to invite users (by email) to activities.
- Invitees can accept/decline; participation stored in DB.
- Guest list and invitation statuses viewable by organizers.

## Implementation notes
- Model `Invitation` with token-based RSVP links; email delivery using local SMTP or dev console.
- Wire endpoints for invite/create/respond.

## References / evidence
- hitobito has `app/controllers/event/guests_controller.rb` and sheet helpers for participation/invitation exports.
