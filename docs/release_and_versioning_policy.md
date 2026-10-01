# Release and versioning policy

## Version sources

The Python package version in `pyproject.toml` and research release metadata under `release/` must remain consistent when a formal software release is prepared.

## Semantic intent

- PATCH: backward-compatible bug fixes or documentation corrections that do not alter scientific contracts.
- MINOR: backward-compatible features, new adapters/metrics or new research tooling.
- MAJOR: incompatible public-contract or scientific-artifact format changes.

A scientific evidence snapshot may require a release/tag even when software API semantics did not materially change.

## Evidence immutability

Never retag or overwrite an evidence-bearing release. Correct errors in a new release and document the relationship in `CHANGELOG.md` and, where necessary, a protocol deviation/correction record.

## Generated artifacts

Publication tables and figures should be reproducible from registered inputs and code. Generated outputs may be excluded from development branches, but a release must provide stable access to the exact evidence package or its immutable external reference.

## Citation metadata

Update `CITATION.cff` when preferred citation, release version, DOI or author metadata changes.
