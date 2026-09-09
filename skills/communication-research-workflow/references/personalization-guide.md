# Private personalization guide

## Contents

1. Layer model
2. What to personalize
3. Source materials
4. Where to place information
5. Privacy and maintenance

## 1. Layer model

Keep three instruction layers separate:

1. **Public Skill defaults** — generic workflow, schemas, scripts, gates, and examples suitable for publication.
2. **Private researcher profile** — stable expertise, agenda, methods, data practices, writing preferences, and collaboration boundaries. Keep this local.
3. **Project contract and `AGENTS.md`** — project-specific sources, definitions, paths, samples, methods, venues, and permissions.

Use this priority:

```text
current explicit user instruction
> current task contract
> project AGENTS.md
> private researcher profile
> public Skill defaults
```

Do not edit the public profile with private details in a repository that will be published. Create a private derivative Skill with a different name, or keep local untracked overrides.

## 2. What to personalize

Distill only stable, useful instructions:

| Section | Add | Do not add |
|---|---|---|
| Research identity | preferred language, career stage, disciplinary communities | unnecessary contact details or government identifiers |
| Research agenda | recurring questions, constructs, theories, contribution standards | unpublished full proposals or raw notes |
| Methods | established methods, methods needing extra audit, preferred software | credentials or undocumented claims of competence |
| Data ecosystems | platforms, identifier namespaces, source-of-truth rules, coverage concerns | API keys, cookies, licensed raw data |
| Project conventions | directory roles, naming conventions, authoritative artifact rules | a broad permission to scan every local directory |
| Writing | target audiences, paragraph logic, terminology, causal-language rules | manuscript full text copied into the Skill |
| Review | severity labels, decision criteria, desired reviewer stance | automatic permission to rewrite reviewed work |
| Collaboration | progress cadence, authority limits, preferred deliverable form | raw chat transcripts |
| Failure prevention | repeated observed errors and their correction rules | speculative personality judgments |

Start from [profile.template.md](../assets/personalization/profile.template.md). Replace placeholders only in a private copy.

## 3. Source materials

Use a minimal, representative sample rather than ingesting everything:

- curriculum vitae or public researcher profile for stable expertise;
- titles, abstracts, introductions, discussions, and reviewer responses from representative publications;
- data dictionaries, codebooks, analysis plans, and reproducibility notes;
- project handoffs and accepted decision logs;
- interaction-history summaries that reveal repeated scope, writing, or verification preferences.

Distill patterns. Do not package source documents, unpublished datasets, full conversations, personal correspondence, or inaccessible licensed content.

Treat coauthored writing as evidence about collaboration outputs, not proof that every sentence reflects one person's individual style. Label uncertain preferences and let the researcher correct them.

## 4. Where to place information

### Private derivative Skill

Place stable private defaults in:

```text
references/profile-and-preferences.md
references/private-research-profile.md
references/private-writing-and-review-style.md
```

Update `SKILL.md` to read those files at startup. Give the derivative a distinct folder and frontmatter name so it cannot be confused with the public Skill.

### Project `AGENTS.md`

Place project-local rules here:

- project identity and allowed root;
- authoritative data, manuscript, and code locations;
- directory-specific write permissions;
- domain terminology and target venue;
- prohibited actions and external-write rules.

### Task contract

Place volatile decisions here:

- the current goal and deliverable;
- source version, fields, keys, sample, exclusions, time window, and estimand;
- operation, authority, write scope, constraints, stop conditions, and audit requirement.

Do not put rapidly changing project facts in the stable private profile.

## 5. Privacy and maintenance

- Keep private profiles out of the public repository and its Git history.
- Store no credentials, raw chat logs, full papers, protected data, or private keys in a Skill.
- Prefer summaries, controlled vocabularies, aliases, and artifact locators.
- Review the profile after five accepted real work packages; update only from observed evidence and researcher approval.
- Run the public privacy audit before every release and manually inspect the Git diff and history.
- If a private value was committed, removing it from the latest file is insufficient; rotate exposed credentials and clean repository history before publication.
