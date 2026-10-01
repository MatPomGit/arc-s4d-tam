# Research records

This directory contains research-governance records that complement, but do not replace, the canonical protocol and implementation sources.

Use the following records:

- `claim_ledger.yaml`: manuscript/research claim -> evidence mapping;
- `evidence_registry.yaml`: immutable reportable evidence bundles and hashes;
- `literature_search_log.yaml`: reproducible literature-search records;
- `risk_register.yaml`: scientific, reproducibility, safety and release risks;
- `negative_results.md`: valid null/negative results worth preserving;
- `decisions/`: consequential scientific/architecture decision records;
- `deviations/`: deviations from frozen or preregistered procedures.

Rules:

1. Never invent evidence to populate a registry.
2. A configuration, pin or protocol is not execution evidence.
3. Every reportable result should be traceable to source commit, configuration, data manifest, environment and analysis code.
4. Every post-freeze protocol change must be recorded as a deviation and classified as confirmatory-impacting or exploratory.
5. Negative results remain part of the record and must not be silently discarded because they do not support the hypothesis.
