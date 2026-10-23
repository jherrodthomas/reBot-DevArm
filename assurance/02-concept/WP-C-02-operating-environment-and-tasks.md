# WP-C-02 Operating environment and task specification

| Field | Value |
|---|---|
| Work product | WP-C-02 Operating environment and task specification (operating envelopes, workstation, people, fixturing) |
| Standard reference | Machinery: ISO 10218-2:2025 §5 (robot application, layout, safeguarding); ISO 12100:2010 §5.3; Other: ISO 21448 §5 (informative method); ASPICE: SYS.1. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (2026-10-20): operating envelopes OE-1…OE-4 from the package's 05_OpEnv, tasks T-01…T-08, environmental limits, exclusions, the development bench. 0.0: skeleton |
| Status | Draft |
| PL / scope | PL d target (open, DQ-004); CFG-001 B601-DM v1.1; the first safety case covers OE-1 only (open, DQ-003, recommended A) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1; someone who has run the arm at a bench with other people present) |
| Approver | Project lead |
| Baseline | BL-001 |

> [!WARNING]
> Draft. Upstream publishes no operating-environment specification; the envelopes come from the package
> (2026-05-04) and every numeric limit marked **(TBC)** is a proposal for the lead or a value the tests of
> WP-V-02 and WP-V-03 must set. No bench has been walked with the arm running under this record.

## 1. Purpose

Specifies where and how the arm is used: the operating envelopes, the tasks within each, the people present, the
fixturing, the environmental limits and what is excluded. It is the machinery analogue of an operational design
domain and the source of every operating-envelope limit the safety case relies on. The risk assessment
([WP-C-03](WP-C-03-risk-assessment.md)) rates its situations against these envelopes and tasks; the information for
use ([WP-O-03](../09-production-operation/WP-O-03-information-for-use.md)) carries the exclusions of §5 to the
operator; the test procedure ([WP-V-07](../06-validation/WP-V-07-test-operations.md)) uses the bench of §6 as its
condition C-6.

People presence per operating envelope is an input to the misuse analysis of WP-C-06.

## 2. Operating envelopes

An envelope is one combination of place, people, fixturing and speed limit. People-presence classes: **operator
only** (a trained person with the stop in hand, outside the reach envelope during motion), **briefed** (trained
people who may be in reach only while the arm is stopped or in TEACH), **public** (anyone, including children).

| Envelope | Name | Who is present | Where the E-stop is | Fixturing | Speed cap | Contact possible | Allowed in the first case |
|---|---|---|---|---|---|---|---|
| OE-1 | Laboratory or desk, supervised | operator only; one observer outside reach | pendant in the operator's hand and a bench-mounted button (DQ-006) | clamped or bolted to a bench (§6) | 50 % in RUN, 25 % in TEACH **(TBC, DQ-016)** | no: nobody in reach during motion; in TEACH only the operator's hands on the arm | **provisionally yes** (open, DQ-003, recommended A), under WP-V-07 |
| OE-2 | Classroom | instructor present; students operating and in reach during teach | instructor-held and bench-mounted | clamped to a desk | 25 % teach speed **(TBC)** | yes: students within reach during teach | no: needs a hand-guiding or separation claim (DQ-005) and the gaps of §5 closed |
| OE-3 | Industrial collaborative cell | trained cell operator; personnel during collaborative tasks | cell E-stop with guards | mounted in a defined cell | ISO/TS 15066 bounded | yes, by design | no: needs power-and-force limiting measured (GAP-28) and an integrator's cell |
| OE-4 | Public-facing demonstration | demonstrator and bystanders, including children | present, but bystanders may reach in | plinth with a barrier | ≤ 250 mm/s at the tool **(package)** | yes, uncontrolled | **excluded** (§5) |

The envelope in force is a safety parameter of the controller safety layer (WP-W-09), never a property the host
application sets alone.

## 3. Tasks

