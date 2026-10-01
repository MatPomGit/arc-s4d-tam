# AGENTS.md

Instructions for AI coding/research agents editing this repository.

This file is authoritative for the whole repository unless a more specific
`AGENTS.md` exists in a subdirectory. Human instructions in the current task
always take precedence. When rules appear to conflict, preserve scientific
integrity, reproducibility, and existing public interfaces — and ask rather
than guess. When asking is not possible, state your assumption explicitly in
your output and proceed conservatively.

## 0. Meta-behavior: read before you write

Before making any change:

1. **Search first.** Do not guess the architecture or blindly overwrite files.
   Use workspace search (`rg`, file search, symbol search) to find all
   usages, callers, and related config before modifying anything.
2. **Plan before you code.** Briefly state (in your response, not necessarily
   in the diff) what you intend to change and why, and confirm it aligns with
   the current model documentation and the constraints below. If your plan touches
   a theoretical/scientific claim, name which category (§4.1) it belongs to.
3. **No unrelated churn.** Do not reformat, rename, or "clean up" files beyond
   the lines the task requires, even if you notice unrelated PEP 8 violations
   or stylistic issues. Note them separately instead of fixing them silently.
4. **Report, don't overstate.** In your final summary, distinguish what you
   verified (ran, tested, checked against source) from what you assumed or
   left unverified. Never say a test passed, a citation was checked, or a
   workflow succeeded unless you actually confirmed it.
5. **Document scientific impact.** If a change touches a scientific claim,
   a preregistered decision, or model semantics, record its rationale, evidence,
   validation and any protocol deviation. Complete authorized work autonomously;
   this file adds no human-review or manual-approval gate.

## 1. Project purpose and current architecture

`MatPomGit/arc-s4d-tam` contains the reproducible benchmark and Python research
reference for **S4D-TAM: Semantic 4D Token Attention Map for Autonomous Navigation
of Unmanned Aerial Vehicles in GNSS-Degraded Environments**.

- `src/s4dtam_benchmark/`: dataset/algorithm contracts, adapters, reference
  implementation, metrics, statistics, reporting and provenance.
- `configs/`: algorithms, datasets, experiments and research execution gates.
- `tests/`: numerical, contract and regression verification.
- `manuscript/`: canonical modular LaTeX article.
- `paper/`: historical material, not the current publication source.
- `docs/` and `mkdocs.yml`: documentation sources and site configuration.
- `tools/`: research-support and release utilities.
- `PROJECT_STATE.yaml`: machine-readable evidence phase, blockers and ordered next actions.
- `research/`: evidence/claim registries, literature log, risks, decisions, deviations and negative-result records.

The executable S4DTAMReference is not the final trained hierarchical transformer.
Synthetic smoke results validate software execution, not scientific superiority
or flight safety. Dataset conversion, baseline reproduction, trained artifacts
and confirmatory evidence require separate verification. Publication targets and
submission gates are defined in `manuscript/PUBLICATION_PATH.md` and
`manuscript/SUBMISSION_CHECKLIST.md`.

## 2. Golden rules

Every agent must follow these rules:

1. Prefer the smallest correct change.
2. Preserve falsifiability. Never modify the theory merely to make an observed
   result look supportive.
3. Never invent data, citations, DOIs, statistical results, sample sizes,
   simulation outputs, effect sizes, validation status, or implementation
   status.
4. Distinguish clearly between: established evidence, adjacent/supporting
   evidence, S4D-TAM-specific hypotheses, simulation results, human empirical
   results, and exploratory analyses.
5. Synthetic simulations are not evidence that the proposed mechanism
   is validated in real navigation or flight.
6. Do not silently turn an exploratory result into a confirmatory claim.
7. Do not inspect a locked test/holdout set and then change the model
   presented as preregistered or confirmatory.
8. Do not perform unrelated refactors while completing a focused task.
9. Do not duplicate an existing implementation, section, configuration, or
   concept when a small extension of the existing one is sufficient.
10. Keep code, scientific claims, documentation, model metadata, and generated
    outputs mutually consistent.

## 3. Repository sources of truth

