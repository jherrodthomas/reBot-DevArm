# WP-P-01 Configuration management plan

| Field | Value |
|---|---|
| Work product | WP-P-01 Configuration management plan (safety-relevant file list, baselines across the fork repositories) |
| Standard reference | SRP/CS: 61508-1 §6.2.3; 13849-1 §12; IEC 62443: 62443-4-1 SM-6, SM-7; ASPICE: SUP.8. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: configuration items, safety-relevant file list, baselines and cross-repository pins; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

This plan says what is under configuration control in the reBot-DevArm fork, how each item is identified, which files
are safety-relevant, and how a baseline is cut across this repository and the software repositories the lead decided
to fork (DQ-007, answered A). Change control is [WP-P-02](WP-P-02-change-management.md), document rules are
[WP-P-04](WP-P-04-documentation-management.md), and releases built on a baseline are
[WP-P-10](WP-P-10-release-management.md).

The configuration and change manager is Jherrod Thomas, acting ([WP-M-02 §3.1](../01-management/WP-M-02-safety-plan.md#31-role-assignments)).
Configuration control means: every item has an identifier and a location; every change to it goes through a pull
request into `main`; and a baseline names one commit of every repository that together make one configuration.

## 2. Configuration items

| Item | What it is | Where | Identified by | Controlled how |
|---|---|---|---|---|
| Assurance record | Work products, the Living Safety Case records, the decision register, trace items, process model, wiki sources, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CLAUDE.md` | This repository (`jherrodthomas/reBot-DevArm`) | Commit SHA; version in each work product header | Pull request into `main`, merge commit ([WP-P-02](WP-P-02-change-management.md)) |
| Hardware record | Upstream's BOM, STEP files, limit blocks, performance test | `hardware/` in this repository | Upstream commit merged, and the merge commit | Merged from upstream only, never edited (§2.1) |
| Concept-phase package | `reBot_DevArm_*.xlsx`, `.docx`, `.pdf` at the repository root | This repository | Commit SHA (unchanged since BL-001) | Input to the record; never edited |
| Software forks | The SDK and the control and digital-twin code that moves or models the arm (DQ-007) | Forks under `jherrodthomas` (§4.3) | Fork URL and commit SHA | Pull request in the fork; pinned per baseline |
| Controller safety layer | Firmware of the dedicated controller between host and bus (DQ-020, answered A) | `rebot-safety-controller` (to be created) | Repository and commit SHA | As a software fork; class SR-A |
| Safety parameter sets | Joint, torque and speed limits, timings, variant table ([WP-W-09](../05-software/WP-W-09-safety-parameters-and-configuration-data.md)) | `assurance/05-software/parameters/` and the controller's `config/` (neither exists yet) | Commit SHA and a parameter-set version | Class SR-A |
| Policy checkpoints | Learned-policy weights the host may run ([WP-W-10](../05-software/WP-W-10-ml-engineering.md)) | Not stored yet | SHA-256 of the file (proposed) | To be defined (OI-8) |
| Arm configurations | CFG-001 (B601-DM v1.1), CFG-002 (B601-RS) | [`case/configurations/`](../case/configurations/cfg-001-b601-dm.yaml) | `CFG-nnn` | Records in this repository |
| Actuator firmware | Damiao (and RobStride) closed firmware | On the actuators | Version read from the actuator, recorded per configuration | Not controlled by the fork; recorded only |
| Tooling | CI workflows, generators, checkers, their Python dependencies | `.github/`, `assurance/**/tools/`, `tools/`, `docs/assets/rebot/*.py` | Commit SHA; action and package versions | Class SR-T; qualification in [WP-P-07](WP-P-07-tool-classification-qualification.md) |
| Bench as built | The bench safety chain and fixture ([WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md)) | Physical | As-built record with part numbers (to be defined) | Change by impact-analysed change ([WP-M-02 §4.1](../01-management/WP-M-02-safety-plan.md#41-early-implementation-of-at-risk-work)) |

Tooling pins today: CI uses Python 3.12 and installs `pyyaml`, `numpy` and `pillow` without version pins, and refers
to GitHub actions by major version (`actions/checkout@v4`, `actions/setup-python@v5`), not by commit
([`assurance.yaml`](../../.github/workflows/assurance.yaml)). A rebuild can therefore run different tool versions (OI-5).

### 2.1 Upstream content in this repository

`hardware/` is Seeed Studio's record (`Seeed-Projects/reBot-DevArm`, CC BY-NC-SA 4.0). It changes only by merging
upstream into a branch and opening a pull request; the merge is class SR-Q (`hardware/**`) and gets an impact record
naming what changed in the BOM, the STEP files and the limit blocks. `README.md` is the fork's own page: on an upstream
merge the fork's version is kept and upstream's changes to it are read for anything the record must reflect. The
upstream README translations (`README_zh.md` and the others) are kept as upstream ships them.

## 3. Safety-relevant file list

[`safety-relevant-paths.txt`](safety-relevant-paths.txt) is the authoritative, machine-readable list. Each line is
`<class> <glob>`; globs are relative to the fork workspace (this repository with the software checkouts beside it);
`**` matches any number of path segments; when several patterns match, the longest wins; a file that matches none is
NSR. The list changes only through a change request ([WP-P-02](WP-P-02-change-management.md)), handled as SR-Q
whatever class its own path has.

| Class | Covers (as the list stands) | What a change requires |
|---|---|---|
| SR-A | The safety-chain design files (`assurance/04-hardware/chain/**`), the controller safety layer source and config, a host-side safety layer if any, the WP-W-09 parameter sets. None of these paths exists yet | Impact record, verification evidence, two human approvals (WP-P-02 §2) |
| SR-Q | The forked SDK (`rebot-motorbridge/**`), the forked ROS 2 driver (`rebot-ros2/**`), `hardware/**` | Impact record, verification, review |
| SR-T | `.github/**`, the generators and checkers, the forks' CI and dependency files (`pyproject.toml`, `package.xml`) | Impact statement in the pull request; impact record if a pin or a check that evidence relies on changes |
| NSR | Everything else, including work product text | Pull request with a safety-impact statement ("none" with a reason is valid) |

The list predates the choice of repositories in §4.3: it names `rebot-motorbridge/` and `rebot-ros2/`, while the forks
being created are `motorbridge`, `reBotArm_control_py` and `ReBot_Arm_DigitalTwin_DM`. The checkout names and the
entries for the last two are to be settled by a change request once the forks exist (OI-2). No tool yet compares a
pull request's changed files with the list; the class is the author's statement in the pull request template (WP-P-02
OI-2).

## 4. Baselines

### 4.1 Identification

A baseline is `BL-nnn`, recorded in [`case/baselines/baselines.yaml`](../case/baselines/baselines.yaml) with
`lifecycle_status` `under-development`, `frozen` or `superseded`, a `tag` and the `source_revision` of this
repository. Every work product's header names the baseline its content refers to. Numbers are never reused.

### 4.2 Cutting and freezing a baseline

1. The safety manager decides to cut a baseline (at a gate review or before a release under WP-P-10).
2. `main` of every repository in the baseline has CI passing at the chosen commit.
3. The pin table (§4.3) is filled: one fork URL and full commit SHA per repository, plus the parameter-set version,
   the policy checkpoint hashes and the actuator firmware versions of the configuration.
4. An annotated tag `BL-nnn` is pushed on the chosen commit of this repository and of every pinned fork.
5. The baseline record is set to `frozen` with its tag, in a pull request. A frozen baseline is never moved; later
   changes go into the next one, and the previous frozen baseline becomes `superseded`.

No baseline has been frozen and no tag exists in this repository.

### 4.3 BL-001 and the starting pins of the software

BL-001 is commit `206ebda` (2026-05-03): upstream's hardware record v1.1 merged, plus the concept-phase package, with
no fork changes to hardware or software. It is `under-development` and untagged. Its record says the software was
upstream and unpinned; what ran on the arm at that date was never recorded.

Under DQ-007 A the software that moves the arm is forked and pinned. The lead is creating the forks; none is
confirmed yet. The starting pins are the upstream heads read on 2026-11-01; they join BL-001's record once each fork
exists and its `main` is at that commit:

| Repository | Upstream | Fork (expected) | Licence as found | Starting pin | State |
|---|---|---|---|---|---|
| motorbridge SDK | `motorbridge/motorbridge` | `jherrodthomas/motorbridge` | MIT | `d5700bcd5b7f9355dd2012488d463c3bac982259` | Unconfirmed; the only fork to be modified at first |
| Arm control (Python) | `Seeed-Projects/reBotArm_control_py` | `jherrodthomas/reBotArm_control_py` | None stated | `d4f3591bc0183de03f3ae8651298db0269aadfdd` | Unconfirmed; not modified; reuse rights unclear (OI-4) |
| Digital twin | `Yang-Ci/ReBot_Arm_DigitalTwin_DM` | `jherrodthomas/ReBot_Arm_DigitalTwin_DM` | Ambiguous: CERN-OHL-W file, Apache-2.0 in README | `7456d8bc3cc6d9c470680988543f90bc8f3b03b0` | Unconfirmed; not modified; licence to settle (OI-4) |

A pin is always a full commit SHA in the fork, never a branch name. When a fork takes upstream changes, the merge is
an SR-Q change in that fork and the new commit is pinned only in a later baseline. The baseline schema has no field
for pins yet, so the table lives in the record's description until one is added (OI-3).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Confirm the three forks under `jherrodthomas`, check each fork's `main` against its starting pin, and write the pins into BL-001's record | Configuration and change manager | G0 |
| OI-2 | Align `safety-relevant-paths.txt` with the forks chosen (checkout names; entries for `reBotArm_control_py` and the digital twin; the `rebot-ros2/` entry) by change request | Configuration and change manager | G0 |
| OI-3 | Add a pin list to the baseline record schema so `validate.py` checks that every baseline names one commit per repository | Safety manager | G1 |
| OI-4 | Settle the reuse terms of `reBotArm_control_py` (no licence) and the digital twin (two licences) with their owners before any change to either ([WP-M-10](../01-management/WP-M-10-upstream-and-supplier-management.md)) | Project maintainer | Before the first change to either fork |
| OI-5 | Pin CI dependencies: package versions for `pip install`, actions by commit SHA | Configuration and change manager | G1 |
| OI-6 | Turn on branch protection for `main` (pull request required, CI required, merge commits only) and add a CODEOWNERS file; neither is visible in the repository | Configuration and change manager | G0 |
| OI-7 | Put to the lead whether the self-approval rule of DQ-010 also stands in for the second human approval an SR-A change needs; no SR-A path exists yet | Safety manager | Before the first SR-A change |
| OI-8 | Define how policy checkpoints and the as-built bench are identified and recorded | ML safety lead; test bench owner | G3 |
