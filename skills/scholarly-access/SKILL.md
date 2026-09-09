---
name: scholarly-access
description: Resolve and legally acquire scholarly full text for communication and other research through a five-layer policy (open access, institutional subscription, federated authentication, repositories, and library delivery), normalize metadata, and archive to Zotero or a local research library. Use when the user asks for paper full text, DOI downloads, institutional access, PDF retrieval, or literature archiving (论文全文/文献获取/DOI下载/机构访问/入库). Never stores passwords and never downloads without explicit user confirmation.
---

# Scholarly Access

## Overview

This Skill turns a citation (DOI or title) into a resolved full-text plan. A literature search result is not yet a usable corpus; only a validated full text with provenance enters the research library. Resolution always follows the five-layer order in [references/resolver-layers.md](references/resolver-layers.md), and every run starts as a dry run.

## Security invariants (do not relax)

- Never store, read, or echo plaintext passwords, tokens, or session secrets. No credential vault, no `.env` password, no username/password fields in this Skill or its institution files.
- Authentication is always the user's own action in a user-authenticated browser session (school SSO, QR code, MFA, or institutional login). When a session is missing or expired, stop and return `AUTH_REQUIRED`; do not automate login or keep the session alive beyond the user's control.
- Do not bypass paywalls, do not break DRM, and do not run bulk scraping that exceeds a database's license terms. Normal single-item or project-scale retrieval is allowed; if a provider limits batch download, switch to metadata-only, open-access, or the provider's legal API.
- Every non-dry run requires the user's explicit confirmation for the exact targets.

## Required start

1. Read [references/resolver-layers.md](references/resolver-layers.md) to fix the five-layer order.
2. Read [references/zotero.md](references/zotero.md) when the user wants archiving or reference-library updates.
3. Inspect the available institution configuration (e.g. `institutions/cuc.yaml`) only to know which resources are eligible and how the user authenticates. Institution files contain no credentials.
4. Run `python scripts/resolve_paper.py --doi <DOI>... --dry-run` first, or the equivalent with `--title` when no DOI is available.

## Workflow

1. Normalize the request: DOI, title, authors, year, venue, and any existing file paths or Zotero collection.
2. Deduplicate by DOI first and normalized title second before resolving.
3. Resolve through the layers in order and record one status per item: `oa`, `institution`, `repository`, `delivery`, or `unavailable`, plus the source URL/identifier and a reason.
4. Validate any PDF that would be kept: readable, correct document (not a captcha or error page), matching DOI/title metadata, and file-size sanity.
5. Archive metadata to `metadata.csv` and `references.bib` when no Zotero connection is available; with an authorized Zotero connection, create items under the requested collection with tags, rename files to `Author_Year_ShortTitle.pdf`, and verify the import.
6. Report the acquisition summary as a table with counts per layer, unresolved items, and the exact `AUTH_REQUIRED` or permission choices that remain.

## Output shape

End with a compact summary:

```text
Resolution: 163/183 full text acquired
oa           67
institution  79
repository   11
delivery      6
unavailable  20
```

For each unavailable item give the remaining option and why it is blocked (license limit, no institutional access, metadata missing, or user action needed).

## Common anti-patterns

- Skipping OpenAlex/Unpaywall and going straight to a publisher HTML page.
- Treating a search engine snippet or a landing page as the full text.
- Hard-coding a school's resource list as if it were a credential store.
- Automating a login sequence or saving an authenticated session without the user's own action.
- Renaming or filing PDFs before validating that they match the citation.

## Institution adapters

Institution files under `institutions/` describe only access topology: `name`, `homepage`, `sso_type`, `resources`, `auth_flow`, and `notes`. Add a new institution by copying a generic template (`generic-ezproxy.yaml`, `generic-openathens.yaml`, `generic-shibboleth.yaml`, or `generic-webvpn.yaml`) and filling the user-visible fields.