- Manuscript: `manuscript/main.tex`, `manuscript/sections/`,
  `manuscript/references.bib`. Do not edit historical `paper/` drafts as the
  canonical article or assume the root bibliography is authoritative.
- Implemented behavior: `src/s4dtam_benchmark/`, `tests/`, `configs/`,
  `pyproject.toml`.
- Contracts: `docs/architecture.md`, `docs/artifact-specification.md`,
  `docs/metrics.md`, `docs/datasets.md`.
- Scientific protocol: `docs/comparison-protocol.md`,
  `docs/preregistration.md`, `docs/methodology.md`,
  `docs/reproducibility.md`.
- External comparison: `configs/experiments/offline_benchmark.yaml`.
- Internal H1-H7 study: `configs/experiments/ablation.yaml`.
- Execution gates: `docs/readiness.md`,
  `configs/readiness/dataset_baseline_matrix.yaml`,
  `configs/reproduction/confirmatory_freeze.template.yaml`.
- Validation stages: `docs/sil-protocol.md`, `docs/hil-protocol.md`,
  `docs/real-flight-protocol.md`.
- Research governance: `PROJECT_STATE.yaml`, `docs/research_workflow.md`,
  `docs/data_management_plan.md`, `docs/statistical_reporting_policy.md`,
  `research/evidence_registry.yaml`, `research/claim_ledger.yaml`.
- Contribution and safety rules: `CONTRIBUTING.md`, `SECURITY.md`.
- Build/check commands: `pyproject.toml`, `.github/workflows/ci.yml`,
  `.github/workflows/docs.yml`, `.github/workflows/manuscript.yml`.

Inspect current files and reconcile inconsistencies within the task scope.
Executable CI is authoritative for actual checks: do not weaken blocking Ruff
or Mypy steps because older README/status prose describes lint as advisory.
MkDocs output is generated from `docs/` and `mkdocs.yml`; edit sources,
not generated site output. Preserve frozen protocols and record deviations.
Before promoting any evidence class, read `PROJECT_STATE.yaml`; do not infer readiness from prose or CI status alone.

## 4. Scientific integrity and research rules

### 4.1 Claims and evidence
For each scientific claim, know which category it belongs to:

- **Established** — supported directly by cited empirical literature.
- **Adjacent evidence** — supports plausibility but does not test the
  S4D-TAM-specific hypothesis.
- **S4D-TAM hypothesis** — proposed and falsifiable, not yet established.
- **Simulation result** — evidence about mathematical/computational behavior
  only.
- **Human result** — evidence from actual human data with the stated
  population, measurement, and design.

Never blur these categories. Avoid phrases such as "the architecture guarantees safety", "the system
proves collision avoidance", or "the model is validated" unless the relevant empirical evidence
actually exists.

### 4.2 Citations
Before adding a bibliographic entry:

- verify that the paper exists;
- verify title, authors, year, journal, and DOI using a reliable source
  (publisher records, DOI metadata, PubMed, Crossref, or a trusted academic
  index);
- do not fabricate missing metadata;
- do not cite a source for a claim it does not support;
- do not cite a review as if it were the primary empirical study when the
  primary study is available and relevant.

Preserve the manuscript's citation setup and target-journal requirements.
Use IEEE for separate technical materials unless another style is requested. Keep scientific English
for the manuscript; use precise, correct Polish for requested Polish materials.
Avoid unsupported numerical precision; define units and operational measures.

If verification is incomplete, mark the item clearly as needing verification
instead of presenting it as final.

### 4.3 S4D-TAM-specific scientific and safety constraints

- Separate external system comparison from internal mechanism analysis.
  ORB-SLAM3, VINS-Mono, FAST-LIO2 and LIO-SAM belong to the external matrix,
  not the H1-H7 inferential family.
- Every internal contrast compares full with exactly one disabled mechanism.
  Preserve paired sequences, seeds, preprocessing, optimization budgets and
  unlisted settings. Do not casually rename or reinterpret H1-H7.
- Preserve H7's joint latency and mission-success non-inferiority decision.
  Read exact margins, primary endpoints, inference units and multiplicity
  correction in the protocol; do not optimize them after observing results.
