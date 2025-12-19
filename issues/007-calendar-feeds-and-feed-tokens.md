# 007 — Calendar feeds and event feed tokens

- **Priority:** Low
- **Related local file:** `src/app.py`

## Summary
Provide iCal/ICS feeds for activities and per-user feed tokens for read-only calendar integration.

## Acceptance criteria
- Endpoint to fetch iCal feed for an activity.
- Per-user (or per-person) feed token support for private feeds.

## Implementation notes
- Implement token model and migrations; generate ICS output for events.

## References / evidence
- hitobito migrations include `add_event_feed_token_to_person` showing feed token usage.
