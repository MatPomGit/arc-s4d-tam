import json
from pathlib import Path

import pytest
import yaml

from s4dtam_benchmark.tartanair_orb_pipeline import (
    PIPELINE_SCHEMA,
    STEPS,
    PipelineBlocked,
    _require_comparison_coverage,
    run_tartanair_orb_pipeline,
)


ROOT = Path(__file__).parents[1]
EXPERIMENT = ROOT / "configs/experiments/tartanair_orb_slam3_development.yaml"


def _write_config(tmp_path: Path, **updates: object) -> Path:
    payload = {
        "schema": PIPELINE_SCHEMA,
        "work_root": str(tmp_path / "work"),
        "experiment_config": str(EXPERIMENT),
        "tartanair": {
            "raw_root": str(tmp_path / "upstream"),
            "fps": 10.0,
            "link_mode": "symlink",
        },
        "orb_slam3": {
            "vocabulary": str(tmp_path / "ORBvoc.txt"),
            "command_template": "",
        },
    }
    payload.update(updates)
    path = tmp_path / "pipeline.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_pipeline_dry_run_records_expected_checkpoints(tmp_path: Path) -> None:
    config = _write_config(tmp_path)
    summary = run_tartanair_orb_pipeline(
        config,
        dry_run=True,
        until="prepare_orb_inputs",
    )
    state = json.loads(summary.state_path.read_text(encoding="utf-8"))
    expected = STEPS[: STEPS.index("prepare_orb_inputs") + 1]
    assert set(state["steps"]) == set(expected)
    assert all(state["steps"][step]["status"] == "dry_run" for step in expected)


def test_pipeline_rejects_resume_after_config_change(tmp_path: Path) -> None:
    config = _write_config(tmp_path)
    run_tartanair_orb_pipeline(config, dry_run=True, until="validate_protocol")
    payload = yaml.safe_load(config.read_text(encoding="utf-8"))
    payload["tartanair"]["fps"] = 20.0
    config.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="configuration changed"):
        run_tartanair_orb_pipeline(config, dry_run=True, until="validate_protocol")


def test_pipeline_requires_positive_explicit_fps(tmp_path: Path) -> None:
    config = _write_config(
        tmp_path,
        tartanair={"raw_root": str(tmp_path / "upstream"), "fps": 0},
    )
    with pytest.raises(ValueError, match="fps must be positive"):
        run_tartanair_orb_pipeline(config, dry_run=True, until="validate_protocol")


def test_pipeline_rejects_wrong_schema(tmp_path: Path) -> None:
    config = _write_config(tmp_path, schema="wrong/v1")
    with pytest.raises(ValueError, match="Pipeline schema"):
        run_tartanair_orb_pipeline(config, dry_run=True, until="validate_protocol")


def test_pipeline_rejects_orb_only_comparison_as_incomplete(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze"
    frozen.mkdir()
    (frozen / "sequence-list.txt").write_text("japanesealley__Hard__P003\n")

    output = tmp_path / "evaluation"
    output.mkdir()
    (output / "metrics_long.csv").write_text(
        "dataset,sequence,algorithm,metric,value\n"
        "tartanair,japanesealley__Hard__P003,orb_slam3,tracking/valid_fraction,0.8\n",
        encoding="utf-8",
    )
    (output / "failures.json").write_text(
        '[{"algorithm":"s4d_tam_reference","phase":"execution"}]\n', encoding="utf-8"
    )

    with pytest.raises(PipelineBlocked, match="Incomplete TartanAir development comparison"):
        _require_comparison_coverage(output, frozen)


def test_pipeline_requires_both_algorithms_for_each_frozen_sequence(
    tmp_path: Path,
) -> None:
    frozen = tmp_path / "freeze"
    frozen.mkdir()
    (frozen / "sequence-list.txt").write_text("P001\nP002\n")

    output = tmp_path / "evaluation"
    output.mkdir()
    metrics = output / "metrics_long.csv"
    metrics.write_text(
        "dataset,sequence,algorithm,metric,value\n"
        "tartanair,P001,s4d_tam_reference,trajectory/ate_rmse_m,0.1\n"
        "tartanair,P001,orb_slam3,trajectory/ate_rmse_m,0.2\n"
        "tartanair,P002,orb_slam3,trajectory/ate_rmse_m,0.3\n",
        encoding="utf-8",
    )
    with pytest.raises(PipelineBlocked, match="P002"):
        _require_comparison_coverage(output, frozen)

    with metrics.open("a", encoding="utf-8") as handle:
        handle.write("tartanair,P002,s4d_tam_reference,trajectory/ate_rmse_m,0.4\n")
    _require_comparison_coverage(output, frozen)


def test_pipeline_rejects_missing_comparison_metrics(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze"
    frozen.mkdir()
    (frozen / "sequence-list.txt").write_text("P003\n", encoding="utf-8")
    with pytest.raises(PipelineBlocked, match="Comparison metrics are missing"):
        _require_comparison_coverage(tmp_path / "missing-evaluation", frozen)
