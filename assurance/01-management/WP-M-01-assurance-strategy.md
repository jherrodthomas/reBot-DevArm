# WP-M-01 Assurance Strategy and Lifecycle Tailoring

| Field | Value |
|---|---|
| Work product | WP-M-01 Assurance strategy and lifecycle tailoring |
| Standard reference | ISO 12100:2010 §4 (strategy for risk assessment and risk reduction); ISO 10218-1:2025 §4 and ISO 10218-2:2025 §4 (risk assessment of the robot and the robot application); ISO 13849-1:2023 §4 (overview, planning); IEC 61508-1:2010 §6 (management of functional safety, tailoring of the lifecycle); IEC 62443-4-1:2018 SM-1 (development process); ISO/IEC TR 5469:2024 (AI in safety functions, informative); UL 4600 (safety case structure, informative); Regulation (EU) 2023/1230 Art. 25 (conformity assessment procedures) |
| Version | 0.1 (initial strategy; 2026-10-20) |
| Status | Draft |
| PL / scope | All (machinery safety, SRP/CS, cybersecurity, ML, process) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); confirmation review of the tailoring rationale by an independent assessor (I3, CR-03) |
| Approver | Project maintainer (acting safety manager). Self-approval at I0 is proposed as a recorded interim limitation until a second person takes the safety manager or reviewer role; it is decision DQ-010 (open, recommended A) |
| Baseline | `206ebda` |

> [!NOTE]
> No standard is held in the drafting environment. Every clause reference in this document is from memory of the
> text and must be checked against a licensed copy before an audit ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1;
> buying the standards is DQ-011).

## 1. Purpose

This document is the assurance path for the reBot-DevArm fork. It sets out:

1. what the fork will claim, and for which configuration of the arm,
2. the safety architecture argument that makes those claims achievable on inherited hardware and on software the
   fork does not yet control,
3. which standards apply to a desktop robot arm, how each one is used and where it is tailored, with rationale,
4. the phases, gates and work products that take the project from today's baseline to a release decision,
5. the strategic decisions the project must take, and the risks to the plan.

The [safety plan (WP-M-02)](WP-M-02-safety-plan.md), [cybersecurity plan (WP-M-08)](WP-M-08-cybersecurity-plan.md),
[ML safety plan (WP-M-09)](WP-M-09-ml-safety-plan.md) and [regulatory conformity strategy (WP-M-13)](WP-M-13-regulatory-conformity-strategy.md)
carry out this strategy for their own disciplines. The [work product register (WP-M-00)](WP-M-00-work-product-register.md)
lists every output. The standards are the machinery set for an industrial robot, because a powered arm with a
650 mm reach on a desk is machinery under Regulation (EU) 2023/1230 and an industrial robot under ISO 10218, however
small it is.

## 2. Starting point

From the [baseline gap assessment](../00-assessment/gap-assessment.md), at the commit in its header:

- **The fork carries a concept-phase engineering package and no engineering change.** The package of 2026-05-04
  (safety case, DFMEA, requirements, architecture, test plan, trace memo) is a sound scaffold: 33 hazards, 31
  safety-function candidates, 104 requirements, 127 test cases. It is an input to this record, not evidence; none
  of its tests has run and none of its analyses has been reviewed.
- **No safety function reaches any Performance Level.** The arm as inherited has no emergency stop in its BOM, no
  supply disconnect, no fuse, no watchdog between the host and the actuators and no operating-mode state machine.
  The only stop is a software command on the same CAN bus that drives the motors (GAP-08, GAP-09, GAP-17, GAP-18).
- **The software that moves the arm is outside the fork.** The `motorbridge` SDK, the ROS 2 driver, the LeRobot
  and Pinocchio integrations and the web UI live in upstream repositories; nothing is pinned to the hardware
  baseline and the only firmware is the actuators' closed firmware (GAP-16).
- **The architecture is the right shape.** A host stack sends commands over one bus to actuators with their own
  position, speed and torque control; a safety layer between the host and the bus, and a hardwired chain on the
  motor supply below both, fit without redesigning the arm.