- A protocol file is not evidence of external preregistration. Keep hash,
  commit and timestamp records; record later changes as amendments.
- The confirmatory-freeze template is intentionally incomplete. Do not invent
  dataset hashes, trained artifacts or baseline evidence to make it pass.
- A pinned baseline revision/container is a specification, not reproduction
  evidence. Record execution on a frozen sensor-compatible cohort.
- Validate sensor availability, calibration, frames, timestamps, alignment,
  units and ground truth before comparing methods. Disclose unequal sensing
  assumptions or privileged information.
- Preserve SequenceData and AlgorithmResult boundaries. Keep dataset
  conversion, algorithm adapters, scoring and reporting independent.
- Missing ground truth means unavailable metrics, not zero error. Keep
  collisions, timeouts, failures and aborts in the protocol-defined denominator.
- Use mission/sequence-level inference, not independent-frame pseudoreplication.
  Preserve pairing and distinguish scenario variation from repeated seeds.
- Separate train, calibration and final test use. Forecasting and online
  calibration must not consume future observations or unavailable ground truth.
- Record reference-map provenance; never use held-out test truth to construct
  a map and present it as ordinary deployment input.
- Distinguish synthetic, offline, SIL, HIL and real-flight evidence. A green
  test suite or no observed collisions does not establish safety, certification,
  embedded real-time performance or superiority of the learned model.
- Follow SECURITY.md: aircraft operation needs an independent safety controller,
  geofence, abort path and qualified operator. Keep live actuation within the
  authorized task scope; do not run hazardous hardware ablations as routine
  benchmark verification.

### 4.4 Confirmatory versus exploratory analyses
Confirmatory work must preserve: preregistered outcome, preregistered
predictor/model, temporal ordering, exclusion rules, missing-data strategy,
stopping rule, holdout definition, and primary metric. Any post hoc change
must be labeled exploratory or documented as a deviation.

### 4.5 Data leakage
Never use test/holdout observations for feature engineering, smoothing
choices, lag selection, threshold selection, interaction discovery,
hyperparameter tuning, model selection, or variable recoding motivated by test
performance. When a final temporal holdout is defined, treat it as locked.

## 5. Software engineering principles

### 5.1 KISS, YAGNI, separation of concerns
Prefer the simplest implementation that correctly solves the problem. Use
small explicit functions, obvious control flow, standard-library
functionality when adequate, and existing project abstractions when they
already solve it. Do not implement features that are not required. Use DRY to
remove meaningful duplication, but do not build opaque abstractions to
eliminate a few repeated lines — readability and scientific traceability win.

Avoid: speculative abstraction, unnecessary class hierarchies, factory
patterns for one implementation, plugin systems without a concrete need,
hidden global state or metaprogramming, and broad refactors not required by
the task.

Keep separate: scientific model definition, simulation logic, data
loading/validation, analysis, plotting/reporting, CLI handling, and generated
outputs. Functions should do one coherent job; split any function that needs a
long explanation of multiple independent responsibilities.

### 5.2 Explicitness
Prefer explicit parameters and return values over hidden global state.
Scientific code must make units, scales, shapes, timing assumptions, random
seeds, and defaults visible. Avoid unexplained magic numbers — give
domain-specific constants a name, a config entry, or a comment.

### 5.3 C++ components (performance-critical pipelines)
- Adhere to modern C++ standards (C++17/20).
- Prefer RAII and value semantics; use smart pointers for owning dynamic
  resources. Document non-owning references and avoid raw owning pointers.
- At Python/C++ bindings (e.g. `pybind11`), explicitly document memory
  ownership and lifecycle at the language boundary.

### 5.4 ROS 2 / robotics modules (when the task touches embodied or robotic
systems)
- Keep native baseline ROS/vendor dependencies behind adapter boundaries.
  Use ROS 2 conventions for new ROS 2 integrations; do not mix ROS APIs.
- Use explicit, appropriate QoS profiles for sensor streams (e.g.
  `SensorDataQoS` for vision/camera feeds).
- Define initialization, shutdown and fault behavior explicitly; use lifecycle
  nodes where the integration requires managed activation.
