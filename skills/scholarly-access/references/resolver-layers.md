# Five-layer resolver policy

Resolve in this exact order. Each layer is cheaper, faster, and more permissive than the next. A lower layer is used only when higher layers produced no usable full text.

| Layer | Name | Source of truth | What the agent may do |
|---|---|---|---|
| 1 | Open access | OpenAlex `best_oa_location` / `pdf_url`, Unpaywall by DOI, publisher OA pages, institutional and subject repositories | Fully automated read-only lookup; download only after user confirmation |
| 2 | Institutional subscription | Institution library gateway and database navigation, publisher pages behind the user's institutional session | Plan only; return `AUTH_REQUIRED` and let the user authenticate in their own browser |
| 3 | Federated authentication | OpenAthens, Shibboleth/SAML, EZproxy, WebVPN configured by the institution | Plan only; same user-authenticated-session rule |
| 4 | Repository and author version | Author/accepted manuscript: arXiv, SSRN, OSF, Zenodo, SSRN, university repositories, author homepages | Automated metadata lookup; download only from legitimate sources and after confirmation |
| 5 | Library delivery | Interlibrary loan or document delivery (for example 超星/百链 style delivery in Chinese university libraries) | Hand off to the library service; never fake a request or bypass quotas |

## Layer 1 details

- Prefer the publisher's published version; accepted and submitted manuscripts are fallbacks, in that order, when the published version is not open.
- Use the DOI as the primary key. When no DOI exists, use normalized title plus year and venue, then record the uncertainty.
- Verify the PDF URL scheme and that the target is the expected document before filing.

## Layer 2 and 3 details

- Institution configuration is about topology only: which resources the user can reach, what authentication flow the school uses, and where the library entry point lives.
- Never collect credentials. The user authenticates in a browser profile they control. The agent may reuse that profile only while the user keeps it active and only for retrieval within the user's entitlements.
- If the resource is not in the institution's list, move to layer 4 or 5 rather than guessing.

## Layer 5 details

- Library delivery is a legitimate last resort for items the institution does not hold directly. Record the request and expected delivery time; treat the delivered copy under the library's terms.

## Status vocabulary

Each item ends with one status:

- `oa` — open-access full text located;
- `institution` — eligible through the institution, but a user-authenticated session is required;
- `repository` — a legitimate repository or author version located;
- `delivery` — library delivery is the remaining legal route;
- `unavailable` — no legal route found under the current institution and permissions.

For every item, record the reason, the candidate source URL/identifier, and the next action, so an unresolved item is a decision, not a dead end.

## License and bulk rules

- Single-article and research-project-scale retrieval is normal use.
- When a database states a bulk-download limit, stop at the limit and switch to metadata-only, open-access, or the provider API.
- Do not circumvent access controls, authentication, or usage caps.
