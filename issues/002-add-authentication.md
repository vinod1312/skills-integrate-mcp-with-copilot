# 002 — Add authentication (signup/login, confirmable, reset, 2FA opt-in)

- **Priority:** High
- **Related local file:** `src/app.py`

## Summary
Add user authentication so participants can manage signups securely and persist identities instead of email-only records.

## Acceptance criteria
- Users can register and login (password-based).
- Email confirmation flow (confirmable) or account activation exists.
- Password reset flow implemented.
- Optional 2FA support is scaffolded or documented.

## Implementation notes
- Use a standard library (FastAPI Users, or implement with passlib + JWT + email confirmations).
- Integrate auth with DB models from issue 001.

## References / evidence
- hitobito migrations show `add_devise_confirmable_to_person` and `add_two_factor_authentication_attrs_to_person` as evidence of confirmable/2FA flows.
