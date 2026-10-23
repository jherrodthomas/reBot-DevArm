# WP-K-01 Safety Case

| Field | Value |
|---|---|
| Work product | WP-K-01 Safety case for the B601-DM arm (UL 4600 structure: claims, arguments, evidence, defeaters) |
| Standard reference | ISO 13849-1:2023 §4.7, §10 (information); ISO 12100 §7 (documentation); ISO 10218-2:2025 §6 (verification and validation of the robot application); Regulation (EU) 2023/1230 Annex IV Part A (technical documentation); UL 4600 §5, §6 |
| Version | 0.1 (2026-10-20): initial structure, 21 claims draft, 20 evidence items, 36 defeaters open, 10 open items; the package's GSN argument restructured onto the record's claims |
| Status | Draft |
| PL / scope | PL d target (DQ-004 open); CFG-001 B601-DM v1.1 on the supervised bench, OE-1 (DQ-003 open); CFG-002 tracked, unclaimed |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I2 for the safety case) |
| Approver | Project lead |
| Baseline | BL-001 |

> [!WARNING]
> Draft. No claim is accepted, no evidence is available, every defeater is open. The machine-readable copy of
> this document lives in `assurance/case/`; the validator fails if the two disagree (check X3). The dashboard in
> the README is generated from those records.

## 1. Purpose and scope

This document argues, for the reference configuration of WP-C-01 (CFG-001, the B601-DM v1.1, fixtured on a bench, operated in
envelope OE-1 by a trained operator with nobody else in reach), that the arm poses no unreasonable risk when operated within its
limits. At BL-001 the argument is a structure with open defeaters: it records what would have to be true, what evidence would show
it, and what is known to contradict it today. The lead's concept-phase package argued the same goal in GSN form (its tab 10_GSN);
this document keeps its conclusion (provisional acceptance for OE-1 only, with nothing yet evidenced) and restructures the argument
onto the record's claims so the validator can check it.

## 2. Argument structure

Goal G0 is argued over four strategies: S1 per safety function (G1.x), S2 over the complementary measures (G2.x),
S3 over the command path (G3.x), S4 over the process (G4.x). GSN diagrams are generated from the records
(`case/tools`), not drawn by hand.

The cybersecurity branch of the argument is WP-K-03 ([cybersecurity case](WP-K-03-cybersecurity-case.md)); claims there that protect a safety function are referenced from the claims below, and the evidence for the safety functions themselves stays in this document.

## 3. Claims

| ID | Claim | Parent | Status | Evidence | Open defeaters |
|---|---|---|---|---|---|
| G0 | The B601-DM arm on the supervised bench poses no unreasonable risk | — | draft | Sn-01, Sn-02, Sn-03, Sn-04, Sn-19, Sn-20 | 3 |
| G1 | The safety functions reach their required Performance Level | G0 | draft | Sn-05 | 0 |
| G1.1 | SF-32 emergency stop is implemented at PL d | G1 | draft | Sn-06, Sn-07 | 4 |
| G1.2 | SF-08 safe stop on watchdog timeout and SF-25 heartbeat monitor are implemented at PL d | G1 | draft | Sn-08, Sn-09 | 2 |
| G1.3 | SF-24 manual reset after a stop is implemented at PL d | G1 | draft | Sn-06, Sn-07 | 2 |
| G1.4 | SF-03 joint torque and speed limiting is implemented at PL d | G1 | draft | Sn-08, Sn-09 | 2 |
| G1.5 | SF-29 software joint limits with mechanical end-stops are implemented at PL c | G1 | draft | Sn-08, Sn-10 | 2 |
| G1.6 | SF-02 contact-force stop and SF-04 collision detection are implemented at PL d within their sensing limits | G1 | draft | Sn-08, Sn-11 | 2 |
| G1.7 | SF-13 gripper holding on power loss is implemented at PL c | G1 | draft | Sn-12 | 1 |
| G1.8 | SF-14 over-temperature shutdown and SF-11 overcurrent cut-off are implemented at PL c | G1 | draft | Sn-13 | 2 |
| G1.9 | SF-06 reduced speed, SF-15 annunciation and SF-23 jerk limiting are implemented at their PLr for the shared workspace | G1 | draft | Sn-08, Sn-20 | 2 |
| G2 | The complementary electrical and mechanical measures are implemented | G0 | draft | — | 0 |
| G2.1 | The 24 V installation is protected and can be disconnected | G2 | draft | Sn-13 | 5 |
| G2.2 | Pinch points, end-stops, base fixing and part strength are within limits | G2 | draft | Sn-10 | 5 |
| G3 | The command path cannot defeat the safety functions | G0 | draft | — | 0 |
| G3.1 | Motion command paths are authenticated and bounded | G3 | draft | Sn-14, Sn-15 | 3 |
| G3.2 | Learned components are outside every safety function and their outputs are clamped | G3 | draft | Sn-16 | 1 |
| G4 | The evidence was produced under a controlled process | G0 | draft | — | 0 |
| G4.1 | A configuration baseline exists and the software is pinned to it | G4 | draft | Sn-17 | 2 |
| G4.2 | Hazards are identified completely and rated | G4 | draft | Sn-01, Sn-02, Sn-04 | 2 |
| G4.3 | Verification and review evidence exists for the motion-critical software and the record | G4 | draft | Sn-09, Sn-18 | 4 |

