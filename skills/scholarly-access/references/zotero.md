# Zotero and local library archiving

## When to use this reference

Use it when the user asks to save resolved papers into a reference library, Zotero collection, or local research corpus.

## Preconditions

- Zotero writes are external mutations. They require explicit user authority for the target library and collection.
- No Zotero connection is required for basic archiving: produce `metadata.csv` and `references.bib` in the project output folder and report their paths.

## Archiving order

1. Normalize metadata (DOI, title, authors, year, venue, journal issue, pages, URL, access date).
2. Deduplicate by DOI, then normalized title, before adding items.
3. Download and validate the PDF (see resolver policy) before import.
4. Rename files consistently: `FirstAuthorLastName_Year_ShortTitle.pdf` with safe filename characters.
5. Create or reuse the collection the user requested, e.g. `Zotero/Multi-Agent Social Influence/Theory`.
6. Add items with tags that match the study's constructs or phases so the library stays queryable.
7. Verify the imported items: item count, PDF attachment, DOI match, and tags.

## Fallback when Zotero is unavailable

Write a stable local folder:

```text
outputs/literature/
├── metadata.csv       # one row per paper with all normalized fields
├── references.bib     # BibTeX entries usable by LaTeX or Word
└── pdfs/              # validated full texts named Author_Year_ShortTitle.pdf
```

## Anti-patterns

- Importing a PDF that has not been validated against the citation.
- Duplicating items because the same paper was resolved through two layers.
- Storing collection paths, credentials, or session state inside the Skill repository.
- Renaming files with Unicode separators or characters that break cross-platform tools.