- **The limits that everything hangs on are unmeasured.** Mass, fixing, joint gaps, end-stop angles, stopping time
  and the contact force the arm can exert are all unknown (GAP-01, GAP-02, GAP-03, GAP-28).
- **Anyone with the adapter can move the arm.** The CAN bus carries no authentication, the host has no access
  control and tele-operation is unauthenticated (GAP-22, GAP-23).
- **A second variant is coming.** The B601-RS with RobStride actuators shares the envelope but not the control
  interface, and has no released BOM (GAP-34).

## 3. What the fork will claim

### 3.1 Reference configuration: the only scope claims apply to

| Element | Reference configuration |
|---|---|
| Arm | **CFG-001, the reBot Arm B601-DM v1.1**: six Damiao V4 actuators (4 × DM4310, 3 × DM4340P; joint 1 a DM4340P since v1.1), one gripper actuator, sheet-metal and CNC aluminium links, 3D-printed covers and fingers, one CAN daisy chain on XT30 2+2 cables, a DM CAN-USB adapter, a MEAN WELL LRS-350-24 supply, **plus the bench safety chain the fork adds before any powered test with a person in reach** (§6.2, [WP-V-07](../06-validation/WP-V-07-test-operations.md)). Recorded as `CFG-001` in the Living Safety Case |
| Function | Position, velocity and torque control of the six joints and the gripper from a host PC in modes M-01 OFF, M-02 IDLE, M-03 TEACH, M-04 RUN, M-05 ESTOP; tele-operation from a leader arm; execution of learned policies in RUN behind the clamps (DQ-008, recommended A) |
| Software | Once forked (DQ-007, recommended A): a tagged fork release that pins the SDK, the ROS 2 driver, the policy runtime and every dependency by commit; until then the upstream software at a recorded version, hardened by nothing |
| Operating environment | **OE-1 only** (DQ-003, recommended A): a supervised laboratory bench, the arm fixtured, nobody but the operator inside the 650 mm reach while the arm is enabled, defined in [WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md) |
| Operator | A trained operator with a hand on the bench E-stop during development ([WP-V-07](../06-validation/WP-V-07-test-operations.md)); after release, personnel briefed per [WP-O-03](../09-production-operation/WP-O-03-information-for-use.md) |

The choice of the B601-DM over the B601-RS is decision DQ-001 (recommended A, open). The RS variant is tracked as
`CFG-002`, every value unverified, and joins the claimed scope through an impact analysis
([WP-M-11](WP-M-11-impact-analysis.md)) when its BOM is released (DQ-017). Any other configuration, including an arm on a
mobile base, a second arm, or a non-upstream gripper, needs the same.

### 3.2 Top-level claim

> **G0**: The reBot-DevArm reference configuration (CFG-001), operated within its operating-envelope limits by
> personnel briefed as its information for use requires, does not expose people to unacceptable risk. The residual
> risk after the three-step method of ISO 12100 is acceptable for the machine's intended use and reasonably
> foreseeable misuse.

Sub-claims that structure the [safety case (WP-K-01)](../10-safety-case/WP-K-01-safety-case.md):

| Sub-claim | Standards | Core argument |
|---|---|---|
| G1 Every safety function achieves its required Performance Level | ISO 13849-1/-2, EN 60204-1, ISO 13850, ISO 10218-1 | The safety functions (WP-C-04) are implemented by a hardwired safety chain and a controller safety layer whose category, MTTFD, DCavg and CCF are calculated (WP-H-04) and validated (WP-V-01…V-05), and the host stack above them cannot defeat them (WP-A-05) |
| G2 The complementary electrical and mechanical measures are implemented | EN 60204-1, ISO 13854, ISO 12100 | The supply is disconnectable, fused and SELV (WP-H-05); the joint gaps, end-stops, base fixing and printed parts are analysed and within limits (WP-H-08) |
| G3 The command path cannot defeat the safety functions | IEC 62443-4-1/-4-2, ISO/IEC TR 5469 | Every motion command path is authenticated and bounded (WP-C-08, WP-S-07); learned components are usage level "outside the safety function" (WP-C-09) and every policy output passes the same clamp as any other command |
| G4 The evidence was produced under a controlled process | IEC 61508-1 §6, §8; ASPICE | A baseline exists and the forks are pinned to it (WP-P-01); the hazards are identified completely and rated (WP-C-03); verification and review evidence exists for the motion-critical code (WP-W-06, WP-P-05) |

