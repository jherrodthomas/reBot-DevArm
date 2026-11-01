<p align="center">
  <img src="docs/assets/rebot/banner.svg" width="100%" alt="reBot-DevArm assurance: the reBot Arm B601-DM v1.1, Seeed Studio's desktop robot arm, with its gripper raised, beside the project name and the standards it follows.">
</p>

<p align="center"><sub>The arm is upstream's own image (<code>media/v1.1_2.png</code>, Seeed Studio, CC BY-NC-SA 4.0), set into the banner by <a href="docs/assets/rebot/banner.py"><code>docs/assets/rebot/banner.py</code></a>. This fork is not affiliated with or endorsed by Seeed Studio.</sub></p>

<p align="center">
  <b>The engineering assurance record for a safety-assured fork of the reBot-DevArm desktop robot arm: machinery risk assessment under ISO 12100 and ISO 10218, a hardwired safety chain with a Performance Level target, collaborative-operation limits, cybersecurity and machine-learning safety, and a safety case published as it is built.</b>
</p>

<p align="center">
  Built on <a href="https://github.com/Seeed-Projects/reBot-DevArm">Seeed Studio's reBot-DevArm</a>. For the arm itself (assembly, bill of materials, software, tutorials) see upstream's repository and documentation.
</p>

<p align="center">
  <a href="docs/README.md">Documentation</a> &nbsp;·&nbsp;
  <a href="https://github.com/jherrodthomas/reBot-DevArm/wiki">Wiki</a> &nbsp;·&nbsp;
  <a href="#record-status">Record status</a> &nbsp;·&nbsp;
  <a href="#safety-architecture">Architecture</a> &nbsp;·&nbsp;
  <a href="#standards-and-engineering-framework">Standards</a> &nbsp;·&nbsp;
  <a href="#roadmap">Roadmap</a> &nbsp;·&nbsp;
  <a href="#known-gaps">Known gaps</a> &nbsp;·&nbsp;
  <a href="#getting-started-with-the-record">Getting started</a> &nbsp;·&nbsp;
  <a href="#contributing-to-the-record">Contributing</a> &nbsp;·&nbsp;
  <a href="https://github.com/Seeed-Projects/reBot-DevArm">Upstream reBot-DevArm</a>
</p>

<p align="center">
  <a href="https://github.com/jherrodthomas/reBot-DevArm/actions/workflows/assurance.yaml"><img src="https://github.com/jherrodthomas/reBot-DevArm/actions/workflows/assurance.yaml/badge.svg?branch=main" alt="assurance checks: records, register, process model, figures, links, tables"></a>
  <a href="https://github.com/jherrodthomas/reBot-DevArm/actions/workflows/wiki.yaml"><img src="https://github.com/jherrodthomas/reBot-DevArm/actions/workflows/wiki.yaml/badge.svg?branch=main" alt="wiki: pages checked and synced"></a>
  <a href="assurance/01-management/decisions/README.md"><img src="https://img.shields.io/badge/decisions-register-F2A33A" alt="decision register"></a>
  <a href="assurance/00-assessment/gap-assessment.md"><img src="https://img.shields.io/badge/gaps-published-FF6B5C" alt="gap assessment published"></a>
  <a href="assurance/case/README.md"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjherrodthomas%2FreBot-DevArm%2Fmain%2Fassurance%2Fcase%2Fbadge.json" alt="Living Safety Case state, from the records"></a>
</p>

## Why the record exists

The reBot Arm B601-DM is an open mechanical and actuator design with a broad software ecosystem, sold as a kit for
embodied-AI research and teaching. What it lacks, by the fork's own
[concept-phase review](assurance/00-assessment/gap-assessment.md), is the safety engineering a machine needs before it
may work with a person in reach: there is no emergency stop in the documented design, no supply disconnect or fuse,
no watchdog between the host and the actuators, no operating-mode state machine, no declared joint limits, no
reliability data, no force or pressure measurement, no validation, and the software lives outside the fork. This
fork keeps upstream's design and adds the record around it, under the standards that apply to an industrial robot.

