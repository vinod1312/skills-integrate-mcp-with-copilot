# 003 — Membership and role management

- **Priority:** Medium
- **Related local file:** `src/app.py`

## Summary
Implement memberships (users belonging to groups/activities) and role-based access (admin, organizer, participant).

## Acceptance criteria
- Users can belong to activities as participants or organizers.
- Roles are assignable and enforced for admin-only endpoints.
- Basic UI or API for listing members and their roles.

## Implementation notes
- Create `Membership` / `Role` models; add authorization checks (dependency injection in FastAPI).
- Consider a simple DSL or RBAC mapping for permissions.

## References / evidence
- hitobito contains role/ability DSL and `app/abilities/*` files illustrating role-based constraints.