**No claim is made, now or as a target, for a person inside the reach envelope while the arm is enabled, for
contact with a moving arm (no power-and-force-limiting claim unless DQ-005 changes it), for the B601-RS variant,
for an arm on a mobile base, or for any configuration outside §3.1.**

## 4. The standards and how each one is used

reBot-DevArm is machinery and an industrial robot. The method is one hazard log, one requirements database,
generated figures and a Living Safety Case; the standards that feed it are these.

| Question | Answered with | Where |
|---|---|---|
| What are the hazards and how much risk reduction does each need? | **ISO 12100** risk assessment (three-step method); **ISO 10218-1 Annex A** and **ISO 10218-2 Annex A** lists of significant hazards for robots and robot applications; required **Performance Level** from the ISO 13849-1 Annex A risk graph | WP-C-01, C-03, C-04, C-05 |
| Which safety functions must the arm have? | **ISO 10218-1 §5**: emergency stop, protective stop, safety-rated monitored stop, speed and force limiting, axis limiting, enabling device in manual mode, operational modes; **ISO 13850** for the emergency stop; **EN 60204-1 §9** for stop categories | WP-C-04 |
| May a person touch or share space with the arm? | **ISO 10218-2:2025 §5** and **ISO/TS 15066** (where the 2025 text is not held): safety-rated monitored stop, speed and separation monitoring, hand guiding, power and force limiting with body-region thresholds. The first case claims **separation only** (DQ-005, recommended A) | WP-C-06, S-04, V-03 |
| How good must the control system be, and how is that shown? | **ISO 13849-1** categories B to 4, MTTFD, DCavg, CCF, PL a to e; **ISO 13849-2** validation and fault lists; **IEC 62061 / IEC 61508** where 13849 runs out (software beyond 13849-1 §7, management, assessment) | WP-S-02…S-05, WP-H-01…H-07, WP-W-01…W-09, WP-V-01…V-05 |
| Is the electrical installation safe? | **EN 60204-1**: supply disconnecting device, overcurrent protection, protection against electric shock, control circuits, verification; the 24 V bus as SELV | WP-H-02, H-05 |
| Where may a person be, and how small must a gap be? | **ISO 13855** approach speeds and separation distances; **ISO 13857** reach distances; **ISO 13854** minimum gaps to avoid crushing | WP-C-06, S-04, H-08, V-03 |
| What if nothing fails but the arm does not sense the contact? | No machinery standard covers performance limits of estimation and perception. **ISO 21448 is used as an informative method** (triggering conditions, known and unknown scenarios) inside WP-C-10 and WP-V-08; the resulting limits become operating-envelope limits or safety functions | WP-C-10, V-08 |
| What if someone attacks it? | **IEC 62443-4-1** (secure development lifecycle) and **62443-4-2** (component requirements, security level target DQ-013); 62443-3-2 for the zone and conduit model | WP-M-08, C-07, C-08, S-07, W-11, V-06, O-05 |
| How far can a learned component be trusted? | **ISO/IEC TR 5469**: AI technology class and usage level; the fork's position is that no learned component implements a safety function. **AI Act** Annex I lists the Machinery Regulation, so a learned safety component would be a high-risk AI system | WP-M-09, C-09, W-10, K-07 |
| Is the whole argument convincing? | **UL 4600** principles for the safety case; the Living Safety Case records and generators | WP-K-01, `case/` |
| What does the law require? | **Regulation (EU) 2023/1230** (Machinery Regulation, applies from 20 January 2027): essential health and safety requirements (Annex III), technical documentation (Annex IV), conformity assessment (Art. 25, Annexes VI–X) with third-party assessment mandatory for machinery with self-evolving safety behaviour (Annex I Part A); **Regulation (EU) 2024/1689** (AI Act) for a learned safety component. The frame itself is DQ-002 | WP-M-13, K-02, K-06, K-07 |
| Are the processes capable? | **ASPICE 4.0** kept as the process capability frame (self-assessment), because no machinery-specific process model exists | WP-M-12 |

