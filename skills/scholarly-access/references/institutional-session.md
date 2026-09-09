# Institutional session protocol (CUC supervised retrieval)

This protocol applies only to the bounded, screened non-OA list that the user explicitly approved. It never automates credential entry and never stores a password.

## Principles

- The user authenticates once, in their own browser, with their own account (SSO, QR code, or MFA). The agent drives the browser only after the user has completed the login.
- Only a working browser profile is reused during the session. Credentials, cookies, and session secrets are never written to the Skill repository, the project directory, logs, or the final report.
- Download one article at a time with a polite pause. If the provider or institution shows a bulk-download or access limit, stop and mark the remaining items `institution-limited`; do not retry aggressively or bypass the limit.
- No paywall bypass, no DRM removal, no mass crawling of an entire issue or volume.

## Workflow

1. Present the exact non-OA list (DOI, title, journal) and the expected count before starting.
2. Open the publisher or library entry point in a controlled browser.
3. If the institutional session is missing or expired, stop and return `AUTH_REQUIRED`; ask the user to log in again and then continue.
4. For each item, navigate to its landing page, follow the institution's legitimate full-text link or download the PDF the user is entitled to access, and save it to the approved PDF folder.
5. Validate each saved PDF (`%PDF` header, reasonable size, matching DOI/title) and record its status in `downloads.jsonl`.
6. On any access error, record `AUTH_REQUIRED` or `institution-limited` and continue to the next item only if the failure was per-item; if the session expired, stop and wait for the user.

## Status vocabulary additions

- `AUTH_REQUIRED`: the user must authenticate (or re-authenticate) before this item can be fetched.
- `institution-limited`: the provider or institution blocks or caps the requested retrieval; fall back to metadata-only, open access, or repository copies.

## Verification

- Report the final counts per status.
- Report the list of items still `AUTH_REQUIRED` or `institution-limited` with the exact reason and the remaining legal option.
- Never log the URL query strings that contain session tokens; store only the DOI and status.
