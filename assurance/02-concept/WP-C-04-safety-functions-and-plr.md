# WP-C-04 Safety functions specification with required Performance Level, stop category and response time

| Field | Value |
|---|---|
| Work product | WP-C-04 Safety functions specification with required Performance Level, stop category and response time |
| Standard reference | Machinery: ISO 10218-1:2025 §5 (safety-related control functions, emergency stop, protective stop, limiting); ISO 13850:2015 §4; SRP/CS: ISO 13849-1:2023 §5, Annex A (PLr); Other: EN 60204-1:2018 §9.2 (stop categories); ISO/TS 15066:2016 §5 (collaborative modes); ASPICE: SYS.2 |
| Version | 0.1 (2026-10-20): SF-32 and the 19 control functions of the package specified at concept level (demand, safe state, response target, stop category, PLr, allocation, modes); SF-01 reserved and not claimed; response targets are the package's and are budgets, not measurements |
| Status | Draft |
| PL / scope | PL d target for SF-32, SF-08, SF-24, SF-25, SF-03, SF-02, SF-04, SF-23 (DQ-004 open, recommended A); PL c and b for the rest; CFG-001 in OE-1 |
| Author | Assurance team (AI-assisted draft, I0), from the package of J. Herrod-Thomas (2026-05-04) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 |

> [!WARNING]
> Draft. The functions are specified at concept level from the hazards and ratings of [WP-C-03](WP-C-03-risk-assessment.md) and the
> scenarios of [WP-C-06](WP-C-06-human-robot-interaction-and-misuse.md). Every response time is a target the package proposed; every
> stopping time and angle is **(TBC)** until [WP-V-02](../06-validation/WP-V-02-stopping-performance-and-holding-tests.md) measures it. None
> of these functions exists on the arm at BL-001. Clause references are to be checked against licensed copies (DQ-011).

## 1. Purpose

Specifies the safety functions of the arm (ISO 13849-1 §5): for each, the demand, the safe state, the response time, the stop
category (EN 60204-1 §9.2), the required Performance Level, the layer that implements it, and the modes it applies in. SF-nn
identifiers are the package's and are never reused; SF-32 is new. [WP-S-02](../03-system/WP-S-02-safety-requirements.md) breaks each
into testable requirements SR-nn.mm; [WP-S-03](../03-system/WP-S-03-technical-safety-concept.md) designs the safety-related parts;
[WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md) budgets the response times and stopping performance.

Conventions: a **demand** is the event the function must respond to; the **safe state** is what it achieves and holds; the
**response time** runs from the demand at the device or the measurement to the start of power removal or the controlled stop at the
drive input; **standstill** adds the stopping time, unmeasured. Stop categories per EN 60204-1 §9.2.2: category 0 is immediate removal
of power (every joint goes limp under gravity unless its actuator holds, which is unknown, GAP-07); category 1 is a controlled stop
with power removed when stopped. **Layers:** `chain` the hardwired safety chain; `layer` the controller safety layer (DQ-020);
`host` the host stack, hardened, no PL claim; `hardware` a mechanical property.

## 2. Safety functions