How each standard is cited: work products are structured after these standards and cite their clauses. **No
compliance is claimed**, because no assessment has been performed and the drafting environment has no licensed copy
of any standard (WP-M-06 OI-1). The wiki page [How we use each standard](../../wiki/How-we-use-each-standard.md)
is the plain-language version of this table.

## 5. Tailoring

The machinery standards assume a manufacturer placing a finished machine on the market. The fork is an open-source
assurance record for a kit designed and sold by someone else, under a licence that forbids commercial use. The table
records each tailoring decision. Each one needs confirmation review by an independent assessor (CR-03).

| # | Topic | Decision | Rationale |
|---|---|---|---|
| T-01 | Lifecycle entry | Treat the fork as a **modification of existing machinery**: impact analysis ([WP-M-11](WP-M-11-impact-analysis.md)), then a full concept phase. The concept-phase package is an input to every concept work product, never a reused safety work product | Upstream has no risk assessment, safety functions or validation; the package is unreviewed and its tests have not run |
| T-02 | Machine boundary | The machine is the arm as delivered, its supply, its host and the safety hardware the fork adds. The workbench, the site network, the leader arm and the wrist camera's downstream consumers are outside the machine, with interface assumptions | The fork controls the arm, its supply and its software once forked; it does not control the bench or the network |
| T-03 | Safety function allocation | **The functions that remove motor power (SF-32 emergency stop, SF-24 manual reset, SF-08 safe stop as the enforced stop) are implemented by the hardwired safety chain.** The limit and monitoring functions (SF-03, SF-25, SF-28, SF-29, SF-02, SF-04) sit on the controller safety layer, which initiates a stop the chain enforces. **No safety function is allocated to a learned component**; every policy output passes the same clamp as any other command. Where the controller layer runs is DQ-020 | Keeps the PL d argument inside components with certificates and known reliability data; keeps the host stack and the policies out of every safety function |
| T-04 | The host stack | The SDK, the ROS 2 driver, the policy runtime and the UI are functional software with **no PL claim**. They are hardened as defence in depth once forked (authentication, bounded commands, the mode state machine mirrored) so that the safety layer and the chain are rarely demanded | The host is a general-purpose computer running unverified third-party code; a PL claim on it would need a lifecycle the project cannot run |
| T-05 | Hardware | Safety components are bought with certificates (safety relay, contactor with mirror contact, E-stop devices, enabling device) and qualified under ISO 13849-1 as well-tried or certified components; the actuators, the adapter and the supply are treated as not safety-related and the chain removes power upstream of them | No supplier reliability data exists for the actuators (GAP-14, DQ-019) |
| T-06 | Proven in use | **Not claimed** for any element. Upstream's thermal test and the community's run history are supporting evidence only ([WP-P-09](../07-supporting/WP-P-09-proven-in-use.md)) | No controlled configuration or field-problem history that would meet IEC 61508 |
| T-07 | Production | Tailored to assembly, commissioning and configuration control of a kit ([WP-O-01](../09-production-operation/WP-O-01-assembly-installation-commissioning.md)). The fork manufactures nothing; the pre-assembled arm is treated as a kit assembled by upstream | The arm is built by whoever follows the instructions; the instructions and the commissioning checks are the product |
| T-08 | Upstream | Seeed Studio is treated as an upstream supplier with no development interface agreement; the supplier-side activities fall to the fork ([WP-M-10](WP-M-10-upstream-and-supplier-management.md)). `hardware/` is upstream's record and is only merged, never edited | Upstream is under no contract and the fork must not imply its endorsement |
| T-09 | Independence | Verification reviews may be done by project members (I0/I1), never by the author. With one maintainer, I1 review needs a second person and self-review is recorded as I0. Confirmation reviews of the risk assessment, the safety plan and the safety case, and the functional safety assessment, need an **external** assessor (I2/I3) ([WP-M-06](WP-M-06-confirmation-measures-plan.md)) | One maintainer today; the assessor is DQ-009 |
| T-10 | Performance limits of sensing | ISO 21448 is used as a method, not a standard to comply with, inside WP-C-10 and WP-V-08 | No machinery standard covers what a current-based torque estimator or a learned policy cannot sense, and the worst contact hazards (GAP-28, GAP-24) are performance limits, not faults |
| T-11 | Cybersecurity scope | IEC 62443-4-1 practices are applied to the fork's software repositories; IEC 62443-4-2 component requirements to the arm with its host as one component at the security level target of DQ-013. The site network, the operator's other computers and the cloud behind the web UI are external zones | The fork controls the arm's software and configuration, not the network it is deployed on |
| T-12 | Process capability | ASPICE 4.0 is used for a self-assessment of process capability ([WP-M-12](WP-M-12-process-capability-baseline.md)), target CL2 for management, support, system and software processes, CL1 for hardware and ML. No ASPICE assessment is claimed | Gives the fork a process model the robotics standards lack |
| T-13 | Regulatory | EU frame recommended (DQ-002): Machinery Regulation and the harmonised route through ISO 10218-1/-2 and ISO 13849-1. The conformity module is DQ-012 (Module A recommended). The AI Act applies only if a learned component becomes a safety component, which T-03 avoids | Where the arm is sold; one technical file |
| T-14 | Variants and other items | The B601-RS is a second **configuration** (CFG-002) of the same item, tracked and unverified until its BOM is released (DQ-001, DQ-017). An arm on a mobile base, a dual-arm set-up or a non-upstream end effector is a separate **item** with its own risk assessment | The RS shares the envelope but not the actuator limits or bus protocol; a base changes every hazard |

