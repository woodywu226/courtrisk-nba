# Data Governance and Provenance

## Purpose

The project uses public sports information for educational research. Public availability does not automatically mean a dataset is complete, accurate, unrestricted, or appropriate for every downstream use.

## Source register

Maintain a source register for every upstream dataset with:

| Field | Description |
|---|---|
| Source name | Dataset/provider name |
| Canonical URL | Original source location |
| Access date | UTC retrieval timestamp |
| Coverage | Seasons and date range |
| License/terms | Applicable license or terms of use |
| Fields used | Variables extracted |
| Known limitations | Missingness, reporting bias, revisions |
| Snapshot checksum | SHA-256 of the frozen raw artifact |

Do not redistribute source data unless its license and terms permit redistribution. Prefer scripts and instructions that allow users to retrieve data themselves.

## Snapshot integrity

- Preserve raw snapshots as immutable inputs.
- Store retrieval metadata and checksums.
- Make transformations deterministic where possible.
- Keep raw, processed, and derived outputs separate.
- Record parser and mapping versions.
- Never silently replace an earlier snapshot with a corrected one.

## Injury-label quality

Injury descriptions may be ambiguous, inconsistent, or incomplete. Maintain an explicit mapping from source text to normalized categories. For each mapping rule, record:
- Pattern or source value.
- Assigned category.
- Rationale.
- Whether the mapping is exact, broad, or uncertain.
- Date and reviewer of the decision.

Unknown or ambiguous strings should be surfaced for review, not silently forced into a convenient category. Keep an unmatched-value report with counts.

## Privacy and security

Do not commit credentials, access tokens, private datasets, or sensitive personal information. Use environment variables or a secret manager for credentials. Review generated reports and notebooks for accidental inclusion of local paths, tokens, or restricted data.

## Synthetic data

Synthetic snapshots must be clearly marked as synthetic in filenames, metadata, reports, and plots. Never use synthetic observations to support claims about NBA injury prevalence or model effectiveness on real players.

## Release review

Before publishing a dataset-derived result, confirm source terms, provenance, label definitions, transformation history, and the distinction between observed facts and model estimates.