| Task | What happens | Envelope | Mode (WP-C-01 §5) | Speed | People during the task | Protective function needed | Status at BL-001 |
|---|---|---|---|---|---|---|---|
| T-01 | Teach by hand-guiding: the operator moves the arm under gravity compensation and records poses | OE-1 (OE-2 later) | M-03 | the person's hand; motor torque at 25 % | operator's hands on the arm; nobody else in reach | SF-03 at the teach limit, SF-28, an enabling device **(to be decided, WP-C-06 §4)**, SF-32 | the mode does not exist (GAP-17); gravity compensation is a client feature |
| T-02 | Dataset collection with the leader arm: the arm follows the leader; the operator holds the leader outside reach | OE-1 | M-04 | 50 % | operator only | SF-25, SF-08, SF-03, SF-26, SF-32 | unauthenticated path; no watchdog (GAP-18, GAP-23) |
| T-03 | Policy execution: a LeRobot or similar policy drives the arm from camera images | OE-1 | M-04 | 50 % | operator only, hand on the stop | SF-03, SF-04, SF-08, SF-25, SF-29, SF-15, the policy clamp of WP-C-09, SF-32 | no clamp on the output (GAP-24) |
| T-04 | Scripted pick-and-place through the SDK | OE-1 | M-04 | 50 % | operator only | as T-03 without the policy clamp; SF-13 for the payload | no limits outside the client (GAP-19) |
| T-05 | Planned motion through ROS 2 and MoveIt 2 | OE-1 | M-04 | 50 % | operator only | as T-04; SF-30 near singularities | driver in progress at the baseline |
| T-06 | Demonstration to visitors at the bench | OE-1 only with visitors outside reach; OE-4 excluded | M-04 | 50 % | operator; visitors beyond the marked line | as T-04; SF-15 warning; the marked line of §6 | nothing warns before motion (GAP-30) |
| T-07 | Maintenance and repair with power on: tightening fasteners, replacing a printed part, checking the harness | OE-1 | M-02 or M-01 | 0 | technician's hands on the arm | the chain open or the disconnect locked (WP-S-06); SF-24 before any restart | no disconnect (GAP-09) |
| T-08 | Assembly and commissioning of a kit; first power-on | OE-1 | M-01 → M-02 | 0 | builder | the commissioning checks of WP-O-01; the E-stop test of WP-V-07 §4 | an assembly video and a BOM are the instructions (GAP-33) |

Tasks T-01 to T-06 run only with the chain of WP-V-07 fitted and the controller safety layer in place; until
then every powered activity is a bench test with nobody inside the reach envelope.

## 4. Environmental limits

| Limit | Value | Basis | Consequence of exceeding |
|---|---|---|---|
| Ambient temperature | +10 to +35 °C **(TBC)** | package assumption; upstream recommends 15 to 35 °C and says torque and accuracy drift above 35 °C ambient or 75 °C motor | thermal trip mid-motion (HZ-T01); a held joint goes limp |
| Humidity | ≤ 80 % RH non-condensing **(TBC)** | no IP rating | electrical fault (HZ-E02) |
| Dust, liquids | dry bench; no drinks, coolant or wet work within reach | IPX0 assumed | HZ-V03 |
| Surface | a level, rigid bench that does not move under the payload moment; the arm bolted or clamped to it (AOU-05); bench mass and fixing **(TBC, WP-H-08)** | 22 N·m moment at reach with 1.5 kg (package estimate) | tip-over (HZ-M06) |
| Payload | ≤ 1.5 kg including the gripper fingers; continuous duty below 1.5 kg within 70 % of reach | README; thermal test | thermal trip; overshoot at the end-stops |
| Lighting | enough for the operator to see the whole reach envelope; for the camera, the policy's training conditions | no safety function depends on light | a policy on an unseen scene (HZ-C06) |
| Electromagnetic environment | a laboratory or office bench; no welders or large drives on the same circuit **(assumed, not tested)** | GAP-15 | bus errors, loss of communication (HZ-C01) |
| Network | the host on a private network or none; no remote access to the SDK or the UI in the first case | GAP-22, GAP-23 | unauthenticated command (HZ-C02) |
| Noise | not measured; the package flags servo noise above 70 dBA in a classroom | HZ-N01 | hearing exposure in OE-2 |