## 6. Safety architecture argument: the central strategy

### 6.1 Doer, checker, and a checker of last resort

```
 ┌──────────────── reBot Arm B601-DM ──────────────────────────────────────────────────────┐
 │  Host PC (layer 1)                  Controller safety layer (layer 2)   Hardwired chain  │
 │  ┌──────────────────────────────┐   ┌──────────────────────────────┐   (layer 3, SRP/CS)│
 │  │ motorbridge SDK, ROS 2 +     │   │ watchdog + heartbeat         │   ┌──────────────┐ │
 │  │ MoveIt 2, Pinocchio, LeRobot │──▶│ mode machine OFF/IDLE/TEACH/ │──▶│ E-stop (x2)  │ │
 │  │ policies, leader-arm teleop, │USB│ RUN/ESTOP; per-joint clamps  │CAN│ enabling dev.│─┼─▶ contactor on
 │  │ web UI, wrist camera         │◀──│ on position/torque/speed;    │◀──│ safety relay │ │   the 24 V motor
 │  └──────────────────────────────┘   │ encoder plausibility; clamp  │   │ fuse, lockable│ │   supply
 │        FUNCTIONAL (no PL claim)     │ on every learned output      │   │ disconnect   │ │
 │                                     └──────────────────────────────┘   └──────────────┘ │
 │                                       initiates stops; PL c/d functions   PL d target   │
 └─────────────────────────────────────────────────────────────────────────────────────────┘
          Operator: hand on the bench E-stop during development (WP-V-07)
          Environment: fixtured arm, nobody but the operator in reach (WP-C-02, OE-1)
```

- **Doer:** the host stack. It decides where the arm goes and how fast. Everything it sends is a request. It is
  functional software from upstream and the community; it is hardened once forked so that the layers below are
  rarely demanded, but no safety function is allocated to it (T-04).
- **Checker:** the controller safety layer. The last software before the bus. It validates every command (finite,
  bounded, fresh), clamps it to the per-joint position, torque and speed limits of the active mode, checks the
  encoders for plausibility, times out the host, and holds the mode state machine. The limit and monitoring
  functions (SF-03, SF-25, SF-28, SF-29, SF-02, SF-04) live here at PL c or d; whether it runs on a dedicated
  controller between the host and the bus or inside the forked SDK is DQ-020 (dedicated controller recommended).