The concept-phase engineering package the fork published first (`reBot_DevArm_Safety_Case.xlsx` and its companions
in this folder: 34 hazards, 31 safety functions, 28 gaps, 104 requirements, 127 test cases) is the **input** to
the record; its identifiers are kept and its gaps are re-stated as GAP-01 to GAP-36.

## Record status

Every work product lives under [`assurance/`](assurance/README.md), numbered in lifecycle order, with a
document-control header that says what it is, which clauses it answers to, and whether anyone has reviewed it.
Nothing is marked complete before its review, and every number below is computed from the records by
[`make_assets.py`](docs/assets/rebot/make_assets.py) and checked by CI on every pull request.

<p align="center">
  <img src="docs/assets/rebot/status.svg" width="100%" alt="Record status card generated from the records: gates passed, work products by status and by gate, gap findings by severity and area, decisions for the lead, cross-domain interfaces, confirmation measures and the hold point, with a records digest. The same values are given as text in the headline below.">
</p>

<!-- BEGIN GENERATED: record-headline (docs/assets/rebot/make_assets.py) -->

**P0 Governance** · no gate passed · 90 work products (30 draft, 60 skeleton, 0 approved) · 36 gap findings (19 high) · 3 decisions open · 1 of 11 cross-domain interfaces open · 0 of 22 confirmation measures performed · records digest `5bd183fe53cb`

<!-- END GENERATED: record-headline -->

<p align="center">
  <img src="docs/assets/rebot/lifecycle.svg" width="100%" alt="The seven phases P0 to P6, each closed by its gate G0 to G6; today is P0 governance and no gate is passed; hold points at G1 (no powered test with a person in reach before the bench chain) and G4 (no person in reach during motion before the collaborative-operation validation passes).">
</p>

| What the card guarantees | |
|---|---|
| A gate counts as passed | only when its record in [`10-safety-case/gates/`](assurance/10-safety-case/gates/README.md) says Pass; a skeleton generated from the process model is not a record |
| A work product counts as approved | only after a verification review by someone other than its author ([WP-P-05](assurance/07-supporting/WP-P-05-verification-review-procedure.md)); a confirmation measure counts only by its record under [`confirmation/`](assurance/10-safety-case/confirmation/README.md) |
| The Living Safety Case dashboard | is generated from the records in [`assurance/case/`](assurance/case/README.md): claims, evidence with review state, defeaters, actions, configurations and reviews, with a validator that refuses an accepted claim whose evidence is not available and accepted or whose defeater is open |
| The records digest | identifies the exact state of the register, the gap assessment, the decision register, the process model and the gate and confirmation records these figures describe, so two readers can confirm they saw the same state |

<p align="center">
  <img src="docs/assets/assurance/dashboard.svg" width="100%" alt="Living Safety Case dashboard generated from the assurance records: assurance state, baseline, claims with accepted evidence, evidence items accepted, open defeaters, records digest.">
</p>

<!-- BEGIN GENERATED: assurance-headline (assurance/case/tools/generate_dashboard.py) -->

**Development** · baseline `BL-001` at `206ebda` · 21 claims (0 with accepted evidence) · 20 evidence items (0 accepted) · 36 open defeaters · records digest `b6ab708350b6`

<!-- END GENERATED: assurance-headline -->

**Start here:** [assurance strategy (WP-M-01)](assurance/01-management/WP-M-01-assurance-strategy.md) · [safety plan (WP-M-02)](assurance/01-management/WP-M-02-safety-plan.md) · [process model and maps (WP-P-11)](assurance/process/README.md) · [powered-test hold point (WP-V-07)](assurance/06-validation/WP-V-07-test-operations.md) · [decision register](assurance/01-management/decisions/README.md)