## 4. Assumptions of use

AOU-01 to AOU-08 of WP-C-01 §8 apply to every claim. At BL-001 each holds only procedurally.

## 5. Safety functions and Performance Levels

SF-32, SF-08, SF-24, SF-25, SF-03, SF-02, SF-04 and SF-23 at PLr d; SF-06, SF-11, SF-13, SF-14, SF-26, SF-28, SF-29 and SF-30 at
PLr c; SF-15, SF-27 and SF-31 at PLr b (WP-C-03 §7, specified in WP-C-04; the target is DQ-004, open). SF-01 (power-and-force
limiting) is reserved and not claimed (DQ-005). None reaches any PL at BL-001: no safety function exists on the arm.

## 6. Evidence

Status rule: Available = performed and approved at a named baseline; Partial = drafted analysis or
specification, not reviewed; Missing = not yet performed.

**Available 0, Partial 9, Missing 11** (20 evidence items)

| ID | Evidence | Location | Status | Supports |
|---|---|---|---|---|
| Sn-01 | Item definition and limits of the machinery | `assurance/02-concept/WP-C-01-item-definition.md` | Partial | G0, G4.2 |
| Sn-02 | Risk assessment and PLr determination | `assurance/02-concept/WP-C-03-risk-assessment.md` | Partial | G0, G4.2 |
| Sn-03 | Baseline gap assessment GAP-01 to GAP-36 | `assurance/00-assessment/gap-assessment.md` | Partial | G0 |
| Sn-04 | Concept-phase engineering package: preliminary safety case workbook | `reBot_DevArm_Safety_Case.xlsx` | Partial | G0, G4.2 |
| Sn-05 | Safety functions specification SF-32 and the package's control functions: demand, safe state, response, stop category, PLr, allocation | `assurance/02-concept/WP-C-04-safety-functions-and-plr.md` | Partial | G1 |
| Sn-06 | Safety-chain design for the bench build: parts, wiring, I/O, estimated PL | `assurance/04-hardware/WP-H-02-electrical-and-safety-chain-design.md` | Missing | G1.1, G1.3 |
| Sn-07 | Emergency-stop and chain test record (each device, each channel, welded contact, reset held) | `assurance/06-validation/WP-V-04-emergency-stop-and-safety-chain-validation.md` | Missing | G1.1, G1.3 |
| Sn-08 | Controller safety layer architecture: watchdog, mode machine, clamps, plausibility | `assurance/05-software/WP-W-03-software-architecture.md` | Missing | G1.2, G1.4, G1.5, G1.6, G1.9 |
| Sn-09 | Software validation on the target: watchdog timing, clamps, mode transitions, bus-off | `assurance/05-software/WP-W-08-software-validation-on-target.md` | Missing | G1.2, G1.4, G4.3 |
| Sn-10 | Mechanical analysis: mass, fixing, joint gaps, end-stops, part strength | `assurance/04-hardware/WP-H-08-mechanical-analysis.md` | Missing | G1.5, G2.2 |
| Sn-11 | Functional insufficiency analysis of the torque estimator, the camera and the policy | `assurance/02-concept/WP-C-10-functional-insufficiency-analysis.md` | Missing | G1.6 |
| Sn-12 | Stopping performance, joint limit and holding tests | `assurance/06-validation/WP-V-02-stopping-performance-and-holding-tests.md` | Missing | G1.7 |
| Sn-13 | Electrical safety: disconnect, fuse, branch protection, connectors, the supply | `assurance/04-hardware/WP-H-05-electrical-safety.md` | Missing | G1.8, G2.1 |
| Sn-14 | Cybersecurity threat and risk assessment | `assurance/02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md` | Missing | G3.1 |
| Sn-15 | Cybersecurity validation and penetration test of the command paths | `assurance/06-validation/WP-V-06-cybersecurity-validation.md` | Missing | G3.1 |
| Sn-16 | ML component definition and the requirements that keep every policy outside the safety functions | `assurance/02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md` | Missing | G3.2 |
| Sn-17 | Baseline record BL-001 | `assurance/case/baselines/baselines.yaml` | Partial | G4.1 |
| Sn-18 | Safety case WP-K-01 | `assurance/10-safety-case/WP-K-01-safety-case.md` | Partial | G4.3 |
| Sn-19 | Operating environment and task specification: envelopes OE-1 to OE-4, tasks, the bench | `assurance/02-concept/WP-C-02-operating-environment-and-tasks.md` | Partial | G0 |
| Sn-20 | Human-robot interaction, collaborative operation and misuse analysis | `assurance/02-concept/WP-C-06-human-robot-interaction-and-misuse.md` | Partial | G0, G1.9 |