- **Checker of last resort (SRP/CS):** the hardwired safety chain. Two-channel E-stop and enabling inputs feed a
  safety relay whose output drops a contactor with a mirror contact on the 24 V motor supply, behind a fuse and a
  lockable disconnect. Nothing in software can hold the contactor closed. This is where the PL d argument for the
  emergency stop (SF-32), the manual reset (SF-24) and the enforced safe stop (SF-08) is made, with certified
  components and calculated MTTFD, DCavg and CCF.

### 6.2 Consequences that shape the plan

1. **The hardware does not exist yet.** The arm has no chain at all. The first engineering act of the fork is the
   bench safety chain (a fuse, a lockable disconnect, a dual-channel E-stop through a safety relay and a contactor)
   before any powered test with a person in reach ([WP-V-07](../06-validation/WP-V-07-test-operations.md), gap
   assessment §9 action 2, decision DQ-006).
2. **The software is not the fork's yet.** No watchdog, mode machine, clamp or authentication can be built until the
   SDK and driver are forked or a dedicated controller is placed in the bus (DQ-007, DQ-020). Until then the chain
   is the only measure and the arm is bench-only.
3. **Separation, not contact, is the first claim.** Without force and pressure measurement (GAP-28) no
   power-and-force-limiting claim can be made. The first case keeps every person outside the reach envelope while the
   arm is enabled (DQ-003, DQ-005); contact detection (SF-02, SF-04) is defence in depth, bounded by what the
   torque estimator cannot sense ([WP-C-10](../02-concept/WP-C-10-functional-insufficiency-analysis.md)).
4. **Stopping performance is the number everything hangs on.** Separation distances (ISO 13855), the speed caps
   and the stop category all derive from a measured stopping time and angle per joint that nobody has measured.
   [WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md) owns the budget;
   [WP-V-02](../06-validation/WP-V-02-stopping-performance-and-holding-tests.md) measures it.
5. **Independence of the chain from the host is the hinge.** The chain shares the supply, the bench and the
   operator with the host. The shared 24 V rail, the adapter, and a safety layer that may run on the same computer as
   the policy runtime are each analysed in [WP-A-05](../08-analyses/WP-A-05-independence-of-the-safety-chain.md).
6. **The limits are unmeasured.** Mass, fixing, joint gaps and end-stop angles (GAP-01…GAP-03) are measured in P1
   so that the risk assessment rates something real ([WP-H-08](../04-hardware/WP-H-08-mechanical-analysis.md)).

## 7. Phases, gates and sequence