## 5. What is outside the environment

Each exclusion becomes an operating limit in WP-O-03 §3 and a marking where it applies.

| Exclusion | Why |
|---|---|
| OE-4: public demonstrations, children or animals within reach, bystanders who may reach in | no detection of a person in reach; no force limiting (GAP-28) |
| OE-2 and OE-3 until their gaps are closed | people in reach during motion or teach need a claim the first case does not make (DQ-005) |
| Outdoor use, wet or dusty rooms, washdown | IPX0; harness and actuators unsealed |
| Mounting on a mobile base, a cart or any moving platform | a second item; the reach envelope and the stopping budget change |
| An unfixtured arm, or a bench lighter than the fixing analysis requires | tip-over (HZ-M06) |
| Payloads above 1.5 kg, liquids, sharp tools or hot objects in the gripper | thermal trip, drop, the tool's own hazard |
| A supply other than a regulated 24 V unit with the protection of WP-H-05 | HZ-E01, HZ-E02 |
| Remote tele-operation over a public network; shared hosts | HZ-C02 |
| Operation with a damaged or substituted printed cover, finger or load-bearing part | exposed joint gap, structural failure (HZ-M01, HZ-M03) |
| Medical, patient-care, food or lifting-of-persons use | AOU-07; outside ISO 10218 |

## 6. Test bench during development

The bench [WP-V-07](../06-validation/WP-V-07-test-operations.md) condition C-6 requires, and the only place the
arm runs under the fork until OE-1 is formally entered:

- a rigid, level bench with the base bolted or clamped as WP-H-08 will specify; until then at least the two
  G-clamps of the BOM, checked before each session;
- a marked floor and bench area of the reach envelope plus 0.5 m on every side **(TBC)**, free of other
  equipment the arm could strike, with the supply and the host outside it;
- the operator's position at the bench edge outside the marked area, facing the arm, with the stop pendant in
  hand; one observer at most, also outside the area and never behind the operator's line of sight;
- the supply's disconnect and the bench E-stop within the operator's reach without stepping into the area;
- payloads of known mass only, recorded in the test log;
- nothing a camera-driven policy could mistake for its training scene within reach, unless that is the test.

## 7. Traceability

| This document | Used by |
|---|---|
| Envelopes OE-1…OE-4, people classes | WP-C-03 situations and ratings per envelope; WP-C-06 §2 scenarios and §5 misuse per people class; WP-O-03 §3 limits; WP-W-09 envelope parameter |
| Tasks T-01…T-08 | WP-C-03 situations; WP-C-04 safety functions per task and mode; WP-V-01 validation scenarios |
| Environmental limits §4 | WP-C-01 §4.4; WP-H-05 (electrical); WP-H-08 (fixing); WP-V-02 test conditions |
| Exclusions §5 | WP-O-03 §3; AOU-05, AOU-06, AOU-07 of WP-C-01 §8 |
| Test bench §6 | WP-V-07 C-6; `06-validation/test-sites/` site records |

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Lead decision on the first envelope (DQ-003, open, recommended A: OE-1 only); rewrite §2 to the answer | Project lead | G1 |
| OI-2 | Set every **(TBC)** value: speed caps (DQ-016), bench fixing and mass (WP-H-08), marked-area margin from the measured stopping angle (WP-V-02), temperature and humidity | Safety manager | G1 |
| OI-3 | Decide whether hand-guiding in TEACH needs an enabling device in OE-1 (WP-C-06 §4) and what T-01 may run until it exists | Safety manager | G1 |
| OI-4 | A site record template for the bench (fixing, area, supply, network) under `06-validation/test-sites/` | Safety manager | G1 |
| OI-5 | Reviewer who has run the arm with other people at the bench confirms the people classes and the T-06 line | Reviewer | G1 |