> **Assurance status represents recorded engineering evidence and review state. It does not constitute certification or approval for operation with a person in reach.**

## Safety architecture

<p align="center">
  <img src="docs/assets/rebot/architecture.svg" width="100%" alt="Platform architecture. Layer 1, the host stack inherited from upstream and hardened as defence in depth: the motorbridge SDK, the ROS 2 driver and MoveIt 2, Pinocchio, authenticated command paths, session lock, a motion-imminent warning, a default-off camera, a learned policy outside every safety function. Layer 2, the controller safety layer, the last software before the motor bus: command validation, watchdog and heartbeat, the mode machine, per-joint clamps, contact detection, encoder plausibility. Layer 3, the hardwired safety chain with a PL d target: a two-channel pendant E-stop, a safety relay with monitored reset, a contactor on the 24 V motor supply, holding on power loss, an enabling device, a fuse and a lockable disconnect. A cross-cutting assurance column of draft work products applies to every layer.">
</p>

The argument is a doer-and-checker argument with one more step. The host stack proposes; the controller safety
layer checks; and a hardwired safety chain is the checker of last resort that nothing in software can override. Only
the chain carries a Performance Level target. The safety layer and the host stack are hardened so that the chain is
rarely demanded, and recorded as defence in depth.

| Layer | Role | State |
|---|---|---|
| Host stack | The SDK, the ROS 2 driver, Pinocchio, the LeRobot policies, the web UI; everything that decides where the arm goes | Inherited and upstream; hardening proposed once forked (DQ-007) |
| Controller safety layer | Validates, clamps, times out and reports every command before it reaches the motor bus; the mode machine | **Does not exist yet.** Where it runs is DQ-020 |
| Hardwired safety chain | Emergency stop, enabling, manual reset, power removal by contactor | **Does not exist yet.** Bench version first ([WP-V-07](assurance/06-validation/WP-V-07-test-operations.md), DQ-006), product version in the [SRP/CS architecture](assurance/03-system/WP-S-03-technical-safety-concept.md) |
| Safety and assurance | Risk assessment, safety functions and PLr, PL calculation, validation, cybersecurity, safety case | Draft and skeleton work products, not yet reviewed |

