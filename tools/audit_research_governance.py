#!/usr/bin/env python3
"""Static audit of S4D-TAM research-governance artifacts.

This audit verifies repository structure and machine-readable consistency.
It does not claim that scientific hypotheses, dataset conversions, baselines,
SIL/HIL validation, or physical validation have succeeded.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "PROJECT_STATE.yaml",
    "TODO.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "docs/adr/README.md",
    "docs/adr/TEMPLATE.md",
    "docs/data_management_plan.md",
    "docs/research_workflow.md",
    "docs/statistical_reporting_policy.md",
    "docs/authorship_contributions.md",
    "docs/experiment_naming_and_ids.md",
    "docs/publication_release_checklist.md",
    "docs/literature_review_policy.md",
    "docs/project_assumptions.md",
    "docs/terminology_glossary.md",
    "docs/release_and_versioning_policy.md",
    "docs/responsible_use_and_safety_governance.md",
    "docs/preregistration.md",
    "docs/reproducibility.md",
    "docs/readiness.md",
    "research/README.md",
    "research/claim_ledger.yaml",
    "research/evidence_registry.yaml",
    "research/literature_search_log.yaml",
    "research/risk_register.yaml",
    "research/negative_results.md",
    "research/decisions/README.md",
    "research/deviations/README.md",
    "configs/reproduction/confirmatory_freeze.template.yaml",
    "configs/readiness/dataset_baseline_matrix.yaml",
]


def load_yaml(path: str) -> dict:
    data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    return data or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"missing required path: {rel}")

    yaml_paths = [
        "PROJECT_STATE.yaml",
        "research/claim_ledger.yaml",
        "research/evidence_registry.yaml",
        "research/literature_search_log.yaml",
        "research/risk_register.yaml",
    ]
    docs: dict[str, dict] = {}
    for rel in yaml_paths:
        if (ROOT / rel).exists():
            try:
                docs[rel] = load_yaml(rel)
            except Exception as exc:  # pragma: no cover - diagnostic branch
                failures.append(f"invalid YAML {rel}: {exc}")

    state = docs.get("PROJECT_STATE.yaml", {})
    actions = state.get("next_actions", [])
    if not actions:
        failures.append("PROJECT_STATE.yaml: next_actions is empty")
    else:
        orders = [item.get("order") for item in actions]
        expected = list(range(1, len(actions) + 1))
        if orders != expected:
            failures.append(
                f"PROJECT_STATE.yaml: next_actions order must be contiguous from 1; got {orders}"
            )
        for item in actions:
            task_id = item.get("id", "<missing-id>")
            for field in (
                "id",
                "action",
                "procedure",
                "prerequisites",
                "expected_outputs",
                "done_when",
            ):
                if field not in item or item[field] in (None, "", []):
                    failures.append(f"PROJECT_STATE.yaml: {task_id} missing {field}")
            procedure = item.get("procedure")
            if procedure and not (ROOT / procedure).exists():
                failures.append(
                    f"PROJECT_STATE.yaml: {task_id} procedure missing: {procedure}"
                )

    claims = docs.get("research/claim_ledger.yaml", {}).get("claims")
    if not isinstance(claims, list):
        failures.append("research/claim_ledger.yaml: claims must be a list")

    evidence = docs.get("research/evidence_registry.yaml", {}).get("evidence")
    if not isinstance(evidence, list):
        failures.append("research/evidence_registry.yaml: evidence must be a list")

    searches = docs.get("research/literature_search_log.yaml", {}).get("searches")
    if not isinstance(searches, list):
        failures.append("research/literature_search_log.yaml: searches must be a list")

    risks = docs.get("research/risk_register.yaml", {}).get("risks")
    if not isinstance(risks, list) or not risks:
        failures.append("research/risk_register.yaml: risks must be a non-empty list")

    result = {
        "repository_governance_ready": not failures,
        "research_phase": state.get("research_phase"),
        "scientific_evidence_ready": False,
        "note": (
            "Static governance readiness is not scientific validation. "
            "PROJECT_STATE.yaml and frozen protocols remain authoritative."
        ),
        "failures": failures,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"repository_governance_ready={str(not failures).lower()}")
        print(f"research_phase={result['research_phase']}")
        if failures:
            for failure in failures:
                print(f"- {failure}")
        else:
            print("static research-governance audit: PASS")
            print(result["note"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
