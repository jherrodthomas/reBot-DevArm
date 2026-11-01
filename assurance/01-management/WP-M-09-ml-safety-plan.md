# WP-M-09 Machine-learning safety plan

| Field | Value |
|---|---|
| Work product | WP-M-09 Machine-learning safety plan |
| Standard reference | Other: TR 5469 (AI technology classes, usage levels); AI Act Art. 9; ASPICE: MLE.1–4. Clause numbers are to be checked against licensed copies ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1) |
| Version | 0.1 (first draft: the DQ-008 position as operating rules, the learned components known today, TR 5469 classification approach, activities per gate, the Annex I Part A and AI Act threshold under DQ-012; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How learned components are managed so that none carries a safety function, and what evidence the fork keeps about
them under ISO/IEC TR 5469 and, if the threshold of [WP-M-13 §5](WP-M-13-regulatory-conformity-strategy.md#5-the-ai-act-threshold)
is ever crossed, the AI Act. A learned component here is any software whose behaviour comes from training on data
rather than from a specification: the LeRobot imitation and reinforcement policies, the YOLO grasping demo, any
vision-language-action model, and any agent that turns a model's output into arm commands. Model-based software
(Pinocchio kinematics and gravity compensation, the current-based torque estimator) is not a learned component; its
limits are analysed in [WP-C-10](../02-concept/WP-C-10-functional-insufficiency-analysis.md).

## 2. Position

The lead decided on 2026-11-01 that learned policies are **inside the item and outside every safety function**:
they run only in RUN, behind the joint, torque and speed clamps and the watchdog, with the checkpoint recorded per
test (DQ-008, answered A; [WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring) T-03). This plan turns that into
rules that hold for every learned component, in development and after release:

| # | Rule | Enforced by |
|---|---|---|
| ML-P1 | No safety function is allocated to a learned component, and no learned output is credited in any PL calculation | [WP-C-04 §5](../02-concept/WP-C-04-safety-functions-and-plr.md#5-allocation) allocation; WP-H-04 |
| ML-P2 | A learned component commands the arm only as a client of the host stack, through the controller safety layer on its dedicated controller (DQ-020, answered A); it has no path to the bus that bypasses the clamps | WP-S-03, WP-S-07; the controller is the only conduit to the bus |
| ML-P3 | A learned component runs only in M-04 RUN; the mode machine refuses its commands in IDLE, TEACH and ESTOP | SF-08, SF-25, the mode machine (WP-W-02) |
| ML-P4 | Every learned output passes the same validation and clamp as any other command: finite, fresh, within the joint, torque, speed and jerk limits of the mode (SF-03, SF-23, SF-29) | Controller safety layer |
| ML-P5 | No learned component can change a limit, a timing, a mode or a safety parameter, and none sits in a stop or reset path | WP-W-09 parameter protection; SF-24 |
| ML-P6 | A learned component may stop the arm (refuse, hold, request IDLE) but its stop is never credited; an out-of-distribution condition it detects leads to stop, not guess | WP-C-09 AIR-nn |
| ML-P7 | Every powered run of a learned component records the repository commit, the checkpoint hash, the dataset identifier and the scene, in the test log | [WP-V-07 §5](../06-validation/WP-V-07-test-operations.md#5-test-log); WP-W-10 |
| ML-P8 | A component that needs the wrist camera uses it under the camera rule: default-off, opt-in per session with a visible indicator, local storage (DQ-014, answered A; SF-31) | Host stack; WP-C-08 |

The consequence the strategy accepts: the safety of a run never depends on the policy being right. A policy that
outputs a wrong but in-limit trajectory is a functional insufficiency bounded by the clamps, the separation of OE-1
and the operator's hand on the pendant ([WP-V-07 §3](../06-validation/WP-V-07-test-operations.md#3-limits-during-development-testing)).

## 3. Classification under ISO/IEC TR 5469

Each learned component gets an AI technology class and a usage level in
[WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md). The approach, to be confirmed
against a licensed copy of TR 5469:

- **Usage level:** the target for every component is the level TR 5469 gives to AI technology used outside the
  safety function, whose effect on safety is bounded by an independent non-AI safeguard (here the controller safety
  layer and the hardwired chain). No component is placed at a usage level where AI forms part of a safety function.
- **Technology class:** deep-learned policies and detectors are expected to fall in the class for which the
  required properties cannot be fully shown by existing functional-safety methods. That is acceptable only because
  of the usage level; the class is recorded, not argued away.
- **Known learned components** (to be completed in WP-C-09 as ML-nn):

| Component | Source | Inputs | Output reaches the arm as | Status |
|---|---|---|---|---|
| LeRobot imitation and reinforcement policies | Hugging Face LeRobot with Seeed's integration (wiki) | camera images, joint state | joint targets through the host stack | upstream; checkpoints per dataset |
| YOLO grasping demo | Seeed wiki demo | camera images | a grasp pose turned into a planned motion | upstream demo |
| Agents in the community ROS 2 driver and digital twin | `Yang-Ci/ReBot_Arm_DigitalTwin_DM` (forked and pinned, not modified; [WP-M-10](WP-M-10-upstream-and-supplier-management.md)) | not yet analysed | not yet analysed | to be analysed; not used in OE-1 until it is |
| Any vision-language-action model | none integrated at BL-001 | — | — | enters only by an impact-analysed change |

## 4. Activities by gate

| Gate | Activity | Work product | Review |
|---|---|---|---|
| G0 | This plan; the learned components identified (§3) | WP-M-09 | — |
| G1 | ML-nn definitions, class and usage level, requirements AIR-nn (output clamping, out-of-distribution stop, checkpoint identity, no learned component in a stop path); the functional insufficiencies and triggering conditions of the policies (distribution shift, occlusion, lighting, unseen objects) | WP-C-09, WP-C-10 | ML-R1 |
| G2 | AIR-nn traced to the controller clamps and the mode machine; the independence of the clamp from the policy runtime analysed | WP-S-02, [WP-A-05](../08-analyses/WP-A-05-independence-of-the-safety-chain.md) | — |
| G3 | Datasets and their provenance, training records, checkpoint pinning, the edge-case coverage matrix against the hazard list | [WP-W-10](../05-software/WP-W-10-ml-engineering.md) | ML-R2 |
| G4 | Fault injection of out-of-limit policy outputs at the controller | [WP-V-05](../06-validation/WP-V-05-fault-injection.md) | — |
| G5 | Unknown-scenario trials with the checkpoint per trial; the AI Act record that no learned component is a safety component | [WP-V-08](../06-validation/WP-V-08-unknown-scenarios-and-field-trials.md), [WP-K-07](../10-safety-case/WP-K-07-ai-act-conformity-record.md) | ML-R3 |
| G6 | Policy-related anomalies from the field fed back into WP-C-10 | [WP-O-04](../09-production-operation/WP-O-04-field-monitoring.md) | — |

The reviews are those of [WP-M-06 §7](WP-M-06-confirmation-measures-plan.md#7-cybersecurity-and-ml-reviews).

### 4.1 The regulatory threshold

The conformity route is Module A, internal control (DQ-012, answered A). It holds only while no safety function is
allocated to a learned component: the Machinery Regulation's Annex I Part A (machinery with self-evolving behaviour
ensuring safety functions) and the AI Act's high-risk path apply only if one is (WP-M-13 §5). Any change that would
let a learned output trigger, inhibit, delay or parameterise a safety function, or that would credit a learned stop,
is therefore not a technical change: it reopens DQ-008 and DQ-012 with the lead before it is made, and its impact
record says so. WP-K-07 states at each gate that the threshold has not been crossed, with the allocation table as
evidence.

## 5. Roles

From [WP-M-02 §3.1](WP-M-02-safety-plan.md#31-role-assignments). Approvals by the one person holding these roles are
self-approval at I0 (DQ-010, answered A).

| Role | Holder (today) | Duty |
|---|---|---|
| ML safety lead | Jherrod Thomas (acting); permanent holder TBD, needed by G1 | Owns this plan and WP-C-09; classifies the learned components; keeps the evidence that none carries a safety function |
| Safety manager | Jherrod Thomas (acting) | Rates policy-induced hazards (HZ-C06) in WP-C-03; owns the allocation of WP-C-04 |
| External ML reviewer | TBD (may be the FS assessor); none engaged | ML-R1…ML-R3 |

## 6. Upstream

The LeRobot integration, the grasping demo, the agents of the community driver and every policy checkpoint are
upstream or community material; their quality varies per dataset (package open issue OI-06; GAP-24). The fork does
not train or ship a checkpoint at this version. It records which checkpoint ran in which test (ML-P7), keeps the
checkpoints it uses under configuration control ([WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md)
lists policy checkpoints as configuration items), and treats a checkpoint as untrusted input whose tampering is a
threat scenario in [WP-C-07](../02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md). Of the three
software repositories (WP-M-10 §2), only `motorbridge` is modified; a policy runtime change in the other two waits
for their licence question to be answered.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Confirm the TR 5469 usage-level and class designations of §3 against a licensed copy (DQ-011: bought when an assessor is engaged) | ML safety lead | G1 |
| OI-2 | Analyse what the agents and web control of the community ROS 2 driver can command, and whether any of them is a learned component | ML safety lead | G1 |
| OI-3 | Identify which LeRobot policies and checkpoints the first safety case runs, with their datasets | ML safety lead | G1 |
| OI-4 | Name an external ML reviewer for ML-R1, or record its deferral at the G1 review | Project maintainer | G1 |
| OI-5 | Add the checkpoint, dataset and scene fields of ML-P7 to the test-log template under `06-validation/test-sites/` | Safety manager | Before the first powered policy run |
| OI-6 | Fill the permanent ML safety lead role | Project maintainer | G1 |