- Never block the event loop in callbacks — offload heavy computation (e.g.
  model inference) to separate threads or async workers.

### 5.5 GUI / display tools (when the task adds a graphical interface)
- Use **PySide6** exclusively. Do not fall back to deprecated `PyQt5` or
  `PySide2` APIs.
- Keep UI threads strictly separate from data-acquisition threads.

### 5.6 Computer vision / affective-computing pipelines (when the task
involves OpenCV, MediaPipe, eye tracking, facial expression, or other spatial
sensor data)
- Document expected tensor shapes in every function docstring that processes
  arrays/tensors (e.g. `[batch, height, width, channels]`).
- Explicitly state the expected color space (BGR vs. RGB) in docs and
  variable names. Never assume the input format.
- Explicitly validate and synchronize timestamps across modalities. Do not
  silently interpolate missing or desynchronized frames in a way that
  falsifies raw experimental results — if interpolation is required, make it
  an explicit, logged, configurable data-cleaning step.

## 6. Python requirements

All new or modified Python code must follow PEP 8
(https://peps.python.org/pep-0008/) and PEP 257
(https://peps.python.org/pep-0257/). When touching existing code, bring the
modified scope into compliance rather than copying an old style violation. Do
not suppress a linter warning solely to make CI green — fix the underlying
issue or document a genuine, narrow exception.

### 6.1 PEP 8 essentials
4 spaces per indent, no tabs; imports grouped at the top unless documented
otherwise; descriptive `snake_case` names, `PascalCase` classes, `UPPER_CASE`
constants; avoid ambiguous names (`l`, `O`, `I`); no wildcard imports; use
`pathlib.Path` for new filesystem code; use context managers for resources;
avoid mutable default arguments; catch specific exceptions, not a blanket
`except Exception` unless re-raising with context at a process boundary.

### 6.2 PEP 257 docstrings
Use triple double quotes. One-line docstrings are a concise command-style
summary ending with a period. Multi-line docstrings need: a one-line summary,
a blank line, then details — parameters (with units/shapes), return value,
side effects, exceptions, assumptions, and reproducibility implications where
relevant. Do not merely restate the signature. Standalone/CLI scripts need a
module docstring explaining purpose and invocation.

### 6.3 Type hints
Use type hints for new public APIs and nontrivial functions when they improve
clarity. Avoid complex generic typing that makes scientific code harder to
read.

### 6.4 Comments
Comments explain *why*, assumptions, and non-obvious constraints — not obvious
syntax. Keep comments synchronized with code; a stale comment is worse than
none.

### 6.5 Error handling and validation
Validate inputs at boundaries. Fail clearly when a configuration is invalid, a
required file is missing, array shapes are inconsistent, an unsupported model
is requested, or a statistical precondition is violated. Do not silently
coerce invalid scientific inputs into plausible-looking values. Do not swallow
errors with empty `except` blocks.

### 6.6 Randomness and determinism
Use explicit seeds; prefer local `numpy.random.Generator` instances over
implicit global random state; record seeds/configurations in outputs meant to
be reproducible. A stochastic result must never be represented as
deterministic.

### 6.7 Concurrency
Do not mix `asyncio` with blocking synchronous code in a way that stalls the
main thread — this is critical for real-time sensor/API pipelines. Do not
introduce unbounded or unterminated listener loops that can freeze a node or
simulation.

## 7. Dependencies and environments

Prefer existing dependencies. Before adding one, ask: can the standard library
solve this? Is it already provided by NumPy or another installed package?
Does it materially simplify a maintained implementation? Is it justified for
reproducibility and long-term maintenance? Do not add a large framework for a
small helper task.

If a dependency is added: pin/lock it per the repository's dependency policy,
update setup/reproducibility docs, ensure CI uses the same source, and explain
why it is needed. Use the repository-local virtual environment; do not rely on
globally installed packages.

## 8. Tests and verification

Behavior-changing code requires verification. At minimum: add/update a test
for bug fixes and nontrivial logic changes; run focused tests relevant to the
changed code; run the broader smoke/unit suite when practical; verify
deterministic outputs when a fixed seed is expected; test error paths for
important validation code.

Current checks follow pyproject.toml, CONTRIBUTING.md and the workflows.
From the repository root, in a local virtual environment:

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tests
python -m pytest --cov=s4dtam_benchmark --cov-report=term-missing
python -m ruff check src tests tools
python -m mypy src
```

CI tests Python 3.10 and 3.12; quality checks use 3.12. Start with relevant
checks. Metric changes require numerical tests; new adapter contracts require
an end-to-end smoke test under CONTRIBUTING.md.

For execution-path changes:

```bash
s4dtam-bench doctor
s4dtam-bench run configs/experiments/smoke.yaml
```

The smoke benchmark is synthetic. Use the documented readiness/freeze
validators for real studies; rejection of an incomplete template is expected.

For documentation changes, install requirements-docs.txt and run
`mkdocs build --strict`. For manuscript changes, from manuscript/:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Inspect undefined citations/references and layout warnings. Report missing
toolchains and unrun checks. AGENTS.md-only edits require content/path/diff
verification, not benchmark execution or new software tests.

Use the repository's `.venv` Python when available.

Do not: delete a failing test to make CI pass; weaken assertions without
scientific/technical justification; skip tests globally because one
platform-specific test is inconvenient; change expected values solely to
match a new unexpected output. For numerical tests, use tolerances justified
by the computation.

## 9. Simulation and analysis code

Simulation code must distinguish: generating parameters, observed/noisy
quantities, fitted parameters, validation data, test data, descriptive
results, and inferential results. Store scientific settings in a
configuration when practical; do not hard-code a parameter in several
scripts. Heavy sweeps must not run on every commit — keep smoke tests small
and deterministic. Do not commit large generated datasets or simulation
outputs unless explicitly required as a reasonably-sized reproducibility
artifact.

## 10. Human data and privacy

Never commit: raw identifiable participant data; names, emails, phone
numbers, IP addresses, or precise locations; consent forms containing
participant identifiers; secrets, credentials, API keys, tokens, or
passwords. Human data should use pseudonymous identifiers; cross-modal linkage
must not reveal identity. Keep raw data, derived analysis data, and public
reproducibility artifacts separate. Synthetic example data must be clearly
labeled synthetic. Never fabricate human data to fill a missing analysis.

## 11. LaTeX and manuscript editing

Treat the manuscript as scientific source code, with the same change
discipline as software. Required: keep terminology consistent across
sections; keep notation consistent with the current mathematical documentation; use
existing macros; keep equations dimensionally/conceptually consistent; verify
all `\input` paths; keep `\begin{...}`/`\end{...}` balanced; verify citation
keys exist in `manuscript/references.bib`; do not add unsupported citations; avoid
duplicating the same argument across Introduction, Discussion, and
Limitations; state uncertainty explicitly; distinguish theoretical proposal
from empirical result.

Do not weaken a falsification criterion because it makes the theory harder to
support. Do not rename constructs casually — a rename may require coordinated
changes across manuscript text, model metadata, study protocol, plots, and
documentation.

## 12. Documentation

Code is not complete until another researcher can understand how to run it.
For every user-facing or research-facing script, document purpose, inputs,
outputs, important assumptions, and an invocation example when non-obvious.
Update README/reproducibility documentation when commands or workflows
change. Prefer one authoritative description over copied documentation in
many places; use links. When a generated artifact disagrees with its source,
fix the source/generator, not the artifact.

## 13. Versioning model semantics

Changes to token lifecycle, temporal state, calibration, topology, reference
maps, risk prediction, normalized artifacts, metrics or experimental contrasts
require coordinated source/configuration/documentation updates. Preserve
compatibility or document a migration. Record commit, configuration, dataset
and artifact hashes, seeds, upstream revisions and environment provenance.

Follow existing package/release conventions. Do not invent a model-version file
or bump versions for routine documentation. Never rewrite frozen study metadata
to conceal a semantic change.

## 14. Git and pull-request discipline

Make cohesive changes. Before editing: inspect the relevant current files,
identify the authoritative source, inspect adjacent tests/configuration, and
understand whether the file is generated.

During editing: avoid unrelated formatting churn; preserve backward
compatibility unless the task explicitly changes it; do not delete material
you do not understand; do not force-push shared branches; do not rewrite
history merely to make it look cleaner.

Before merging: review the full diff; check for accidentally committed
secrets or data; verify citations and paths; run relevant tests/checks;
ensure documentation is consistent; summarize scientific and software
consequences in the PR description.

Use squash merge for a branch with many mechanical AI commits when a single
coherent change is preferable.

## 15. GitHub Actions and CI

CI must be precise and economical: use path filters when a workflow only
concerns part of the repository; do not run benchmark jobs for
manuscript-only or agent-policy edits; do not run heavy Monte Carlo sweeps on ordinary
pushes/PRs; use `concurrency` with `cancel-in-progress: true` when repeated
runs would waste resources; grant minimum required token permissions; cache
dependencies only where it provides real value; fail early on cheap
validation before expensive work; avoid duplicate workflows that test the
same thing.

Before adding a workflow trigger, ask whether a change matching that trigger
can actually affect the workflow's output. Never add an action solely because
"CI should have more checks" — every job must have a concrete failure mode it
protects against.

## 16. Common AI failure modes to avoid

Treat this list as explicit negative requirements.

### Scientific mistakes
Do not: invent citations or DOI metadata; convert a theoretical assumption
into a factual statement; use simulation success as human validation; hide a
negative/null result; redefine the outcome after seeing results; add
constructs because they make the theory sound more complete; increase model
complexity without an empirical identification plan; conflate within-person
and between-person effects; use the same data for model selection and final
evaluation; call a feasibility failure evidence against the theory; equate prediction accuracy with physical safety; describe correlation as causal without a valid
causal design.

### Coding mistakes
Do not: duplicate code instead of finding the existing implementation; create
a large class for a simple function; add a dependency for a trivial task;
silently change defaults; hard-code paths specific to one developer's
machine; use broad exception handling to hide failures; leave dead code,
unused imports, debug prints, or commented-out blocks; optimize before
identifying a bottleneck; write dense code that needs reverse engineering;
leave public functions undocumented; ignore PEP 8/257 in changed Python code;
mix `asyncio` with blocking calls that freeze the main loop; hallucinate
unterminated listener/callback loops that can crash a node or simulation;
import `PyQt5`/`PySide2` instead of `PySide6` for interface logic.

### Repository mistakes
Do not: edit generated results instead of their source; treat planned
research modules as learned and validated; create a second competing
configuration for the same experiment without a clear reason; change
manuscript notation without updating model metadata; update model metadata
without checking manuscript consistency; trigger expensive CI for irrelevant
file changes; commit environment-specific caches, virtual environments, or
large temporary outputs.

### Documentation mistakes
Do not: write documentation that describes planned functionality as
implemented; leave stale command examples; duplicate the same long
instructions in multiple files; state that a test was run when it was not;
state that a workflow passed before checking its actual conclusion.

## 17. Definition of done

A task is complete only when all applicable items are true:

- the requested behavior/content is implemented via the smallest correct
  change;
- a brief action plan was stated before modifications (§0);
- current sources of truth agree, and no fabricated data/citations exist;
- scientific claims are supported and correctly qualified by category (§4.1);
- Python changes comply with PEP 8; public modules/functions/classes have
  PEP 257 docstrings;
- ROS 2, C++, and PySide6 constraints are maintained where applicable (§5.3–
  5.6);
- sensor/multimodal pipelines explicitly handle timestamp synchronization and
  color/shape geometries where applicable (§5.6);
- relevant tests/checks pass, or unrun checks are explicitly reported as such;
- generated files were regenerated from source when necessary;
- README/reproducibility docs are updated when usage changed;
- CI triggers remain scoped and economical;
- no secrets or identifiable participant data were added;
- the final diff was reviewed for unrelated changes, and any scientific or
  preregistration-sensitive change was documented with its validation and deviations.

## 18. References for coding conventions

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/

These are mandatory conventions for Python code changed by AI agents in this
repository.
