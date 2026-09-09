---
name: communication-literature
description: Search, screen, and synthesize communication and media literature into verified evidence matrices for reviews, theory papers, and study designs. Use for communication literature review, systematic-style search, evidence mapping, claim support checks, 或传播学文献综述/文献检索/证据矩阵/引文核查. Do not use for full-text download or PDF filing, which routes to scholarly-access.
---

# Communication Literature

## Overview

This Skill turns a research question into a reproducible evidence base: a search log, screening rules, an evidence matrix, and a claim-support record. The output is a corpus of verified sources, each labeled with what it actually supports.

## Required start

1. Lock the question and the object (journalism, platform, HMC, audience, public opinion, discourse) so the search cannot silently drift into another literature.
2. Record search decisions before results: databases, venues, query strings, date windows, language, and inclusion/exclusion rules.
3. Do not treat a retrieval count as synthesis. Screen titles and abstracts, then full texts where the claim requires them.

## Database and venue routing

Choose sources from the actual indexing, not from brand lists. As a default routing:

- English communication journals: Journal of Communication, JCMC, Communication Research, Human Communication Research, New Media & Society, Mass Communication & Society, Journal of Broadcasting & Electronic Media, Communication Methods and Measures, plus ICA/division-affiliated venues relevant to the topic.
- Indexes for communication: Communication & Mass Media Complete, Web of Science (incl. SSCI), Scopus, and Google Scholar for citation chasing when the underlying source is verified.
- Chinese-language research: CNKI and Wanfang for journal coverage, and Chinese-language venues 新闻与传播研究/国际新闻界/现代传播 when the topic requires local scholarship. WoS does not substitute for Chinese database coverage.
- Open metadata and full-text discovery: OpenAlex and Crossref for DOI-level metadata and OA locations; hand full-text acquisition to `scholarly-access`.

Record which databases exist in the current environment. If a source is not accessible, search what is accessible and mark coverage as a limitation rather than pretending comprehensive coverage.

## Screening rules

- Deduplicate by DOI first, then by normalized title plus year.
- Apply inclusion/exclusion criteria to titles, then abstracts, then full texts; keep a one-line reason for every exclusion at the full-text stage.
- Record the decision window and the language balance when a bilingual question is being reviewed.
- Distinguish existence from support: a source may exist and not support the sentence. In the matrix, mark support level explicitly.

## Evidence matrix

Produce a claim-oriented matrix when the deliverable is a review or a design:

| Claim | Source (author, year) | Design | Sample/context | Key result | Boundary | Support level |
|---|---|---|---|---|---|---|
| ... | ... | experiment/survey/text/network | ... | effect/direction | ... | direct/partial/indirect/contradicts |

The rows are claims, not papers. A paper that appears in several rows must be consistent across rows; if not, flag the conflict.

## Claim-support rules

- Verify that every citation exists (DOI or stable identifier) before using it.
- Verify that the source supports the exact sentence. Do not let a "real paper" mask an unsupported inference.
- Label synthesis statements: `evidence`, `inference`, `hypothesis`, `unverified`.
- For a new study, end with the unresolved disagreements and boundary conditions the design must address.

## Handoff

- Metadata-only needs: OpenAlex or Crossref.
- Full text or PDF acquisition: hand off to `scholarly-access` and continue with metadata while the request is pending.
- Citation export: Zotero or BibTeX after the user authorizes library writes; otherwise keep `metadata.csv` and `references.bib` in the output folder.

## Common anti-patterns

- Copying a reference list without reading or verifying support.
- Reporting "N papers found" as if it established coverage or synthesis.
- Reviewing only one database for a bilingual or cross-national question.
- Including sources that contradict the argument without recording the contradiction.
- Using Google Scholar links as the only citation evidence.

## Output shape

End with: search log, screening counts with reasons, evidence matrix, claim-support record, and a short "unresolved disagreements and boundaries" section.

See [references/search-protocol.md](references/search-protocol.md) for the log and matrix templates.