| ID | Safety function | Demand | Safe state | PLr | Cat. | Stop cat. | Response target | Layer |
|---|---|---|---|---|---|---|---|---|
| SF-32 | Emergency stop | A person actuates the pendant or bench emergency-stop device | Motor supply removed by the contactor; every joint unpowered; the gripper holds (SF-13); latched until a deliberate reset (SF-24) | d | 3 | 0 | ≤ 200 ms to power removal | chain |
| SF-08 | Safe stop on watchdog timeout | The controller safety layer sees no valid command for 250 ms, the host heartbeat is lost (SF-25), the control loop misses its deadline, or the motor bus goes bus-off twice within 1 s | Controlled stop of every joint, then motor supply removed by the chain if standstill is not reached within 300 ms; latched | d | 3 | 1 then 0 | ≤ 100 ms after the timeout | layer+chain |
| SF-24 | Manual reset after a stop (prevention of unexpected start-up) | An emergency stop or a safe stop has latched, or power returns after a loss | No joint moves until a deliberate reset on the pendant with every E-stop released and the host in IDLE; release of the E-stop alone does not restart | d | 3 | — | n/a (a state, not a reaction) | chain |
| SF-25 | Heartbeat and deadline monitor | The host does not send its heartbeat within 250 ms, or the safety layer's own loop overruns | As SF-08 | d | 3 | 1 then 0 | ≤ 50 ms to detection | layer |
| SF-03 | Joint torque and speed limiting per joint | A commanded or measured joint torque or speed exceeds the limit of the active mode and envelope (DQ-016) for more than 10 ms | Command clamped at the limit; a measured exceedance for more than 100 ms stops the joint (SF-08 path) | d | 3 | 1 | ≤ 10 ms clamp; ≤ 100 ms stop | layer |
| SF-02 | Contact-force stop | The estimated external torque on any joint exceeds the contact threshold of the active mode | Controlled stop of every joint and hold; resumes only on operator command | d | 3 | 1 | ≤ 50 ms | layer |
| SF-04 | Collision detection by torque estimation | The difference between commanded and measured joint torque, corrected for gravity and friction, exceeds the detection threshold | As SF-02 | d | 3 | 1 | ≤ 100 ms | layer |
| SF-23 | Trajectory jerk limit for transient contact | A commanded trajectory exceeds the jerk or acceleration limit of the active mode | Command shaped or refused; never reaches the drive | d | 3 | — | ≤ 50 ms | layer |
| SF-01 | Power-and-force limiting (ISO/TS 15066) | Not claimed in the first safety case (DQ-005, recommended A). If claimed: the predicted contact force or pressure for the active body region exceeds the ISO/TS 15066 threshold | Speed and torque caps per body region; contact stop (SF-02) | d | 3 | 1 | ≤ 100 ms | layer |
| SF-06 | Reduced speed in the shared workspace | The envelope or mode declares a person may be in reach (OE-2 and above; TEACH) | Joint speed capped at the reduced-speed limit (DQ-016) | c | 2 | — | ≤ 200 ms | layer |
| SF-11 | Overcurrent cut-off per branch | A branch current exceeds its rating | The fuse or electronic breaker opens that branch | c | 2 | 0 | ≤ 50 ms | chain |
| SF-13 | Gripper holding on power loss | Motor power is removed (SF-32, SF-08) or lost | The gripper keeps its grasp (brake or non-back-drivable drive) for payloads above the limit of DQ-015 | c | 2 | — | static | hardware |
| SF-14 | Stator over-temperature shutdown | An actuator reports stator temperature above the warning threshold (75 °C proposed) or the shutdown threshold (90 °C, upstream's protection) | Torque reduced at the warning threshold; controlled stop and hold at the shutdown threshold | c | 2 | 1 | ≤ 200 ms | layer |
| SF-15 | Motion-imminent annunciation | A transition into RUN or a motion start after a stop | Audible or visible signal at least 500 ms before motion | b | 1 | — | continuous | host |
| SF-26 | Authenticated command channel | A motion command arrives over the network or from a client | Unauthenticated or unsigned commands are discarded | c | 2 | — | ≤ 100 ms | host |
| SF-27 | Operator session lock | 30 s without operator input in a tele-operation session | Session locked; re-authentication required | b | 1 | — | ≤ 30 s | host |
| SF-28 | Encoder plausibility cross-check | A joint's reported position disagrees with its commanded motion or with the integrated velocity beyond the plausibility window | Joint stopped (SF-08 path) and the fault latched | c | 2 | 1 | ≤ 50 ms | layer |
| SF-29 | Software joint limits with mechanical end-stops | A position command or a measured position passes the software limit, set at least 5° inboard of the mechanical end-stop | Command clamped; a measured exceedance stops the joint | c | 2 | 1 | ≤ 10 ms | layer |
| SF-30 | Singularity avoidance in inverse kinematics | The planned trajectory approaches a kinematic singularity | Damped least-squares solution; joint speed stays within SF-03 | c | 2 | — | ≤ 10 ms | host |
| SF-31 | Camera default-off and opt-in recording | The arm powers up with a camera fitted | Stream off; recording opt-in with a visible indicator; local storage (DQ-014) | b | 1 | — | n/a | host |

## 3. Specification per function

### 3.1 SF-32 Emergency stop

- **Devices:** a mushroom-head latching button on the operator's pendant and one on the bench, each with two NC contacts.
- **Chain:** both channels into a safety relay with monitored manual reset; the relay drops a contactor with a mirror contact on the
  24 V motor supply. No software is in the path; the host and the safety layer are informed through the diagnostic signals of
  [WP-S-05](../03-system/WP-S-05-safety-chain-io-interface.md) and may not override it.
- **Stop category 0** (DQ-004 context): power is removed immediately. The consequence for a loaded arm is that every joint without a
  brake falls under gravity; whether the Damiao actuators hold is unknown (GAP-07) and is measured in WP-V-02. If they do not, a
  category 1 stop (SF-08 first, then power removal) is the better E-stop and this section changes; recorded as OI-1.
- **Modes:** all. **Reset:** SF-24.

### 3.2 SF-08 Safe stop on watchdog timeout

- **Demand sources:** no valid command for 250 ms (package SRS-002: a command is valid if finite, within limits and fresh); the host
  heartbeat lost (SF-25); the safety layer's loop overruns; bus-off twice within 1 s (package SRS-009).
- **Reaction:** a controlled stop of every joint by the safety layer (category 1), then, if standstill is not reached within 300 ms,
  the safety layer opens the chain's enable input so the contactor removes power. The function is therefore allocated to the layer
  and the chain together; the PL d claim rests on the chain path, the layer path is the first channel.
- **Modes:** IDLE, TEACH, RUN.

### 3.3 SF-24 Manual reset after a stop

A deliberate action on the pendant with every E-stop device released and the host in IDLE; release of a button alone never
restarts motion (package SYRS-006, HZ-P04). Power return after a loss lands in OFF, never in the previous mode. Modes: all.

### 3.4 SF-25 Heartbeat and deadline monitor

The host sends a heartbeat at 4 Hz or faster; the safety layer expects it within 250 ms and monitors its own loop period, reacting
through SF-08 (package SRS-001, SRS-002). Modes: IDLE, TEACH, RUN.

### 3.5 SF-03 Joint torque and speed limiting per joint

Per-joint limits per mode and envelope (the ceilings of DQ-016 until measured) enforced by the safety layer on every command and
checked against the measured values (package SYRS-003, SYRS-004). An exceedance of the measured value for more than 100 ms is a
fault handled by SF-08. The actuators' own limits are a backstop, not a channel. Modes: TEACH (reduced), RUN.

### 3.6 SF-02 Contact-force stop and SF-04 collision detection

Both rest on the external torque estimated from motor current, gravity and friction models: there is no joint torque sensor.
The sensing limits of SF-02 and SF-04 are settled in WP-C-10: a contact that produces less current than the estimation noise is
not detected, and the threshold that can be set without nuisance stops bounds the force at which the arm reacts. In OE-1 these
functions are defence in depth; they become a claim only with the measurement campaign of DQ-005 B. Modes: TEACH, RUN.

### 3.7 SF-23 Trajectory jerk limit

Commands are shaped to the jerk and acceleration limits of the mode before they reach the drive (package SF-23). Modes: RUN.

### 3.8 SF-01 Power-and-force limiting

Reserved. Not claimed in the first safety case (DQ-005, recommended A). If the lead chooses B, this section specifies the body-region
thresholds of ISO/TS 15066 Annex A, the joint torque and speed caps derived from the measurement, and the contact stop (SF-02) as the
reaction.

### 3.9 PL c and PL b functions

| ID | Specification note |
|---|---|
| SF-06 | The reduced-speed cap of DQ-016 whenever the mode or envelope allows a person in reach; in OE-1 that is TEACH only |
| SF-11 | A fuse or electronic breaker per branch sized at or below 1.5 × the branch's steady-state current (package SYRS-013) |
| SF-13 | Holding on power loss for payloads above the DQ-015 limit; a hardware property tested in WP-V-02 |
| SF-14 | Torque de-rating at 75 °C stator temperature, controlled stop at 90 °C (upstream's own protection is the backstop, GAP-13) |
| SF-15 | Audible or visible signal 500 ms before motion starts (package SYRS-035) |
| SF-26, SF-27 | Authentication and session lock on every network and client command path (package SYRS-015, SYRS-016; WP-C-08) |
| SF-28 | Plausibility of each joint's reported position against the commanded motion (package SRS rows on encoders) |
| SF-29 | Software limits at least 5° inboard of the mechanical end-stops (package SYRS-017), with DM-06 providing the stops |
| SF-30 | Damped least-squares inverse kinematics near singularities (package SYRS-024) |
| SF-31 | Camera default-off, opt-in recording, local storage (DQ-014) |

## 4. Required Performance Level

| PLr | Functions | Basis |
|---|---|---|
| d | SF-32, SF-08, SF-24, SF-25, SF-03, SF-02, SF-04, SF-23, (SF-01) | ISO 10218-1 PL d, category 3 for the safety-related control functions of an industrial robot (to be checked); the risk graph of WP-C-03 §5 gives d or e for the rows they address |
| c | SF-06, SF-11, SF-13, SF-14, SF-26, SF-28, SF-29, SF-30 | Risk graph c for the rows they address; limiting and diagnostic functions whose failure is covered by a d-rated stop |
| b | SF-15, SF-27, SF-31 | Risk graph b or below; warning, session and privacy functions |

The adopted target is DQ-004 (open). Option B of that decision would lower every d above to c with the bench-only envelope as the
condition; this document would then record the lowered value with the rationale, never silently.

## 5. Allocation

| Layer | Functions | PL claim |
|---|---|---|
| Hardwired safety chain | SF-32, SF-24; the power-removal path of SF-08 and SF-11 | The only layer with a PL d claim |
| Controller safety layer (DQ-020) | SF-08 (first channel), SF-25, SF-03, SF-02, SF-04, SF-23, SF-06, SF-14, SF-28, SF-29 | A channel of the SRP/CS once it is on separate hardware; on the host it is defence in depth until WP-A-05 argues otherwise |
| Host stack | SF-15, SF-26, SF-27, SF-30, SF-31 | No PL claim; hardened |
| Hardware property | SF-13; DM-01…DM-07 | Verified by test or inspection, no PL |

Every learned component (LeRobot policies, the grasping demo) commands the arm only through the host stack and the safety layer;
learned components are outside every safety function, and nothing they output reaches a drive without passing SF-03, SF-23, SF-29
and the watchdog (WP-M-01 T-03; [WP-C-09](WP-C-09-ml-component-definition-and-safety-requirements.md)).

## 6. Response time and stop category per function

| ID | Detection | Reaction start | Standstill | Stop category | Source |
|---|---|---|---|---|---|
| SF-32 | device contact | ≤ 200 ms to power removal (relay plus contactor) | TBC (WP-V-02) | 0 | package SYRS-005 (500 ms) tightened to the relay budget |
| SF-08 | 250 ms timeout | ≤ 100 ms after timeout | TBC | 1 then 0 | package SYRS-008, SRS-001 |
| SF-25 | ≤ 50 ms | via SF-08 | TBC | 1 then 0 | package SF-25 |
| SF-03 | ≤ 10 ms | clamp immediate; stop ≤ 100 ms on measured exceedance | TBC | 1 | package SF-03 |
| SF-02, SF-04 | ≤ 50 ms / ≤ 100 ms | controlled stop | TBC | 1 | package SF-02, SF-04 |
| SF-14 | ≤ 200 ms | de-rate, then stop | TBC | 1 | package SF-14 |

The budget is kept in WP-S-04; every TBC is measured in WP-V-02 before any separation distance is derived.

## 7. Applicability per mode and task

| Mode | Functions active |
|---|---|
| M-01 OFF | SF-32 (power already removed), SF-24 |
| M-02 IDLE | SF-32, SF-24, SF-25, SF-08, SF-26, SF-27, SF-31 |
| M-03 TEACH | all of IDLE plus SF-03 at the reduced limits, SF-06, SF-02, SF-04, SF-28, SF-29, SF-14, SF-13 |
| M-04 RUN | all of TEACH plus SF-23, SF-30, SF-15 at the RUN limits |
| M-05 ESTOP | SF-32 latched, SF-24, SF-13 |

Tasks T-01…T-08 of WP-C-02 map onto these modes; T-07 and T-08 run in OFF or IDLE only.

## 8. Traceability

| From | To |
|---|---|
| Hazards HZ-nn (WP-C-03 §4, §5) | §2 column Hazards of WP-C-03 §7 |
| Package SF-nn, SYRS, SRS, HwRS | §2 and §3 (identifiers kept) |
| Requirements | WP-S-02 SR-<SF>.<nn> |
| Architecture | WP-S-03 (chain, layer), WP-W-03 (software), WP-H-02 (chain design) |
| Validation | WP-V-02 (stopping, holding), WP-V-03 (force, separation), WP-V-04 (E-stop and chain), WP-V-05 (fault injection) |
| Trace items | `trace/items/hazards.yaml` |

## 9. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Decide the stop category of SF-32 after the holding test of WP-V-02: category 0 only if the loaded arm does not fall | Safety-related control system engineer | G2 |
| OI-2 | Apply DQ-004 (PLr target) and DQ-005 (SF-01) once answered | Safety manager | G1 |
| OI-3 | Replace the package's response targets by the budget of WP-S-04 | Safety-related control system engineer | G2 |
| OI-4 | Specify an enabling device for TEACH (three-position) if hand-guiding is to be inside the case (WP-C-06 §4) | Safety manager | G1 |
| OI-5 | Confirm each actuator's fault behaviour on bus loss and over-temperature with the supplier (DQ-019) | Electrical and mechanical engineer | G2 |
