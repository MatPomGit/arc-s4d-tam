# Future research and publication proposals | S4D-TAM

**2026-10-09 · conditional opportunity register, not an active manuscript or research approval.** Scientific methods, protocol freezes, data/ethics provenance and claim ownership are governed by `PROJECT_STATE.yaml` and the canonical project files. Novelty has not undergone a systematic audit. Prefer simulation, lawful secondary datasets and own devices before human recruitment, without downgrading evidence quality.

## Existing principal contribution
The active P01 paper owns the S4D-TAM **full-vs-H1–H7 component ablation** under [prospective protocol](../docs/preregistration.md): offline datasets/benchmarks, SIL, HIL and conditional real flight. At present frozen real manifests, executed baseline reproduction, final learned model and confirmatory evidence are incomplete. **Do not** call the synthetic smoke a validated flight system. See [low-cost evidence strategy](../docs/LOW_COST_EVIDENCE_STRATEGY.md).

## F-S4D-01: Cross-domain uncertainty calibration and risk-aware transfer

**Working title:** *Transferability of Uncertainty Calibration Across Embodied Autonomous Systems*.
**Priority:** medium and **conditional**; joint idea with [ARC-HRI-SAFETY](https://github.com/MatPomGit/arc-hri-safety).

**Independent question:** Which estimator-level calibration properties (predictive coverage, threshold sensitivity, tail latency, risk-ranking under controlled distribution shift) are invariant between GNSS-degraded UAV perception and humanoid HRI safety when compared with domain-appropriate ground truths? What calibration methods transfer and where do they fail?

**Cheap method:** harmonized **offline** comparisons using genuinely frozen, versioned, licensable sensor/model outputs, independent simulation of matched shifts and separately held-out datasets. Human surveys not useful; physical UAV flight not required for a calibration **method** paper. Do not equate different collision-risk definitions or transfer metrics without a common formal estimand.

**Evaluation:** same calibration method class vs domain-specific alternatives; risk-coverage curves, ECE/NLL where proper, conditional coverage/decision loss, false-confidence tails and latency constraints with uncertainty. Distinguish transfer of *metrics* from actual transfer of model weights.

**Distinctness:** S4D P01 H3 already owns an internal uncertainty-calibration ablation; HRI M04 owns safety-specific online calibration. This candidate must contribute independent multi-domain generalization or a new invariant/limitation, not reprint either primary ablation result.

**GO:** frozen reproducible evidence on both domains, defensible common target, meaningful independent comparators, verified novelty versus transfer and calibration literature. **NO-GO:** no comparable label/event definition, incomplete learned artifacts, only repackaged H3/M04 plots or no cross-domain generalization.

**TODO**
- [ ] P0 Audit overlapping scientific claims across both repos and related calibration/shift literature.
- [ ] P0 Freeze comparable output schema and independent ground truth semantics with data use rights.
- [ ] P0 Complete S4D's already required real dataset/baseline/model readiness before inference.
- [ ] P1 Run cross-domain held-out benchmark and decide no-go vs independent article.
- [ ] P1 Create joint manuscript and shared evidence ledger only after verified GO decision.

## F-S4D-02: Degradation-invariant risk and semantic token persistence (watch list only)
Potential original question: when sensor failures, semantic class shifts and GNSS degradation occur jointly, can a resource-bounded token lifecycle preserve predictive utility more effectively than fixed-memory policies? **But H7 token lifecycle and H1/H3/H6 component studies already belong to P01**. Treat as supplementary stress test by default.

- [ ] P0 Finish existing P01 H1–H7 locked experiments and identify any independent phenomenon.
- [ ] P1 NO-GO unless a new algorithm and distinct cross-dataset benchmark survive novelty/overlap audit.
- [ ] P1 Do not claim flight safety from simulation or SIL alone.

## Portfolio decision
**No new dedicated manuscript folder now.** Deliver existing P01 frozen offline evidence and baseline reproduction first. Reevaluate F-S4D-01 only with real, provenance-verified cross-domain calibration outputs.