The lifecycle has seven phases, each closed by a gate; gate names and exit criteria are in
[WP-M-00 §2](WP-M-00-work-product-register.md#2-gates), the activities per phase in [WP-M-02 §4](WP-M-02-safety-plan.md#4-lifecycle-activities-per-phase),
and the integrated maps in the [process model (WP-P-11)](../process/README.md).

| Phase | Gate | What it settles | Hold points |
|---|---|---|---|
| P0 Governance | G0 | Plans, roles, configuration control, the configuration (DQ-001), the frame (DQ-002), the software fork (DQ-007), the assessor (DQ-009) | None; nothing is powered under the fork |
| P1 Concept | G1 | Machine limits, operating envelope (DQ-003), risk assessment, safety functions with PLr (DQ-004), the collaborative claim (DQ-005), risk reduction concept, cybersecurity and ML concepts, test operations | **Hold point:** no powered test with a person in reach without the bench safety chain and WP-V-07 approved |
| P2 System design | G2 | SRS, chain architecture and category, response-time and separation budget, I/O map, mechanical analysis, system analyses | |
| P3 HW/SW development | G3 | Chain hardware and PL calculation, the safety layer, software verification, qualification of components and tools | |
| P4 Integration and verification | G4 | Integration, PL verification, stopping, holding, separation and E-stop tests, fault injection | **Hold point:** no person inside the reach envelope with the arm enabled before WP-V-03 passes |
| P5 Validation and release | G5 | Validation on the arm, cybersecurity validation, safety case, assessment, technical file, release record | |
| P6 Operation | G6 | Field monitoring, incident response, updates | |

## 8. Strategic decisions

Each decision is asked of the project lead through the [decision register](decisions/README.md); this table is the
index, the register entry is the question. None of batch 1 is answered at this version.

| # | Decision | Register | Status |
|---|---|---|---|
| D-01 | Reference configuration: the B601-DM now, the RS tracked | DQ-001 | Open, batch 1 (recommended A) |
| D-02 | Regulatory frame: EU machinery | DQ-002 | Open, batch 1 (recommended A) |
| D-03 | First operating envelope: the supervised bench only | DQ-003 | Open, batch 1 (recommended A) |
| D-04 | Required PL for the stop functions: PL d | DQ-004 | Open, batch 1 (recommended A) |
| D-05 | Collaborative claim: separation only, no PFL | DQ-005 | Open, batch 1 (recommended A) |
| D-06 | Bench safety chain before any powered test with a person in reach | DQ-006 | Open, batch 1 (recommended A) |
| D-07 | Fork the software that moves the arm | DQ-007 | Open, batch 1 (recommended A) |
| D-08 | Learned policies in the item, outside every safety function | DQ-008 | Open, batch 1 (recommended A) |
| D-09 | Independent assessor: when | DQ-009 | Open, batch 1 (recommended A, not for now) |
| D-10 | Roles and self-approval while the project has one person | DQ-010 | Open, batch 1 (recommended A) |
| D-11 | Buying the standards | DQ-011 | Queued |
| D-12 | Conformity assessment route and module | DQ-012 | Queued (Module A recommended) |
| D-13 | Cybersecurity security level target | DQ-013 | Queued |
| D-14 | Camera privacy default | DQ-014 | Queued |
| D-15 | Gripper holding on power loss | DQ-015 | Queued |
| D-16 | Torque and speed ceilings for the bench envelope | DQ-016 | Queued (decider: claude) |
| D-17 | The RS variant as a second configuration | DQ-017 | Queued |
| D-18 | Supply disconnecting means | DQ-018 | Queued |
| D-19 | Supplier reliability data request | DQ-019 | Queued |
| D-20 | Where the controller safety layer runs | DQ-020 | Queued |

## 9. Risks to the plan

Project risks are managed in [WP-M-07](WP-M-07-risk-management.md). The ones that shape this strategy:

| Risk | Effect | Response |
|---|---|---|
| The lead cannot fund the bench chain (relay, contactor, devices, disconnect) | No stop that removes power without software; every test runs with the arm caged or nobody in reach | DQ-006 option C is a defensible fallback; the record stays bench-only and says so |
| One person holds every role | No I1 review, no confirmation measure, self-approval everywhere | T-09; DQ-009, DQ-010; verification reviews by any second contributor count |
| The software stays upstream | No watchdog, mode machine, clamp or authentication can exist in the case | DQ-007 option B (a dedicated controller) gives a safety layer without a software fork |
| No supplier reliability data for the actuators | No PL calculation closes on a channel that includes an actuator | T-05: the chain removes power upstream of the actuators; DQ-019 asks anyway |
| The standards are not available to the authors | Clause numbers wrong; the 2025 editions of ISO 10218 changed the collaborative text | DQ-011; every clause reference marked to check; WP-M-06 OI-1 |
| The non-commercial licence | A safety-assured build used in a workplace may be commercial use upstream forbids (GAP-35) | WP-M-13 §2; the record places nothing on the market and names the envelopes it covers |
| The Machinery Regulation's AI provisions pull a learned component into Annex I Part A | Mandatory third-party conformity assessment and an AI Act file | T-03 keeps learned components outside every safety function; WP-M-13 §5 tracks the threshold |

## 10. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Apply the batch-1 answers (DQ-001…DQ-010) to §3.1, §5 and §8 when they arrive | Safety manager | G0 |
| OI-2 | Replace the text diagram of §6.1 with a generated figure pinned to §6.1 and §6.2 so CI detects when it may be stale | Safety manager | G1 |
| OI-3 | Confirm the tailoring table with the assessor once engaged (DQ-009) | Safety manager | G1 |
| OI-4 | Check every clause reference against a licensed copy once the standards are bought (DQ-011); revise §4 for the 2025 text of ISO 10218-1/-2 | Safety manager | G1 |
| OI-5 | Add CFG-002 rows to §3.1 when the RS BOM is released (DQ-017) | Safety manager | G1 |
