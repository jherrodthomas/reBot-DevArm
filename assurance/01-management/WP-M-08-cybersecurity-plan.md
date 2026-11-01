# WP-M-08 Cybersecurity plan

| Field | Value |
|---|---|
| Work product | WP-M-08 Cybersecurity plan |
| Standard reference | IEC 62443: 62443-4-1 §5 (SM-1…SM-13); 62443-4-2 §4; ASPICE: MAN.7 (CS). Clause numbers are to be checked against licensed copies ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1) |
| Version | 0.1 (first draft: scope, SL-T of DQ-013, the 4-1 practices mapped to work products, the three upstream repositories as supplied components, interface to safety; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How cybersecurity is managed for the fork under IEC 62443-4-1 (secure product development lifecycle) and
IEC 62443-4-2 (technical requirements for components), and how it interfaces with machinery safety. It applies the
cybersecurity rows of the [assurance strategy](WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used)
and tailoring T-11 ([WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring)); the
[safety plan (WP-M-02)](WP-M-02-safety-plan.md) refers here for the discipline. The plan is updated at every gate and
whenever the scope of §2 changes. No security activity of §3 has been performed yet.

## 2. Scope and security context

### 2.1 What is protected

The arm with its host is assessed as one component (T-11), CFG-001 in OE-1 ([WP-C-01](../02-concept/WP-C-01-item-definition.md),
[WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md)). The 4-1 practices apply to the repositories the
fork controls: this record, the three software forks of DQ-007 (§2.3) and the controller safety layer of DQ-020.

| Element (WP-C-01 §3) | Security role | Interfaces |
|---|---|---|
| E-06 host software: the forked `motorbridge` stack, the arm control library, the ROS 2 driver and digital twin, the policy runtime | Every motion request originates here; hardened as defence in depth, no PL claim (T-04) | IF-03, IF-04, IF-05, IF-06 |
| E-07 controller safety layer on a dedicated controller between the host and the motor bus (DQ-020, answered A) | The only path from the host to the bus once fitted; authenticates the host session and clamps every command | IF-01, IF-02, the host link |
| E-04, E-05 motor bus and CAN-USB adapter | CAN carries no authentication; whoever reaches the bus moves the arm (GAP-22) | IF-01, IF-02 |
| E-08 bench safety chain | Hardwired, no network or software interface; the controller can only open it through K3 ([WP-H-02 §2](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md#2-design-decisions) E-07) | none that can close it |
| E-10 wrist camera, leader arm | Camera stream is personal data at the bench (GAP-25); the leader arm is a command source | IF-05, IF-06 |
| Update path | How a fork release and its parameter sets reach a built arm ([WP-P-10](../07-supporting/WP-P-10-release-management.md), [WP-O-05](../09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md)) | release artefacts |

**External zones (not protected, interface assumptions only):** the site network, the operator's other computers,
any remote operator, the hosted web UI linked from upstream's README translations, PyPI and other package indexes, and GitHub
itself. WP-S-07 draws the zones and conduits; the bench in OE-1 runs with one client, the host on a private network or
none, and no remote session ([WP-V-07 §3](../06-validation/WP-V-07-test-operations.md#3-limits-during-development-testing)).

### 2.2 Security level target

Decided by the lead (DQ-013, answered A, 2026-11-01). WP-C-08 §2 records it and derives the requirements.

| Foundational requirement (62443-4-2) | SL-T | Why it matters here |
|---|---|---|
| FR 1 Identification and authentication control | **SL 2** | Every motion command path authenticated (GAP-22, GAP-23); SF-26 |
| FR 2 Use control | SL 1 | One client at a time, session lock (SF-27) |
| FR 3 System integrity | **SL 2** | Signed safety parameters and releases; command integrity at the controller |
| FR 4 Data confidentiality | **SL 2** | Camera stream and recordings (DQ-014, SF-31); credentials |
| FR 5 Restricted data flow | SL 1 | The chain zone has no conduit; the host-to-controller link is the only conduit to the bus |
| FR 6 Timely response to events | SL 1 | Security event log on the host and the controller |
| FR 7 Resource availability | SL 1 | Denial of service on the heartbeat ends in a safe stop (SF-08, SF-25), not in motion |

### 2.3 Software supplied from upstream

The software that moves the arm is three upstream repositories, which the lead chose to fork into the
`jherrodthomas` GitHub account and pin (DQ-007, answered A). Under 4-1 SM-9 and SM-10 they are externally provided
components; their management is in [WP-M-10 §2](WP-M-10-upstream-and-supplier-management.md#2-upstream).

| Repository | Role | Licence | Fork's use |
|---|---|---|---|
| `motorbridge/motorbridge` | CAN motor-control stack: Rust core, C ABI, Python and C++ bindings | MIT | Forked and changed: authenticated client session, command bounds mirrored from the controller, build from source at the pin |
| `Seeed-Projects/reBotArm_control_py` | Arm control library: kinematics, dynamics, gravity compensation on top of motorbridge | None stated | Forked and pinned; not modified until a licence is stated |
| `Yang-Ci/ReBot_Arm_DigitalTwin_DM` | Community ROS 2 driver and digital twin: MoveIt 2, MuJoCo, web control, agents | Ambiguous (CERN-OHL-W-2.0 file, Apache-2.0 in README) | Forked and pinned; not modified until the licence is clarified; its web control and agent paths are not used in OE-1 until authenticated |

Because two of the three cannot be changed yet, the security measures that matter sit where the fork may write
code: the controller safety layer (authentication of the host link, command validation) and the forked motorbridge.
The unmodified repositories are treated as untrusted command sources behind those measures.

## 3. Practices of IEC 62443-4-1 and where each lands

Practice names are given from memory and are to be checked against a licensed copy.

| Practice | What the fork does | Work product |
|---|---|---|
| SM Security management (SM-1…SM-13) | This plan; roles (§5); applicability (SM-3) via the baseline impact analysis; competence (SM-4); file integrity and protected default branch (SM-6); development environment (SM-7); signing keys for releases and parameter sets held by the cybersecurity manager, never in a repository (SM-8); externally provided and third-party components (SM-9, SM-10); issue handling (SM-11); process verification and improvement (SM-12, SM-13) | WP-M-08, [WP-M-04](WP-M-04-organization-competence-safety-culture.md), [WP-M-05](WP-M-05-quality-assurance-plan.md), [WP-M-10](WP-M-10-upstream-and-supplier-management.md), [WP-M-11](WP-M-11-impact-analysis.md), [WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md), [WP-P-08](../07-supporting/WP-P-08-software-component-qualification.md) |
| SR Security requirements (SR-1…SR-5) | Product security context (§2), threat model and threat scenarios TS-nn rated against the hazard list, CSR-nn with the SL-T of §2.2, requirements review | [WP-C-07](../02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md), [WP-C-08](../02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md) |
| SD Secure design (SD-1…SD-4) | Zones and conduits; defence in depth from host to controller to chain; design review | [WP-S-07](../03-system/WP-S-07-cybersecurity-architecture.md) |
| SI Secure implementation (SI-1, SI-2) | Secure coding rules for the controller and the forked motorbridge (Rust, C, Python); implementation review in the pull request | [WP-W-01](../05-software/WP-W-01-software-development-environment-guidelines.md), [WP-W-05](../05-software/WP-W-05-software-unit-design.md), [WP-W-11](../05-software/WP-W-11-cybersecurity-implementation-verification.md) |
| SVV Verification and validation (SVV-1…SVV-5) | Requirement tests, threat mitigation tests, dependency vulnerability scans, a penetration test of the host and controller link before release; tester independence per WP-M-06 | [WP-W-11](../05-software/WP-W-11-cybersecurity-implementation-verification.md), [WP-V-06](../06-validation/WP-V-06-cybersecurity-validation.md) |
| DM Defect management (DM-1…DM-6) | Private intake through [SECURITY.md](../../SECURITY.md); triage against the hazard list; advisories; routing of upstream defects to their owners | [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md), [WP-O-05](../09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md) |
| SUM Security updates (SUM-1…SUM-5) | Every update qualified as a change with an impact record; dependent-component updates (upstream pins, PyPI, ROS 2) documented; delivery as a signed fork release | [WP-P-10](../07-supporting/WP-P-10-release-management.md), [WP-O-05](../09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md) |
| SG Security guidelines (SG-1…SG-7) | Defence-in-depth and environment expectations (private network, one client), hardening, secure operation, account and key handling, disposal of recordings | [WP-S-06](../03-system/WP-S-06-requirements-installation-operation.md), [WP-O-02](../09-production-operation/WP-O-02-operation-maintenance-decommissioning.md), [WP-O-03](../09-production-operation/WP-O-03-information-for-use.md) |

Supply-chain rules that follow from SM-9 and SM-10, applied from the first fork release:

1. Every upstream repository is used at a pinned commit of its fork, never at a branch or a floating package
   version. `motorbridge` is built from the fork's source at its pin, not installed from PyPI (upstream's published
   package is `motorbridge` 0.5.6, whose source commit is not yet recorded).
2. Each release carries a software bill of materials listing the three pins and every dependency with its version
   and hash; WP-P-08 holds the list and the qualification argument per component.
3. An upstream update enters only by merge into the fork with an impact record ([WP-M-11 §5](WP-M-11-impact-analysis.md#5-change-impact-analysis-records)).

## 4. Interface to safety

| Interface | Rule | Where |
|---|---|---|
| Threats that can cause a hazard | Rated with the severity of the hazard they reach; such a scenario becomes a cyber-induced hazard row (as HZ-C02 is) | WP-C-07 ↔ [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) |
| The chain as a zone | The bench safety chain has no conduit from the host or the network; no software path can close the contactors | WP-S-07 ↔ [WP-S-03](../03-system/WP-S-03-technical-safety-concept.md), WP-H-02 |
| Safety parameters | Joint limits, timings and the variant table are protected assets: signed, integrity-checked at load, changed only by an SR-A change | [WP-W-09](../05-software/WP-W-09-safety-parameters-and-configuration-data.md) ↔ WP-W-11 |
| No security measure may block a stop | A stop, a reset of the chain and the watchdog never wait for authentication; a failed authentication leads to refusal or a safe stop, never to motion | WP-C-08 requirements reviewed by the safety manager |
| Learned components | A policy is an untrusted client like any other; a tampered checkpoint is a threat scenario, bounded by the controller clamps | [WP-M-09](WP-M-09-ml-safety-plan.md), WP-C-09 |
| Change control | Every change with a security effect gets an impact record that names hazards and threat scenarios together | [`07-supporting/impact/`](../07-supporting/impact/README.md) |

Conflicts between a security and a safety requirement are decided by the safety manager and recorded in both work
products; safety takes precedence where an option would delay or prevent a stop.

## 5. Roles

From [WP-M-02 §3.1](WP-M-02-safety-plan.md#31-role-assignments). One person holds both acting roles; under DQ-010
(answered A) their approvals are self-approval at I0.

| Role | Holder (today) | Duty |
|---|---|---|
| Cybersecurity manager | Jherrod Thomas (acting); permanent holder TBD, needed by G1 | Owns this plan, the threat and risk assessment, the SL-T record and the signing keys; interface to safety on threats that can cause a hazard |
| Safety manager | Jherrod Thomas (acting) | Rates cyber-induced hazards; decides security-safety conflicts (§4) |
| External cybersecurity reviewer and assessor | TBD; none engaged | CS-I1 at G1 and CS-A1 at G5 ([WP-M-06 §7](WP-M-06-confirmation-measures-plan.md#7-cybersecurity-and-ml-reviews)) |

## 6. Known starting position

From the [gap assessment](../00-assessment/gap-assessment.md#5-motion-control-software-and-command-path), at BL-001:

- Any process that can open the CAN-USB adapter can command every joint; CAN has no authentication and the SDK
  accepts any caller (GAP-22, High).
- Tele-operation, the web UI and the ROS bridge are unauthenticated and unencrypted, and an idle session never locks
  (GAP-23, High). The community ROS 2 driver adds web control and agent paths of its own.
- The wrist camera streams by default where fitted (GAP-25). The lead chose default-off, opt-in recording per session
  with a visible indicator, local storage (DQ-014, answered A); it is SF-31 in WP-C-04 and not yet implemented.
- Nothing is pinned (GAP-16) and no release, SBOM or signature exists. The forks are being created; until they exist
  and are pinned, the bench runs under the empty-envelope rule of [WP-V-07](../06-validation/WP-V-07-test-operations.md) condition C-4.
- In place: [SECURITY.md](../../SECURITY.md) with private vulnerability reporting on this repository and its scope.

## 7. Schedule

| Gate | Due |
|---|---|
| G0 | This plan; the forks pinned and the supply-chain rules of §3 set up in WP-P-01 and WP-P-08 |
| G1 | WP-C-07 (threat scenarios TS-nn), WP-C-08 (SL-T and CSR-nn); CS-I1 |
| G2 | WP-S-07 (zones and conduits, the host-to-controller link) |
| G3 | WP-W-11 (implementation and verification of the CSRs) |
| G5 | WP-V-06 (cybersecurity validation, penetration test), [WP-K-03](../10-safety-case/WP-K-03-cybersecurity-case.md) (cybersecurity case), [WP-K-05](../10-safety-case/WP-K-05-cybersecurity-assessment.md) (CS-A1) |
| G6 | WP-O-05 in operation |

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Confirm that the three forks exist under `jherrodthomas`, record their URLs and pinned commits, and enable private vulnerability reporting on each; extend the scope of SECURITY.md to name them | Cybersecurity manager | G0 |
| OI-2 | Record which commit the PyPI package `motorbridge` 0.5.6 was built from, or document that the fork never installs it | Cybersecurity manager | G0 |
| OI-3 | Choose the SBOM format and tooling and the signing scheme for releases and parameter sets (SM-6, SM-8) | Cybersecurity manager | G1 |
| OI-4 | Name an external reviewer with IEC 62443 competence for CS-I1, or record its deferral at the G1 review (none engaged; DQ-009 answered A for the assessor) | Project maintainer | G1 |
| OI-5 | Establish how the hosted web UI linked from upstream's README translations reaches an arm, and whether the DigitalTwin web control and agents can command motion; feed both into WP-C-07 | Cybersecurity manager | G1 |
| OI-6 | Fill the permanent cybersecurity manager role | Project maintainer | G1 |
