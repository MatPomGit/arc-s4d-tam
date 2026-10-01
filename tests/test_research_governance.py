from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_audit_module():
    path = ROOT / "tools" / "audit_research_governance.py"
    spec = importlib.util.spec_from_file_location("audit_research_governance", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_required_governance_paths_exist() -> None:
    audit = _load_audit_module()
    missing = [rel for rel in audit.REQUIRED_PATHS if not (ROOT / rel).exists()]
    assert not missing


def test_project_state_actions_are_ordered_and_resolvable() -> None:
    state = yaml.safe_load((ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8"))
    actions = state["next_actions"]
    assert [item["order"] for item in actions] == list(range(1, len(actions) + 1))
    for item in actions:
        assert (ROOT / item["procedure"]).exists()


def test_research_registries_start_as_structured_lists() -> None:
    for rel, key in [
        ("research/claim_ledger.yaml", "claims"),
        ("research/evidence_registry.yaml", "evidence"),
        ("research/literature_search_log.yaml", "searches"),
    ]:
        payload = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
        assert isinstance(payload[key], list)


def test_risk_register_is_nonempty() -> None:
    payload = yaml.safe_load(
        (ROOT / "research/risk_register.yaml").read_text(encoding="utf-8")
    )
    assert payload["risks"]
