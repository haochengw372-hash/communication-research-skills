# Acceptance prompt: full-text resolution for a DOI list

## Prompt

Use `$scholarly-access` to resolve full text for this DOI list in dry-run mode. Output one row per DOI with status (`oa`, `institution`, `repository`, `delivery`, or `unavailable`), a reason, and the next action.

DOIs:

```text
10.1080/0123456789abcdef
10.1177/0123456789abcdef
10.1111/0123456789abcdef
10.1002/0123456789abcdef
10.1016/j.chb.2024.108123
```

Constraints:

- Do not download anything; do not authenticate anywhere.
- Do not create, read, or reference credential stores.
- If the institution adapter is not provided, treat every paywalled item as `unavailable` with the missing-access reason instead of guessing.
- Save the output table only into a scratch folder.