## 7. Defeaters

One defeater per finding of the gap assessment. A defeater closes only through a recorded review that names the
evidence closing it.

| ID | Defeater | Gap | Claims | Status |
|---|---|---|---|---|
| DF-01 | Joint pinch-zone gaps are not analysed | GAP-01 | G2.2 | open |
| DF-02 | Mechanical end-stops exist only where the BOM says so (the joint-1 yaw limit block and the upper- and lower-arm limit blocks, added in v1.1); joints 4 to 6 and the gripper rely on the actuator's own position limits, and no joint has a documented stop angle or a software limit inboard of it | GAP-02 | G1.5, G2.2 | open |
| DF-03 | The mass, the payload moment at reach, the centre of gravity and the base fixing are not specified | GAP-03 | G2.2 | open |
| DF-04 | Load-bearing machined parts are offered as 3D-printable substitutes ("can be 3D printed in ABS with high infill") with no strength analysis, and the printed covers and fingers have no declared material, load case or inspection interval; a cracked cover exposes the joint gap it guards | GAP-04 | G2.2 | open |
| DF-05 | Sharp edges on the sheet-metal brackets and the fastener torque are not specified; the DFMEA rates a loosened fastener as a projectile risk | GAP-05 | G2.2 | open |
| DF-06 | No separation-distance or reach-envelope safeguarding plan exists | GAP-06 | G1.9 | open |
| DF-07 | Whether the gripper holds its grasp on power loss is unknown | GAP-07 | G1.7 | open |
| DF-08 | No emergency stop exists in the documented design | GAP-08 | G1.1, G1.3 | open |
| DF-09 | No supply disconnecting device: the 24 V, 14.6 A supply feeds the XT30 daisy chain directly; there is no lockable disconnect and no fuse between the supply and the harness | GAP-09 | G1.1, G2.1 | open |
| DF-10 | No overcurrent protection per branch | GAP-10 | G1.8, G2.1 | open |
| DF-11 | The mains side is undocumented: the LRS-350-24 is an open-frame supply with exposed mains terminals, and no enclosure, bonding, cord or inlet is specified | GAP-11 | G2.1 | open |
| DF-12 | The arm's 24 V input is not keyed against reverse polarity and has no reverse-polarity protection; the package's own architecture notes a barrel-jack style input it recommends replacing | GAP-12 | G2.1 | open |
| DF-13 | Motor over-temperature protection is the actuator's own closed firmware only | GAP-13 | G1.8 | open |
| DF-14 | No reliability data exists for any part of a safety function | GAP-14 | G1.1 | open |
| DF-15 | EMC immunity and emissions are not declared for the arm or the harness; a disturbed CAN bus is a loss-of-communication event (GAP-18) | GAP-15 | G2.1 | open |
| DF-16 | The software that moves the arm is outside the fork | GAP-16 | G1.2, G1.4, G4.1 | open |
| DF-17 | No operating-mode state machine exists | GAP-17 | G1.3 | open |
| DF-18 | Loss of communication holds the last command | GAP-18 | G1.2 | open |
| DF-19 | Joint speed, torque and momentum limits are not declared per joint and are enforced, where at all, only inside the client library; nothing between a command source and the drive bounds them | GAP-19 | G1.4 | open |
| DF-20 | Software joint limits inboard of the mechanical end-stops are not defined, so a position command can run a joint into its stop or through a singularity | GAP-20 | G1.5 | open |
| DF-21 | No verification evidence exists for any software component | GAP-21 | G4.3 | open |
| DF-22 | Any process with the CAN-USB adapter open can command every joint | GAP-22 | G3.1 | open |
| DF-23 | Tele-operation (the leader arm path, the web UI, the ROS bridge) is unauthenticated and unencrypted; an idle session never locks | GAP-23 | G3.1 | open |
| DF-24 | Learned policies (LeRobot imitation policies, the YOLO grasping demo) run with no independent clamp on their output and no verification against the hazard list; the package's own FMEA rates an out-of-distribution scene as a high-priority failure | GAP-24 | G3.2 | open |
| DF-25 | The wrist camera, where fitted, streams by default and nothing states a retention or recording posture; people at the bench are recorded without a decision | GAP-25 | G3.1 | open |
| DF-26 | Inverse kinematics near the workspace boundary can spike joint speed; the damping is a property of the client library, not of a limit the arm enforces | GAP-26 | G1.6 | open |
| DF-27 | Adequacy of risk reduction is not recorded for 18 of the package's hazards | GAP-27 | G0, G4.2 | open |
| DF-28 | No power-and-force-limiting measurement exists and the body-region thresholds are not bound to joint torque or speed caps, so no collaborative claim (contact permitted) can be made for any envelope | GAP-28 | G1.6 | open |
| DF-29 | No information for use: no operator manual, no limits and warnings, no power-on checklist, no E-stop test procedure, no lock-out, no residual-risk statement; the Seeed wiki covers assembly and software only | GAP-29 | G0 | open |
| DF-30 | No motion-imminent warning exists before a commanded motion; the package asks for an audible or visible signal 500 ms ahead | GAP-30 | G1.9 | open |
| DF-31 | No safety function has been validated | GAP-31 | G1.1, G4.3 | open |
| DF-32 | Design-review, nonconformance and corrective-action records are absent, and test and calibration records are not kept; git history is the only document control | GAP-32 | G4.3 | open |
| DF-33 | Kit assembly has no production controls | GAP-33 | G4.3 | open |
| DF-34 | The B601-RS (RobStride) variant has no released BOM, firmware notes or software; the two variants share the envelope but not the control interface, and nothing detects which is fitted | GAP-34 | G4.1 | open |
| DF-35 | The CC BY-NC-SA 4.0 licence forbids commercial use; a safety-assured build placed in a workplace (the package's OE-3) may be commercial use under upstream's statement, and the record does not yet say which envelopes the licence allows | GAP-35 | G0 | open |
| DF-36 | Repeatability (< 0.2 mm) is declared but no ISO 9283 test pack exists; not a safety gap, but the record's only performance evidence is the upstream thermal test | GAP-36 | G4.2 | open |

## 8. Reviews

None at BL-001.

## 9. Residual risk statement

Not yet possible: no safety function exists on the configuration, so no operation with a person in reach of the arm while it
is powered in RUN is within this case, and hand-guiding in TEACH is within it only once the enabling and reduced-speed measures
of WP-C-06 §4 exist (WP-C-03 §8).

## 10. Open items

| ID | Item | Needed by | Claims |
|---|---|---|---|
| OI-1 | Weigh the arm, record the base fixing (bolts, torque), the centre of gravity and the payload moment at reach | G1 | G2.2, G4.2 |
| OI-2 | Measure every joint gap against ISO 13854 and record each joint's mechanical end-stop angle | G1 | G2.2, G1.5 |
| OI-3 | Test whether a loaded joint and the gripper hold on power loss; decide the stop category of SF-32 from the result | G2 | G1.7, G1.1 |
| OI-4 | Fork the SDK and the ROS 2 driver, pin them in BL-001 and start the controller safety layer (DQ-007, DQ-020) | G0 | G1.2, G4.1 |
| OI-5 | Buy and fit the bench safety chain and the disconnect before any powered test with a person in reach (DQ-006, DQ-018) | G1 | G1.1 |
| OI-6 | A reviewer who has operated the arm confirms every rating in WP-C-03 | G1 | G4.2 |
| OI-7 | Ask Damiao and RobStride for reliability and fault-behaviour data (DQ-019) | G3 | G1.1, G1.8 |
| OI-8 | Decide the collaborative claim (DQ-005) and bound the torque estimator's detection floor in WP-C-10 | G1 | G1.6 |
| OI-9 | Re-rate every WP-C-03 row for OE-1 once the first envelope is decided (DQ-003) | G1 | G4.2 |
| OI-10 | Settle which operating envelopes the non-commercial licence allows a safety-assured build to be used in (GAP-35) | G0 | G0 |
