# Contributing

S4D-TAM is a research repository. Contributions must preserve both software correctness and scientific traceability.

## Before changing code or protocols

- Search for the canonical contract or protocol before adding a parallel implementation.
- Read `PROJECT_STATE.yaml` for the current evidence phase and blockers.
- Read `AGENTS.md` for repository-wide scientific-integrity rules.
- For changes that affect claims, estimands, datasets, metrics, comparison fairness or reproducibility, record the rationale in an ADR or research decision record.
- Never edit a frozen confirmatory rule after inspecting the relevant outcomes. Use `research/deviations/` for post-freeze departures.

## Engineering rules

Keep dataset converters, algorithm adapters, metrics and reporting independent. Add numerical tests for every metric and an end-to-end smoke test for each new adapter contract. Preserve units, coordinate frames, timestamp semantics and normalized `SequenceData`/`AlgorithmResult` boundaries.

Run:

```bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest --cov=s4dtam_benchmark
python tools/audit_research_governance.py
```

## Research records

For publication-facing work:

- register immutable evidence in `research/evidence_registry.yaml`;
- map claims to evidence in `research/claim_ledger.yaml`;
- record literature-search provenance in `research/literature_search_log.yaml`;
- preserve valid null/negative findings in `research/negative_results.md`;
- record protocol deviations under `research/deviations/`;
- use the publication/research-release checklist before release.

A source pin, container reference, protocol or configuration is not by itself evidence that an experiment was reproduced.

## Data and security

Do not commit datasets without redistribution permission, model weights without provenance, credentials, private infrastructure details, restricted logs or personal data. Large publication artifacts should use an immutable external archive or release asset and be referenced by checksum.

## Pull requests

A research-facing pull request should state:

1. what changed;
2. whether scientific claims or frozen protocols are affected;
3. what tests/checks were actually run;
4. what evidence class is affected;
5. any known limitations or deviations.

Do not claim that CI success establishes scientific superiority, real-world validation or safety.
