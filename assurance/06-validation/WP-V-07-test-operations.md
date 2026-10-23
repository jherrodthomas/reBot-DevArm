# WP-V-07 Test Operations and Safety Procedures for Powered Testing

| Field | Value |
|---|---|
| Work product | WP-V-07 Test operations and safety procedures for powered testing (hold point) |
| Standard reference | ISO 12100:2010 §6.4 (information for use, including for the development phase), §6.3 (safeguarding and complementary protective measures); ISO 10218-2:2025 §5 (robot application, safeguarding); ISO 13850:2015 §4 (emergency stop function, as bench equipment); EN 60204-1:2018 §5.3 (supply disconnecting device), §7.2 (overcurrent protection); ASPICE 4.0 VAL.1. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (initial procedure; 2026-10-20) |
| Status | Draft |
| PL / scope | Development testing only. No PL is claimed for the bench equipment |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Project lead |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

This procedure is the **hold point** of [WP-M-01 §7](../01-management/WP-M-01-assurance-strategy.md#7-phases-gates-and-sequence):
no reBot-DevArm is powered under the fork's control with any person inside its 650 mm reach envelope until the
conditions below hold. It exists because the arm as inherited has no emergency stop, no supply disconnect, no fuse,
no watchdog between the host and the actuators and no operating-mode machine, and its only stop is a software
command on the same CAN bus that drives the motors ([gap assessment](../00-assessment/gap-assessment.md) GAP-08,
GAP-09, GAP-17, GAP-18). The procedure makes the next months of testing defensible without claiming any
Performance Level: it relies on bench equipment and on the operator, and says so.

It applies to every powered test, from the first stopping-angle measurement to the validation runs of
[WP-V-01](WP-V-01-safety-validation.md). Powering a single actuator on the bench, disconnected from the arm, is
outside it. Buying the bench chain is decision DQ-006 (open, recommended A: a wired two-channel E-stop pendant,
a safety relay and a contactor on the 24 V motor supply, with a fuse and a lockable disconnect). Until it is fitted,
no powered test with any person inside the reach envelope is run; the arm may be run only with the whole bench
area empty and the operator at the supply's switch.

## 2. Conditions before any powered test

| # | Condition | Evidence | Closes |
|---|---|---|---|
| C-1 | A fuse sized for the motor supply and a lockable disconnect are fitted between the 24 V supply and the arm's harness; the supply's mains terminals are enclosed | Photo and part numbers in the change record under [`07-supporting/impact/`](../07-supporting/impact/README.md) | GAP-09, GAP-11 (bench) |
| C-2 | A dual-channel emergency stop (two NC contacts, mushroom button, latching) on a pendant in the operator's hand, through a safety relay that drops the 24 V motor supply by a contactor with a mirror contact; a second button on the bench | Wiring sketch in the change record; a functional test before every session (§4) | GAP-08 (bench) |
| C-3 | The arm's base is fixtured to a rigid bench with the bolts or clamps WP-H-08 specifies (until then: both G-clamps of the BOM, tightened, checked by hand) | Photo in the test log; the fixing recorded | GAP-03 (bench) |
| C-4 | The host software is pinned to a recorded version, the watchdog and heartbeat are on, and the mode machine refuses RUN without a live heartbeat and an authenticated session; until that software exists (DQ-007), nobody is inside the reach envelope while any client is connected | Version read and logged before the test; until then the empty-bench rule in the log | GAP-16, GAP-17, GAP-18 (bench) |
| C-5 | Joint speed and torque ceilings are set to the development limits of §3 (queued, DQ-016, decider: claude) in the client configuration and read back before the test | Configuration file and read-back in the log | GAP-19 (bench) |
| C-6 | The bench area of [WP-C-02 §6](../02-concept/WP-C-02-operating-environment-and-tasks.md#6-test-bench-during-development) is marked; nobody but the operator and one observer is present, both outside the reach envelope during motion | Area sketch in the test log | Operating-envelope limit (WP-C-02) |
| C-7 | The payload is at most 1.5 kg, of known mass, recorded; no sharp, hot or liquid payload | Test log | WP-C-01 §4.1 |
| C-8 | The operator has read this procedure, is trained per WP-M-04, and has run the pre-session checks of §4 | Signed line in the test log | WP-M-04 competence |

Conditions C-1 and C-2 are the bench safety hardware of [WP-M-02 §4.1](../01-management/WP-M-02-safety-plan.md#41-early-implementation-of-at-risk-work);
they are carried forward as the first draft of the product chain ([WP-S-03](../03-system/WP-S-03-technical-safety-concept.md),
[WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md)), not thrown away.

## 3. Limits during development testing

| Limit | Value | Source |
|---|---|---|
| Joint speed and torque | 50 % of the actuator maximum in RUN, 25 % in TEACH, until WP-S-04 sets a budget from the measured stopping performance | DQ-016 (queued); package 05_OpEnv |
| Mode | RUN only with nobody in reach; TEACH only by the operator, both hands on the arm, nobody else in reach; no RUN command accepted while a person is in reach | WP-C-06 HR-01, HR-02 |
| Payload | ≤ 1.5 kg; no continuous operation above 70 % reach beyond 30 min without a rest; stop at the first thermal warning from any actuator | README; thermal test (joint 2 at 90 °C) |
| Reach-in | Nobody reaches into the envelope while any client is connected; objects are repositioned in IDLE after the arm is stopped and the mode is indicated | WP-C-06 IS-07, MU-01 |
| Gripper | No person under or beside a held payload; holding on power loss is unknown (GAP-07) | WP-C-06 IS-09 |
| Policies | A learned policy runs only on a scene recorded in the log, with the operator's hand on the pendant and nothing fragile or sharp in reach | WP-C-09; GAP-24 |
| Network and clients | One client at a time; the host on a private network or none; no remote session | GAP-22, GAP-23 |
| Wireless stop | Not accepted as a stop; if present, in addition to the pendant | WP-C-06 MU-09 |

## 4. Pre-session and per-session checks

1. Check the fixing (C-3) by hand; log it.
2. With the arm powered and in IDLE (actuators enabled, holding), press the pendant E-stop: the contactor must
   drop, every actuator must lose supply, and the arm must not re-enable until the reset is pressed. Repeat with
   the bench button. Log both results.
3. Read the host software version, the safety-layer version where it exists, and the joint ceilings (C-5); compare
   with the planned configuration. Log them.
4. Walk the bench area; confirm the markings, the empty envelope and the observer's position.
5. From IDLE, command a slow move of one joint through a small angle and press the pendant stop during it;
   confirm the stop and note the angle travelled after the press.
6. Only then start the planned test.

A failed check ends the session.

## 5. Test log

Every session has a log entry in [`06-validation/test-sites/`](test-sites/README.md): date, operator, observer,
bench and fixing, software versions, joint ceilings, payload, pre-session check results, the tests run with their
references (WP-V-02, V-03, V-04, V-05, V-01), the policy checkpoint if any, anomalies, and the E-stop presses with
their reasons.

## 6. Anomalies

Any unexpected motion, any motion after a stop demand, any failure of a pre-session check, any contact with a
person or object, any thermal trip and any E-stop press that was not planned is a safety anomaly
([WP-M-02 §9](../01-management/WP-M-02-safety-plan.md#9-safety-anomaly-handling)). Testing stops; the anomaly is
raised as an issue labelled `safety-anomaly`; the safety manager lifts the stop in writing after the cause is
understood.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Buy and fit the bench safety hardware (DQ-006, open, recommended A); record it under `07-supporting/impact/` | Project lead | Before the first powered test with a person in reach |
| OI-2 | Name and train the test operator(s) (WP-M-02 §3.1) | Project maintainer | Before the first powered test |
| OI-3 | Replace the §3 ceilings with the budget of WP-S-04 once the stopping performance is measured (WP-V-02) | Safety-related control system engineer | G2 |
| OI-4 | Specify the fixing (WP-H-08) and replace the G-clamp interim of C-3 | Electrical and mechanical engineer | G2 |
| OI-5 | Define the bench in WP-C-02 §6 with measured margins and reference it in C-6 | Safety manager | G1 |
