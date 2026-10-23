# Baseline Gap Assessment

| Field | Value |
|---|---|
| Work product | Baseline gap assessment (supporting document, not a registered work product) |
| Standard reference | ISO 12100:2010; ISO 10218-1:2025 and ISO 10218-2:2025 (checked against the 2011 editions and ISO/TS 15066:2016 where the 2025 text is not held); ISO 13849-1:2023 and 13849-2:2012; EN 60204-1:2018; ISO 13850:2015; ISO 13854:2019; ISO 13857:2019; IEC 62443-4-1/-4-2; Regulation (EU) 2023/1230 |
| Version | 0.1: initial assessment (2026-10-20) |
| Status | Draft |
| Author | Assurance team (AI-assisted static review of the repository and of the concept-phase engineering package, I0) |
| Reviewer(s) | TBD |
| Baseline | `jherrodthomas/reBot-DevArm@206ebda` (2026-05-03: upstream `Seeed-Projects/reBot-DevArm` hardware record v1.1 of 2026-04-25 plus the fork's concept-phase engineering package of 2026-05-04) |

## 1. Scope and method

This was a static review of the fork at the baseline above. No arm was built, powered or operated, and no software
was run. The review had two inputs:

- **The inherited repository.** The B601-DM hardware record (`hardware/reBot_B601_DM/`: the v1.1 STEP assembly, the
  3D-printed, machined and purchased-parts BOM, the performance-testing reference) and the upstream README. The
  software the arm runs (the Python `motorbridge` SDK, the ROS 2 driver, the LeRobot and Pinocchio integrations, the
  grasping demo, the web UI) lives in other upstream repositories and on the Seeed wiki; it was read only as
  documented, not as code (GAP-16).
- **The concept-phase engineering package** the fork added on 2026-05-04 at the repository root:
  `reBot_DevArm_Safety_Case.xlsx` (34 catalogued hazards, which its dashboard counts as 33; 31 safety functions, 28 gaps, 8 assumptions), `reBot_DevArm_DFMEA.xlsx`
  (27 failure modes), `reBot_DevArm_Requirements.xlsx` (104 requirements), `reBot_DevArm_TestPlan.xlsx` (127 test
  cases), the architecture description, the trace memo and the bundle. The package is treated as an **input**: its
  findings are re-stated here as GAP-nn with the package identifier in the evidence column (§8 maps every one), its
  hazard and safety-function identifiers are kept in [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) and
  [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md), and its workbooks become evidence items of the safety case
  once each is reviewed (WP-K-01 Sn-03).
- **Configuration:** findings are stated for the **reBot Arm B601-DM v1.1**: six Damiao V4 actuators (4 × DM4310,
  3 × DM4340P per the BOM; joint 1 moved to a DM4340P in v1.1), one gripper actuator, sheet-metal and CNC aluminium
  links with 3D-printed covers and fingers, a single CAN daisy chain on XT30 2+2 cables, a DM CAN-USB adapter to a host
  PC, and a MEAN WELL LRS-350-24 (24 V, 14.6 A) supply. The B601-RS (RobStride) variant has no released BOM and is
  covered in §7 as a variant, not as assessed design.
- **Not reviewed:** the Seeed wiki tutorials beyond what the README links, the Star Arm 102 leader arm, the Isaac Sim
  model, the actuators' own firmware (closed), the `reBot_B601_RS` folder (empty of a BOM at the baseline).

Severity: **High** means the finding blocks a safety claim or allows a hazardous event today; **Medium** means it
weakens a claim or must be closed before a gate; **Low** means a documentation or process gap with no direct hazard.
Every finding becomes a defeater in the safety case ([WP-K-01 §7](../10-safety-case/WP-K-01-safety-case.md#7-defeaters))
and stays open until the work product that closes it is reviewed.

## 2. Summary

The arm is a well-documented open mechanical and actuator design with a broad software ecosystem, and the package
the fork published is a sound concept-phase scaffold. What neither contains is the safety engineering a machine
needs before it may work with people in reach: there is no emergency stop in the documented design, no supply
disconnect or fusing, no watchdog between the host and the actuators, no operating-mode state machine, no declared
joint limits, no reliability data, no force or pressure measurement, no validation, and the software is outside the
fork's control. Nineteen findings are rated High. The package's own conclusion stands: **provisional acceptance for a
supervised, fixtured laboratory bench (OE-1) only**, and this record does not yet support even that with evidence.

| Area | Findings | High |
|---|---|---|
| §3 Mechanical and structural | GAP-01…GAP-07 | 4 |
| §4 Electrical, power and emergency stop | GAP-08…GAP-15 | 4 |
| §5 Motion control, software and command path | GAP-16…GAP-26 | 8 |
| §6 Collaborative operation and information for use | GAP-27…GAP-30 | 2 |
| §7 Process, documentation and configuration | GAP-31…GAP-36 | 1 |

## 3. Mechanical and structural

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-01 | Joint pinch-zone gaps are not analysed: the gaps between adjacent links, between the covers and the links, and at the gripper jaws are not measured against the minimum gaps that avoid crushing a finger or hand | STEP assembly v1.1; package GAP-13854-01, HZ-M01, HZ-P03, FM-27 | ISO 13854; ISO 10218-1 (pinch and crush points) | High |
| GAP-02 | Mechanical end-stops exist only where the BOM says so (the joint-1 yaw limit block and the upper- and lower-arm limit blocks, added in v1.1); joints 4 to 6 and the gripper rely on the actuator's own position limits, and no joint has a documented stop angle or a software limit inboard of it | BOM "Added yaw angle motion limit", `01_Upper_Arm_Limit`, `01_Lower_Arm_Limit`; package HZ-C05, SYRS-017 | ISO 10218-1 (axis limiting); ISO 13849-1 §5 | High |
| GAP-03 | The mass, the payload moment at reach, the centre of gravity and the base fixing are not specified: the README gives "approx. 4.5 kg" and the package estimates a 22 N·m moment at 650 mm with 1.5 kg, but the base plate's fixing points, bolt size and torque are not documented and an unfixtured arm tips | README specifications; package HZ-M06, FM-09, ASS-A-05 | ISO 12100 §5.3; Machinery Reg. Annex III §1.3 | High |
| GAP-04 | Load-bearing machined parts are offered as 3D-printable substitutes ("can be 3D printed in ABS with high infill") with no strength analysis, and the printed covers and fingers have no declared material, load case or inspection interval; a cracked cover exposes the joint gap it guards | BOM remarks on `02_Base_Reinforcement_Part`, `02_Motor_Front_Spacer`, `02_Slider_Bracket`; package FM-07, FM-08, ASS-A-03 | ISO 12100 §6.2; ISO 10218-1 | Medium |
| GAP-05 | Sharp edges on the sheet-metal brackets and the fastener torque are not specified; the DFMEA rates a loosened fastener as a projectile risk | BOM; package HZ-M03, FM-10 | ISO 12100 Annex B | Low |
| GAP-06 | No separation-distance or reach-envelope safeguarding plan exists: the 650 mm reach is declared but where a person may stand relative to it, in which mode, is not | package GAP-13857-01, SYRS-030 | ISO 13857; ISO 13855; ISO 10218-2 §5 | High |
| GAP-07 | Whether the gripper holds its grasp on power loss is unknown: the gripper actuator and its drive train are not characterised for back-driving, so a payload may drop when the E-stop removes power | package HZ-M07, FM-06, SYRS-014 | ISO 10218-1 (end effector, power loss) | Medium |

## 4. Electrical, power and emergency stop

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-08 | No emergency stop exists in the documented design: the BOM lists no E-stop device, safety relay or contactor; upstream's docs mention a XIAO ESP32 wireless stop but specify nothing (channels, link surveillance, what it switches); the only stop is a software command over the same CAN bus that drives the motors | BOM (purchased parts); package GAP-10218-02, GAP-60204-03, HZ-P04, FM-16, FM-17, FM-25 | ISO 10218-1 §5 (emergency stop); ISO 13850; EN 60204-1 §9.2, §10.7 | High |
| GAP-09 | No supply disconnecting device: the 24 V, 14.6 A supply feeds the XT30 daisy chain directly; there is no lockable disconnect and no fuse between the supply and the harness | BOM "Power supply 24V 14.6A", XT30 cables; package GAP-60204-01 | EN 60204-1 §5.3, §7.2 | High |
| GAP-10 | No overcurrent protection per branch: seven actuators share one 16 AWG XT30 chain; a stalled joint or a shorted harness is limited only by the supply's own protection | BOM; package SYRS-013, HZ-E02, HZ-T02 | EN 60204-1 §7.2, §13 | Medium |
| GAP-11 | The mains side is undocumented: the LRS-350-24 is an open-frame supply with exposed mains terminals, and no enclosure, bonding, cord or inlet is specified | BOM "Power supply", "Power Cable 12AWG" | EN 60204-1 §6, §8 | High |
| GAP-12 | The arm's 24 V input is not keyed against reverse polarity and has no reverse-polarity protection; the package's own architecture notes a barrel-jack style input it recommends replacing | package FM-15, HZ-E01, architecture §7.1 | EN 60204-1 §6; IEC 60204-1 §13 | Medium |
| GAP-13 | Motor over-temperature protection is the actuator's own closed firmware only: upstream's test reached 90 °C on joint 2 and was stopped by that protection; there is no cut-off independent of the drive and no stator temperature threshold the record controls | `performance_testing/Performance_Testing.md`; package HZ-T01, FM-03, SYRS-012 | ISO 12100 Annex B (thermal); EN 60204-1 §7.3 | Medium |
| GAP-14 | No reliability data exists for any part of a safety function: the Damiao DM4310 and DM4340P actuators, the gripper actuator and the supply publish no MTTFD, B10D or failure-rate figure, so no Performance Level can be calculated | package GAP-13849-02, OI-05 | ISO 13849-1 §6, Annex C–D | High |
| GAP-15 | EMC immunity and emissions are not declared for the arm or the harness; a disturbed CAN bus is a loss-of-communication event (GAP-18) | package GAP-EMC-01, HZ-E04 | EN 61000-6-2/-6-3; EN 60204-1 §4.4.2 | Low |

## 5. Motion control, software and command path

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-16 | The software that moves the arm is outside the fork: the `motorbridge` SDK, the ROS 2 driver, the LeRobot and Pinocchio integrations and the web UI live in upstream repositories and on the wiki, none is pinned to the hardware baseline, and the only firmware is the actuators' closed firmware; nothing the fork controls can be hardened until that software is forked (decision DQ-007) | README roadmap and links; package EV-SDK-01 | ISO 13849-1 §7; IEC 61508-3 §7.4.2 | High |
| GAP-17 | No operating-mode state machine exists: the modes OFF, IDLE, TEACH, RUN and ESTOP the package proposes are not implemented; any client can enable a motor and command torque at any time, and nothing gates the transition into motion | package GAP-10218-04, SYRS-009 | ISO 10218-1 §5 (operational modes) | High |
| GAP-18 | Loss of communication holds the last command: no watchdog or heartbeat between the host and the actuators is documented, so a stalled SDK process, a dropped ROS topic or a bus fault leaves each joint under its last torque or position command | package HZ-C01, HZ-C04, FM-18, FM-19, SYRS-008 | ISO 13849-1 §5; ISO 10218-1 §5 | High |
| GAP-19 | Joint speed, torque and momentum limits are not declared per joint and are enforced, where at all, only inside the client library; nothing between a command source and the drive bounds them | package GAP-10218-03, SYRS-003, SYRS-004 | ISO 10218-1 §5 (limiting); ISO/TS 15066 | High |
| GAP-20 | Software joint limits inboard of the mechanical end-stops are not defined, so a position command can run a joint into its stop or through a singularity | package HZ-C05, SYRS-017 | ISO 10218-1 §5 | Medium |
| GAP-21 | No verification evidence exists for any software component: no tests of the motion-critical path, no static analysis, no coverage; the package's 127 test cases are specified, none has run | package TestPlan 09_Stats; GAP-13849-03 | ISO 13849-1 §7, §8 | High |
| GAP-22 | Any process with the CAN-USB adapter open can command every joint: CAN carries no authentication, the host has no access control on the adapter, and the SDK accepts commands from any caller | package HZ-C02, FM-20; architecture §5 | IEC 62443-4-2 CR 1, CR 2; ISO 10218-1 §5 | High |
| GAP-23 | Tele-operation (the leader arm path, the web UI, the ROS bridge) is unauthenticated and unencrypted; an idle session never locks | package GAP-CYB-01, SYRS-015, SYRS-016 | IEC 62443-4-2 CR 1.1, CR 1.7; IEC 62443-4-1 SR | High |
| GAP-24 | Learned policies (LeRobot imitation policies, the YOLO grasping demo) run with no independent clamp on their output and no verification against the hazard list; the package's own FMEA rates an out-of-distribution scene as a high-priority failure | package GAP-LP-01, HZ-C06, FM-21, OI-06 | ISO/IEC TR 5469; ISO 10218-1 §5 | High |
| GAP-25 | The wrist camera, where fitted, streams by default and nothing states a retention or recording posture; people at the bench are recorded without a decision | package GAP-PRIV-01, HZ-D01, FM-23 | IEC 62443-4-2 CR 4; GDPR (reference) | Medium |
| GAP-26 | Inverse kinematics near the workspace boundary can spike joint speed; the damping is a property of the client library, not of a limit the arm enforces | package HZ-C07, FM-22 | ISO 10218-1 §5 (singularities) | Medium |

## 6. Collaborative operation and information for use

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-27 | Adequacy of risk reduction is not recorded for 18 of the package's hazards: the hazard is rated and a safety function named, but the three-step allocation and the residual risk are not written | package GAP-12100-01, 07_HARA | ISO 12100 §6.1, §6.4 | High |
| GAP-28 | No power-and-force-limiting measurement exists and the body-region thresholds are not bound to joint torque or speed caps, so no collaborative claim (contact permitted) can be made for any envelope | package GAP-15066-01, GAP-15066-02, HZ-P01, HZ-P02, FM-24 | ISO/TS 15066 §5, Annex A; ISO 10218-2 §5 | High |
| GAP-29 | No information for use: no operator manual, no limits and warnings, no power-on checklist, no E-stop test procedure, no lock-out, no residual-risk statement; the Seeed wiki covers assembly and software only | package GAP-12100-02, GAP-DOC-01, SYRS-034 | ISO 12100 §6.4; ISO 13849-1 §13; Machinery Reg. Annex III §1.7 | Medium |
| GAP-30 | No motion-imminent warning exists before a commanded motion; the package asks for an audible or visible signal 500 ms ahead | package SYRS-035, SF-15 | ISO 10218-1 §5; ISO 12100 §6.4 | Low |

## 7. Process, documentation and configuration

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-31 | No safety function has been validated: no validation plan or report exists, no category 3 structure is implemented for the functions the package rates PL d, and no fault-injection has been run | package GAP-13849-01, GAP-13849-03, GAP-10218-01 | ISO 13849-1 §6, §10; ISO 13849-2 | High |
| GAP-32 | Design-review, nonconformance and corrective-action records are absent, and test and calibration records are not kept; git history is the only document control | package GAP-9001-01, -02, -04, -05 | ISO 9001 §7.5, §8.3, §8.7, §10.2 (informative); IEC 61508-1 §6 | Medium |
| GAP-33 | Kit assembly has no production controls: an assembly video and a BOM are the only instructions, and fastener torque, harness termination and cover fit depend on the builder | package GAP-9001-03; BOM | ISO 12100 §6.4; Machinery Reg. Annex III §1.7.4 | Medium |
| GAP-34 | The B601-RS (RobStride) variant has no released BOM, firmware notes or software; the two variants share the envelope but not the control interface, and nothing detects which is fitted | README roadmap (B601-RS "in progress"); package GAP-VAR-01, FM-26, OI-03 | ISO 12100 §5.3 (limits); ISO 13849-1 §12 | Medium |
| GAP-35 | The CC BY-NC-SA 4.0 licence forbids commercial use; a safety-assured build placed in a workplace (the package's OE-3) may be commercial use under upstream's statement, and the record does not yet say which envelopes the licence allows | README licence statement; package EV-LIC-01 | Machinery Reg. Art. 3, Art. 10 (placing on the market) | Medium |
| GAP-36 | Repeatability (< 0.2 mm) is declared but no ISO 9283 test pack exists; not a safety gap, but the record's only performance evidence is the upstream thermal test | package GAP-9283-01 | ISO 9283 | Low |

## 8. Map of the package's gap register

| Package ID | Here | Package ID | Here |
|---|---|---|---|
| `GAP-12100-01` | GAP-27 | `GAP-9001-01` | GAP-32 |
| `GAP-12100-02` | GAP-29 | `GAP-9001-02` | GAP-32 |
| `GAP-10218-01` | GAP-31 | `GAP-9001-03` | GAP-33 |
| `GAP-10218-02` | GAP-08 | `GAP-9001-04` | GAP-32 |
| `GAP-10218-03` | GAP-19 | `GAP-9001-05` | GAP-32 |
| `GAP-10218-04` | GAP-17 | `GAP-60204-01` | GAP-09 |
| `GAP-15066-01` | GAP-28 | `GAP-60204-02` | GAP-31 |
| `GAP-15066-02` | GAP-28 | `GAP-60204-03` | GAP-08 |
| `GAP-13849-01` | GAP-31 | `GAP-EMC-01` | GAP-15 |
| `GAP-13849-02` | GAP-14 | `GAP-9283-01` | GAP-36 |
| `GAP-13849-03` | GAP-31 | `GAP-13854-01` | GAP-01 |
| `GAP-DOC-01` | GAP-29 | `GAP-13857-01` | GAP-06 |
| `GAP-CYB-01` | GAP-23 | `GAP-LP-01` | GAP-24 |
| `GAP-PRIV-01` | GAP-25 | `GAP-VAR-01` | GAP-34 |

Findings the package did not carry and this review adds: GAP-02 (end-stops), GAP-03 (mass and fixing), GAP-04
(printed substitutes), GAP-05, GAP-07 (gripper holding), GAP-10 (branch protection), GAP-11 (mains side), GAP-12
(input connector), GAP-13 (thermal cut-off), GAP-16 (software outside the fork), GAP-18 (watchdog), GAP-20, GAP-21,
GAP-22 (bus access), GAP-26, GAP-30, GAP-35 (licence).

## 9. Priority actions

In the order the record will take them; each is a work product or a decision, never a claim.

1. **Decide the frame and the first envelope** (DQ-002, DQ-003): the EU machinery frame with ISO 10218 and
   ISO/TS 15066, and a supervised, fixtured bench (OE-1) as the only envelope of the first safety case.
2. **Bench safety hardware before any powered test with a person in reach** ([WP-V-07](../06-validation/WP-V-07-test-operations.md)):
   a lockable disconnect and a fuse on the 24 V supply, a dual-channel emergency stop through a safety relay that
   drops the motor supply by contactor, and the operator's hand on the button. Buying it is DQ-006.
3. **Fork the software** (DQ-007) so that a safety layer can sit between every command source and the bus: a
   watchdog and heartbeat (GAP-18), the mode state machine (GAP-17), per-joint limits (GAP-19, GAP-20), and a clamp on
   every learned output (GAP-24).
4. **Write the risk assessment on the record's terms** ([WP-C-03](../02-concept/WP-C-03-risk-assessment.md),
   [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md), [WP-C-05](../02-concept/WP-C-05-risk-reduction-concept.md)):
   the package's hazards re-rated per operating envelope, an explicit emergency-stop function, the three-step
   allocation for every row (GAP-27).
5. **Measure what the analyses assume** (GAP-03, GAP-01, GAP-02): weigh the arm, record the fixing, measure the joint
   gaps, record the end-stop angles.
6. **Ask the suppliers for reliability data** (DQ-019) and decide the collaborative claim (DQ-005) before any PL
   calculation or force measurement is planned.

## 10. Decisions raised

DQ-001 (which configuration first), DQ-002 (regulatory frame), DQ-003 (first operating envelope), DQ-004 (required
PL for the stop functions), DQ-005 (collaborative claim), DQ-006 (bench safety hardware), DQ-007 (fork the
software), DQ-008 (learned policies in the item), DQ-009 (assessor), DQ-010 (roles while one person holds them);
queued: DQ-011 (standards purchase), DQ-012 (conformity route), DQ-013 (security level target), DQ-014 (camera
privacy default), DQ-015 (gripper holding requirement), DQ-016 (torque and speed ceilings for OE-1), DQ-017 (the RS
variant), DQ-018 (supply disconnect means), DQ-019 (supplier data request), DQ-020 (where the safety layer runs). All
in the [decision register](../01-management/decisions/register.yaml).