More in the [architecture overview](docs/architecture.md) and [WP-M-01 §6](assurance/01-management/WP-M-01-assurance-strategy.md#6-safety-architecture-argument-the-central-strategy).

## Standards and engineering framework

<p align="center">
  <img src="docs/assets/rebot/standards.svg" width="100%" alt="Standards-informed engineering framework, one question per standard. ISO 12100: what could hurt someone, and how much risk reduction does it need? ISO 10218-1 and -2: which safety functions must a robot arm have, and how is it integrated? ISO/TS 15066: what may the arm do when a person is in reach? ISO 13849-1 and -2: how reliable must the control system be, and how is that shown? EN 60204-1 and ISO 13850: is the electrical installation safe, and does the E-stop work? ISO 13854, 13855 and 13857: where may a hand or a person be relative to the joints? IEC 62443: what if someone attacks it? ISO/IEC TR 5469: how far can a learned policy be trusted? UL 4600 and the Machinery Regulation: is the whole argument convincing, and what does the law require? Aligned practices, not a compliance claim.">
</p>

The arm is machinery and an industrial robot, so the frame is the machinery set, applied with one method: one hazard
log, one requirements database, generated figures, a safety case with its defeaters published. Work products are
structured after these standards and cite their clauses; **no compliance is claimed**, because no assessment has been
performed and no standard is held. [WP-M-01 §4](assurance/01-management/WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used)
explains how each standard is used and where it is tailored; the wiki's
[How we use each standard](https://github.com/jherrodthomas/reBot-DevArm/wiki/How-we-use-each-standard) is the
plain-language version.

| Topic | Standard | Main work products |
|---|---|---|
| Risk assessment and reduction | ISO 12100:2010 | [Item definition](assurance/02-concept/WP-C-01-item-definition.md) · [Risk assessment](assurance/02-concept/WP-C-03-risk-assessment.md) · [Risk reduction concept](assurance/02-concept/WP-C-05-risk-reduction-concept.md) |
| Industrial robots and robot applications | ISO 10218-1:2025, ISO 10218-2:2025 | [Safety functions and required PL](assurance/02-concept/WP-C-04-safety-functions-and-plr.md) · [Operating envelopes](assurance/02-concept/WP-C-02-operating-environment-and-tasks.md) |
| Collaborative operation | ISO/TS 15066:2016 | [Human-robot interaction](assurance/02-concept/WP-C-06-human-robot-interaction-and-misuse.md) · [Collaborative operation validation](assurance/06-validation/WP-V-03-collaborative-operation-validation.md) |
| Safety-related parts of control systems | ISO 13849-1:2023, ISO 13849-2:2012 | [SRP/CS architecture](assurance/03-system/WP-S-03-technical-safety-concept.md) · [PL calculation](assurance/04-hardware/WP-H-04-reliability-data-and-pl-calculation.md) · [Safety validation](assurance/06-validation/WP-V-01-safety-validation.md) |
| Where ISO 13849 runs out | IEC 62061:2021, IEC 61508:2010 | [Software safety requirements](assurance/05-software/WP-W-02-software-safety-requirements.md) · [Confirmation measures](assurance/01-management/WP-M-06-confirmation-measures-plan.md) |
| Electrical equipment, emergency stop, gaps and distances | EN 60204-1:2018, ISO 13850:2015, ISO 13854:2019, ISO 13855:2024, ISO 13857:2019 | [Electrical safety](assurance/04-hardware/WP-H-05-electrical-safety.md) · [Mechanical analysis](assurance/04-hardware/WP-H-08-mechanical-analysis.md) · [Stopping and separation budget](assurance/03-system/WP-S-04-response-time-and-stopping-budget.md) |
| Cybersecurity | IEC 62443-4-1:2018, IEC 62443-4-2:2019 | [Threat and risk assessment](assurance/02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md) · [Cybersecurity plan](assurance/01-management/WP-M-08-cybersecurity-plan.md) |
| Machine learning in safety functions | ISO/IEC TR 5469:2024 | [ML component definition](assurance/02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md) · [ML safety plan](assurance/01-management/WP-M-09-ml-safety-plan.md) |
| Regulatory | Regulation (EU) 2023/1230 (Machinery), Regulation (EU) 2024/1689 (AI Act) | [Regulatory conformity strategy](assurance/01-management/WP-M-13-regulatory-conformity-strategy.md) |
| Safety case structure | UL 4600 principles | [Safety case](assurance/10-safety-case/WP-K-01-safety-case.md) |

<p align="center">
  <img src="docs/assets/rebot/standards-map.svg" width="100%" alt="Standards map: fifteen standards and practices down the side, the seven gates across, each cell the number of work products needed by that gate whose register row cites the standard. Counted from the work product register.">
</p>

| Supporting practice | Where it is applied |
|---|---|
| Integrated process model | [WP-P-11](assurance/process/README.md): activities, lanes, cross-domain interfaces and gates as data; generated swimlane maps and gate skeletons |
| Process capability | [ASPICE self-assessment, WP-M-12](assurance/01-management/WP-M-12-process-capability-baseline.md) |
| Performance limits of sensing and the learned policy | ISO 21448 used as a method, not a standard, in the [insufficiency analysis](assurance/02-concept/WP-C-10-functional-insufficiency-analysis.md) |
| Safety analysis | [FMEA](assurance/08-analyses/WP-A-01-system-fmea.md) · [FTA](assurance/08-analyses/WP-A-02-fault-tree-analysis.md) · [CCF](assurance/08-analyses/WP-A-03-common-cause-failure-analysis.md) · [STPA](assurance/08-analyses/WP-A-04-stpa.md) · [Independence of the chain](assurance/08-analyses/WP-A-05-independence-of-the-safety-chain.md) |
| Independent review | [Confirmation measures plan](assurance/01-management/WP-M-06-confirmation-measures-plan.md) · [Verification and review procedure](assurance/07-supporting/WP-P-05-verification-review-procedure.md) |
| Decisions | [Decision register](assurance/01-management/decisions/README.md): every question for the project lead, self-contained, in batches of ten |

## Roadmap

<p align="center">
  <img src="docs/assets/rebot/roadmap.svg" width="100%" alt="Roadmap. Phase 1 Foundation, active: governance and safety plan, baseline gap assessment, work product register, integrated process model, decision register. Phase 2 Safety engineering, active: item, envelopes and risk assessment, safety functions and required PL, the collaborative-operation decision, cybersecurity threat assessment, the powered-test hold point. Phase 3 Build and verify, planned: bench safety chain, software fork and safety layer, chain design and PL calculation, stopping, holding and E-stop tests, fault injection. Phase 4 Validate and release, planned: validation on the arm, independent assessment, technical documentation, declaration of conformity draft, field monitoring.">
</p>

Status is taken from what exists in the repository. "Draft" means written but not reviewed; "skeleton" means the
structure and clause map exist and the content is still to be written.

| Phase | Work | Status |
|---|---|---|
| **1 · Foundation** | [Assurance strategy](assurance/01-management/WP-M-01-assurance-strategy.md), [safety plan](assurance/01-management/WP-M-02-safety-plan.md), [confirmation measures](assurance/01-management/WP-M-06-confirmation-measures-plan.md), [regulatory strategy](assurance/01-management/WP-M-13-regulatory-conformity-strategy.md) | Draft |
| | [Baseline gap assessment](assurance/00-assessment/gap-assessment.md) | Draft |
| | [Work product register](assurance/01-management/WP-M-00-work-product-register.md), [process model and maps](assurance/process/README.md), [decision register](assurance/01-management/decisions/README.md) | Draft; checked by CI |
| | [Living Safety Case records and dashboard](assurance/case/README.md) | Draft: records at BL-001, validated and drawn by CI |
| **2 · Safety engineering** | [Item definition](assurance/02-concept/WP-C-01-item-definition.md), [operating envelopes](assurance/02-concept/WP-C-02-operating-environment-and-tasks.md), [risk assessment](assurance/02-concept/WP-C-03-risk-assessment.md), [safety functions and PLr](assurance/02-concept/WP-C-04-safety-functions-and-plr.md), [interaction and misuse](assurance/02-concept/WP-C-06-human-robot-interaction-and-misuse.md) | Draft, from the concept-phase package |
| | [Risk reduction concept](assurance/02-concept/WP-C-05-risk-reduction-concept.md), [insufficiency analysis](assurance/02-concept/WP-C-10-functional-insufficiency-analysis.md), [cybersecurity threat assessment](assurance/02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md), [ML component definition](assurance/02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md) | Skeleton |
| | [Powered-test hold point](assurance/06-validation/WP-V-07-test-operations.md) | Draft; the bench chain waits on the lead (DQ-006) |
| **3 · Build and verify** | Bench safety chain, software fork and safety layer, [chain architecture](assurance/03-system/WP-S-03-technical-safety-concept.md) and [PL calculation](assurance/04-hardware/WP-H-04-reliability-data-and-pl-calculation.md), [stopping and holding tests](assurance/06-validation/WP-V-02-stopping-performance-and-holding-tests.md), [fault injection](assurance/06-validation/WP-V-05-fault-injection.md) | Planned |
| **4 · Validate and release** | [Safety validation](assurance/06-validation/WP-V-01-safety-validation.md), [assessment](assurance/10-safety-case/WP-K-04-functional-safety-assessment.md), [technical documentation](assurance/10-safety-case/WP-K-02-technical-documentation-index.md), [release record](assurance/10-safety-case/WP-K-06-release-record.md), [field monitoring](assurance/09-production-operation/WP-O-04-field-monitoring.md) | Planned |

## Known gaps

The project publishes its own counter-evidence. The [baseline gap assessment](assurance/00-assessment/gap-assessment.md)
reviewed the hardware record and the concept-phase package, finding by finding, against the standards above. The
findings that shape everything:

| | Finding | Closes through |
|---|---|---|
| GAP-08 | No emergency stop exists in the documented design; the only stop is a software command on the motor bus | The bench chain before any powered test with a person in reach ([WP-V-07](assurance/06-validation/WP-V-07-test-operations.md), DQ-006); the hardwired chain ([WP-S-03](assurance/03-system/WP-S-03-technical-safety-concept.md)) |
| GAP-09, GAP-11 | No supply disconnect or fuse; an open-frame mains supply with exposed terminals | Electrical safety ([WP-H-05](assurance/04-hardware/WP-H-05-electrical-safety.md)) |
| GAP-16, GAP-17, GAP-18 | The software is outside the fork; no mode machine; a lost connection holds the last command | Fork the software (DQ-007) and build the controller safety layer ([WP-W-03](assurance/05-software/WP-W-03-software-architecture.md)) |
| GAP-19, GAP-02, GAP-03 | No declared joint limits, end-stops, mass or fixing | Mechanical analysis ([WP-H-08](assurance/04-hardware/WP-H-08-mechanical-analysis.md)) and the parameter sets ([WP-W-09](assurance/05-software/WP-W-09-safety-parameters-and-configuration-data.md)) |
| GAP-28, GAP-06 | No force or pressure measurement; no separation-distance plan | The collaborative-operation decision (DQ-005) and its validation ([WP-V-03](assurance/06-validation/WP-V-03-collaborative-operation-validation.md)) |
| GAP-22, GAP-23 | Anyone with the CAN adapter or the network can move the arm | Cybersecurity requirements and architecture ([WP-C-08](assurance/02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md), [WP-S-07](assurance/03-system/WP-S-07-cybersecurity-architecture.md)) |
| GAP-14, GAP-31 | No reliability data, no validation of any safety function | Supplier data (DQ-019), the PL calculation ([WP-H-04](assurance/04-hardware/WP-H-04-reliability-data-and-pl-calculation.md)) and the validation plan ([WP-V-01](assurance/06-validation/WP-V-01-safety-validation.md)) |

Every finding becomes a defeater against a claim in the safety case and stays open until the work product that
closes it is reviewed.

## Hazard scenes on the real CAD

<p align="center">
  <img src="assurance/sim/figures/sim-hero-dashboards.jpg" width="100%" alt="Three hazard scenes rendered on upstream's CAD, each cropped to its 3D view with a red band reading synthetic, no evidence credit: the elbow closing on the operator's fingers while hand-guiding in TEACH, the gripper coming down on a hand against the bench, and the base sweeping the gripper past a bystander's head during RUN.">
</p>

Fifteen hazards of the risk assessment are drawn on upstream's v1.1 CAD, posed by a joint rig at the moment the hazard
occurs, with a person where the interaction analysis puts them and the link gap or distance against the ISO 13854
minimum gaps beside the package's rating and the stop functions that do not exist yet
([WP-P-12](assurance/sim/README.md), [gallery](assurance/sim/blender/dashboards/README.md)). They are pictures for
review: synthetic, no evidence credit, and nothing in the safety case rests on them.

## Getting started with the record

Only Python 3 is needed (PyYAML for the decision register):

```bash
git clone https://github.com/jherrodthomas/reBot-DevArm.git
cd reBot-DevArm
python3 assurance/01-management/decisions/check_decisions.py     # the questions for the lead
python3 assurance/process/tools/process_model.py --check         # process maps and gate skeletons current
python3 assurance/tools/folder_index.py --check                  # folder indexes match the register
python3 docs/assets/rebot/make_assets.py --check                 # README figures match their generator
python3 tools/wiki/build_wiki.py                                 # the wiki pages check clean
```

**On an arm:** the fork publishes no software build and changes no hardware yet. No arm is powered with a person
inside its 650 mm reach under the fork's control until the conditions of
[WP-V-07](assurance/06-validation/WP-V-07-test-operations.md) hold: a fused and switched 24 V supply, a dual-channel
emergency stop through a safety relay, the arm fixtured, pinned software with the watchdog on, and nobody but the
operator at the bench.

## Contributing to the record

Contributions are welcome in machinery and robot safety, safety-related control systems, electrical and mechanical
engineering, embedded and ROS 2 software, cybersecurity, verification, documentation and review. Safety-relevant
changes need a rationale, an impact analysis and appropriate verification.

| | |
|---|---|
| [Contributing](CONTRIBUTING.md) | Rules for safety-relevant changes and assurance records |
| [Issues](https://github.com/jherrodthomas/reBot-DevArm/issues) · [Pull requests](https://github.com/jherrodthomas/reBot-DevArm/pulls) | Problem reports, safety concerns, reviews of the analyses; pull requests target `main` |
| [Security policy](SECURITY.md) | Private vulnerability reporting |
| [Wiki](https://github.com/jherrodthomas/reBot-DevArm/wiki) | Orientation: processes, process maps, how each standard is used, glossary, how decisions are made. Kept in [`wiki/`](wiki/README.md) and mirrored on merge |
| [Upstream reBot-DevArm](https://github.com/Seeed-Projects/reBot-DevArm) | The arm this fork is derived from |

## The concept-phase engineering package

The package of 2026-05-04 stays at the repository root as the record's input; the files are not edited.

| File | Purpose |
|---|---|
| `reBot_DevArm_Safety_Case.xlsx` | 15-tab preliminary safety case (ISO 12100 / 10218 / TS 15066 / 13849 / 9001 / 60204-1): 34 hazards, 31 safety functions, 28 gaps |
| `reBot_DevArm_Safety_Case_Report.docx` | Narrative safety case |
| `reBot_DevArm_Safety_Case_Summary.pdf` | 2-page executive summary |
| `reBot_DevArm_DFMEA.xlsx` | AIAG-VDA 2019 DFMEA: 27 failure modes (11 high action priority) |
| `reBot_DevArm_Requirements.xlsx` | SyRS, SRS and HwRS: 104 requirements, traced |
| `reBot_DevArm_Architecture.docx` | 5 architectural views with embedded diagrams |
| `reBot_DevArm_TestPlan.xlsx` | V-model test plan: 127 cases, ISO 13849-2 and TS 15066 V&V matrices |
| `reBot_DevArm_Trace_Memo.docx` | Cross-package traceability verification |
| `reBot_DevArm_Engineering_Bundle.pdf` | Single-file stakeholder bundle |
| `01_hero_banner.png` … `05_mode_fsm.png` | The package's banner, KPI, envelope and architecture figures |

## Maintainer and upstream attribution

**Jherrod Thomas** maintains this record as an open engineering initiative: a public demonstration of
safety-lifecycle development, systems engineering and assurance practice on a real robot arm.

reBot-DevArm is designed and published by [Seeed Studio](https://github.com/Seeed-Projects/reBot-DevArm) under
CC BY-NC-SA 4.0. This fork keeps that licence for the whole repository, including the record, and is non-commercial;
`hardware/` is upstream's record, merged and never edited here. The fork is an independent project and is not
affiliated with or endorsed by Seeed Studio; it carries no reBot trademark claim.

Open-source licensing does not establish machinery safety certification, CE marking, or suitability for operation
with a person in reach.
