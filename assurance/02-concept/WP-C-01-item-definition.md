# WP-C-01 Item Definition and Limits of the Machinery

| Field | Value |
|---|---|
| Work product | WP-C-01 Item definition and limits of the machinery (intended use, foreseeable misuse, use, space and time limits) |
| Standard reference | ISO 12100:2010 §5.3 (determination of the limits of the machinery), §5.4 (hazard identification inputs); ISO 10218-1:2025 §4 (robot design, terms), ISO 10218-2:2025 §4 (robot application); ISO 13849-1:2023 §4.5; Regulation (EU) 2023/1230 Annex III §1.1.2, Annex IV Part A (technical documentation). Clause numbers are to be checked against licensed copies (WP-M-06 OI-1) |
| Version | 0.1 (2026-10-20): initial draft from the concept-phase package (03_ItemDef, 13_Assumptions), the B601-DM v1.1 BOM and the gap assessment; CFG-001 and CFG-002; F-01…F-08; E-01…E-10; IF-01…IF-08; AOU-01…AOU-08 |
| Status | Draft |
| PL / scope | PL d target for the stop functions (open, DQ-004, recommended A); CFG-001 the B601-DM v1.1 on a fixtured bench in OE-1 (open, DQ-003, recommended A); CFG-002 the B601-RS, tracked, every value unverified (open, DQ-001, recommended A) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Project lead |
| Baseline | BL-001 (`206ebda`): the fork with upstream's v1.1 hardware record and the concept-phase package |

> [!WARNING]
> Draft prepared for engineering review. Values marked **(unknown)** are not stated anywhere in the upstream
> record or the package and must be measured or decided before the risk assessment (WP-C-03) can be rated with
> confidence. No arm has been built, weighed or powered under this record. Everything said about CFG-002 is a
> placeholder: the B601-RS BOM was not released at the baseline.

## 1. Item identification

| Field | Value |
|---|---|
| Item | reBot-DevArm: a desktop six-axis robot arm with one actuated gripper, its motor harness and CAN bus, the external 24 V supply, the host computer running the control software, and (once they exist) the controller safety layer and the bench safety chain the fork adds. Two configurations: **CFG-001**, the B601-DM v1.1 (§1.1), the reference configuration; **CFG-002**, the B601-RS (§1.2), tracked and unverified |
| Fork | `jherrodthomas/reBot-DevArm` from `Seeed-Projects/reBot-DevArm` at BL-001 |
| Product class | An industrial robot arm in the sense of ISO 10218-1 (a manipulator with its controller), sold as a motor kit, a structural kit, a full kit or pre-assembled. On its own, without its supply, its host and a fixing, it is arguably partly completed machinery; fixtured to a bench with its supply and host it is machinery and a robot application (ISO 10218-2). The fork assesses the fixtured, powered arm. Collaborative operation (ISO/TS 15066) is a mode of application, not a property of the arm, and is claimed only where WP-C-06 §4 proves it (open, DQ-005, recommended A: not in the first case) |
| Upstream designation | "reBot Arm B601 DM" (Damiao actuators) and "reBot Arm B601 RS" (RobStride actuators); hardware v1.1 of 2026-04-25 |
| Manufacturer of record | Seeed Studio (Shenzhen) for upstream; the kit builder for a built arm. The fork assigns no manufacturer and places no product on the market; the CC BY-NC-SA 4.0 licence forbids commercial use (gap assessment GAP-35) |

### 1.1 Reference configuration CFG-001, the B601-DM v1.1

| Element | Value | Source |
|---|---|---|
| Structure | Six sheet-metal and CNC aluminium (5052) links L1…L6 with 3D-printed covers (ABS), fillers and a handle; a base plate and base link; a base reinforcement part added in v1.1 | `hardware/reBot_B601_DM/readme.md` (metal and printed parts) |
| Actuators | 4 × Damiao DM4310 (V4) and 3 × DM4340P (V4), integrated drive and absolute encoder, 24 V, CAN. Joint 1 is a DM4340P since v1.1; the allocation of the remaining DM4340P units to joints 2 and 3 and of the DM4310 units to joints 4 to 6 and the gripper is inferred from the load path and **(unknown)** until confirmed on a built arm (OI-4) | BOM purchased parts; v1.1 changelog |
| Gripper | One actuated parallel gripper: a joint actuator driving a rack (module 1, 16 teeth) on an MGN9 linear rail with two sliders; printed fingers (ABS) or an optional soft TPU finger; holding on power loss **(unknown)** (GAP-07) | BOM; README "DIY finger" |
| Motion limits | Mechanical limit blocks on joint 1 (yaw limit), on the upper arm and on the lower arm; nothing documented for joints 4 to 6 or the gripper; stop angles **(unknown)** (GAP-02) | BOM `02_Arm_Yaw_Limit`, `01_Upper_Arm_Limit`, `01_Lower_Arm_Limit` |
| Harness and bus | One CAN daisy chain through the links on XT30 2+2 cables (350 mm and 200 mm, 16 AWG), with cable restraints at joints 5, 6 and 7 since v1.1; termination **(unknown)** | BOM; v1.1 changelog |
| Host interface | DM CAN-USB adapter board to the host PC over USB | BOM |
| Supply | MEAN WELL LRS-350-24, 24 V, 14.6 A, open-frame, mains-fed; a 12 AWG mains pigtail and a 16 AWG XT30 pigtail to the arm; no fuse, no disconnect, no reverse-polarity protection (GAP-09 to GAP-12) | BOM |
| Host and software | Any PC, Jetson or Raspberry Pi running the upstream Python `motorbridge` SDK; the ROS 2 Humble driver with MoveIt 2 (in progress at the baseline); Pinocchio kinematics; LeRobot policy runtime; the YOLO grasping demo; a web UI. None of it is in this repository or pinned to the hardware (GAP-16) | README roadmap |
| Optional sensing | A wrist camera on a printed mount: Intel D435i, D405, Orbbec Gemini 305 or Gemini 2, or a 32 × 32 UVC module | README "Optional hardware" |
| Optional input | Star Arm 102-LD leader arm for tele-operation and dataset collection | README |
| Emergency stop | None in the documented design; upstream mentions a XIAO ESP32 wireless stop without specifying it (GAP-08) | gap assessment §4 |
| Fixing | Two 6-inch G-clamps are in the purchased-parts list; no bolt pattern, torque or bench requirement is stated (GAP-03) | BOM |

### 1.2 Configuration CFG-002, the B601-RS (unverified)

The B601-RS shares the mechanical envelope and assembly with the DM arm and replaces the Damiao actuators with
RobStride units (models **(unknown)**) on a bus whose protocol and termination are **(unknown)**. Its BOM, assembly
video, ROS 2 driver and LeRobot integration were "in progress" at the baseline. Every actuator-specific row of this
record (limits, holding, thermal behaviour, fault reactions, reliability data) carries a CFG-002 placeholder until
the BOM is released; whether the RS is tracked at all is open (DQ-001, recommended A; DQ-017 queued).

## 2. Intended use and functions

### 2.1 Intended use (ISO 12100 §5.3.2)

- **Use:** embodied-AI research, education and light tele-operated or learned pick-and-place on a workbench:
  teaching by hand-guiding, collecting demonstration datasets with a leader arm, running imitation policies on real
  hardware, scripted and planned motion through the SDK or ROS 2, and demonstrations. Upstream markets the arm for
  "desktop embodied AI applications".
- **Users:** builders (assemble from the kit and the video), operators (developers, researchers, educators who
  run the software), instructors and students (OE-2, outside the first case), bystanders (anyone within reach).
- **Level of training:** none assumed by upstream beyond its wiki; the fork assumes a trained operator present
  with a stop in reach for every powered run (AOU-01).
- **Envelopes:** the four operating envelopes OE-1 to OE-4 of [WP-C-02 §2](WP-C-02-operating-environment-and-tasks.md);
  the first safety case covers OE-1 only (open, DQ-003, recommended A).

### 2.2 Functions

| ID | Function | Implemented by | Notes |
|---|---|---|---|
| F-01 | Free-drive and teach: gravity-compensated joint freedom so a person can move the arm by hand and record poses | SDK torque mode with Pinocchio gravity compensation on the host | A person is in contact with the arm by design; no enabling device exists |
| F-02 | Position control: move the tool centre point to a commanded joint or Cartesian pose | Actuator position loop; IK on the host (Pinocchio, MoveIt 2) | Joint limits only as the client sets them (GAP-19, GAP-20) |
| F-03 | Velocity and torque control: low-level joint commands at the bus rate | Actuator MIT-mode control; SDK | No clamp between the client and the drive |
| F-04 | Pick-and-place: open and close the gripper inside a motion plan | SDK or ROS 2; gripper actuator | Holding on power loss unknown (GAP-07) |
| F-05 | Sense: stream joint position, velocity, torque estimate and temperature, and the wrist camera | Actuator telemetry on CAN; camera over USB | Camera default-on where fitted (GAP-25) |
| F-06 | Tele-operation: follow a leader arm or a remote operator | Leader-arm SDK path; web UI; ROS bridge | Unauthenticated (GAP-22, GAP-23) |
| F-07 | Learned policy execution: run a LeRobot imitation or reinforcement policy from camera images and joint state | Policy runtime on the host, commands through F-02 or F-03 | No independent clamp on the output (GAP-24) |
| F-08 | Stop: bring every joint to rest and remove the drive's enable | Today a software command on the CAN bus; the hardwired chain of WP-S-03 once built | No stop exists that software cannot override (GAP-08) |

### 2.3 Functions the item does not provide

An emergency stop that removes motor power without software; a watchdog that stops the arm when the host falls
silent; an operating-mode state machine; per-joint torque, speed and position limits enforced outside the client;
collision detection; an enabling device for teach mode; a motion-imminent warning; authentication on any command
path. The record says so (gap assessment §4 and §5) and WP-C-04 specifies each as a safety function to be built.

## 3. Item boundary

### 3.1 Inside the item

| Element | Name and content | Role |
|---|---|---|
| E-01 | Mechanical structure: links L1…L6, base plate and link, covers, fillers, limit blocks, fasteners, bearings | structure, pinch and crush points, end-stops |
| E-02 | Actuators: 4 × DM4310, 3 × DM4340P with integrated drive, encoder and closed firmware | the only thing that applies torque; the last stage before the joint |
| E-03 | Gripper: actuator, rack and rail, fingers | end effector; holding of the payload |
| E-04 | Harness and bus: XT30 2+2 CAN daisy chain, cable restraints, termination (unknown) | power and command distribution to every joint |
| E-05 | CAN-USB adapter | the single command path from the host to the bus |
| E-06 | Host software as it touches the arm: the SDK, the ROS 2 driver, the policy runtime, the UI, assessed at their interface to the bus | command sources; functional only; no PL claim |
| E-07 | Controller safety layer (to be built): watchdog and heartbeat, mode state machine, per-joint clamps, encoder plausibility, clamp on every learned output; where it runs is queued (DQ-020) | the checker between every command source and the bus |
| E-08 | Bench safety chain (to be built): two-channel E-stop pendant, safety relay, contactor with mirror contact on the 24 V motor supply, fuse, lockable disconnect (open, DQ-006, recommended A) | the checker of last resort; removes motor power without software |
| E-09 | 24 V supply as installed: the LRS-350-24 and its DC output pigtail; the mains side only as far as the supply's terminals | motor and logic power |
| E-10 | Optional wrist camera and its mount; the leader arm's interface at the SDK | sensing and tele-operation inputs inside the boundary at their interface only |

### 3.2 Outside the item

The host application beyond its interface to the bus (the operator's scripts, notebooks and policies as content);
the site network and any remote operator; the mains installation and the supply's cord and inlet; the Star Arm
leader arm as a device; the workbench, its clamps and the floor; the objects the arm handles; the people at the
bench.

### 3.3 Interfaces

| ID | Interface | Direction | Content | Integrity today |
|---|---|---|---|---|
| IF-01 | CAN bus: host → actuators | in | position, velocity, torque and enable commands per actuator (MIT mode) | no authentication, no sequence, no clamp; any process with the adapter open |
| IF-02 | CAN bus: actuators → host | out | position, velocity, torque estimate, temperature, fault flags | best effort; no host watchdog on the stream (GAP-18) |
| IF-03 | USB: host ↔ CAN-USB adapter | in/out | bus frames | a USB disconnect is silent to the arm |
| IF-04 | SDK and ROS 2 API: application → driver | in | joint and Cartesian targets, gripper commands, mode | any caller; no session, no lock (GAP-22, GAP-23) |
| IF-05 | Leader arm and web UI → host | in | tele-operation targets | unauthenticated; no deadman |
| IF-06 | Wrist camera → host | out | image stream | default-on; no retention rule (GAP-25) |
| IF-07 | 24 V DC: supply → harness | power | up to 14.6 A on one XT30 chain | no fuse, no disconnect, no polarity protection (GAP-09 to GAP-12) |
| IF-08 | Mechanical: base plate → bench | structural | the full payload moment | no bolt pattern or torque stated; clamps only (GAP-03) |

The chain's I/O (E-08 → E-07) will be IF-09 once WP-S-05 defines it.

## 4. Limits of the machinery (ISO 12100 §5.3)

### 4.1 Use limits

| Limit | Value | Status | Source |
|---|---|---|---|
| Payload | 1.5 kg recommended at the tool centre point; continuous use below 1.5 kg within 70 % of reach | declared by upstream | README specifications; thermal test |
| Reach and speed in the first case | 50 % of maximum joint speed and rated torque in RUN, 25 % in TEACH, until WP-V-02 measures stopping performance | proposed (queued, DQ-016, decider: claude) | package 05_OpEnv |
| Maximum joint speed and torque | actuator maxima **(unknown)** in the record; DM4310 and DM4340P datasheet values to be quoted in WP-W-09 | none | GAP-19 |
| Stopping time and angle per joint | **(unknown)**; never measured | none | WP-V-02 |
| Users | trained operator, builder; students and bystanders outside the first case | assumed | AOU-01, AOU-06 |
| Reasonably foreseeable misuse | operation by untrained users; payload above 1.5 kg; operation outside the declared workspace; operation with damaged printed parts; operation without a fixtured base; operation with bystanders in reach and no enclosure; modifying torque limits in software; a non-rated supply; a non-OEM gripper without re-validation; running a policy on an unseen scene; two clients commanding at once; leaving the arm powered unattended | analysed in WP-C-06 §5 | package 03_ItemDef |
| Variant | CFG-001 only; an RS actuator on the bus is outside the case until DQ-017 | none | GAP-34 |

### 4.2 Space limits

| Limit | Value | Source |
|---|---|---|
| Reach envelope | a hemisphere of radius 650 mm centred on the base; about 720 mm high with the arm vertical | README; package |
| Footprint | about 150 × 150 mm base plate | package 03_ItemDef |
| Fixing | the base fixtured to a level workbench; bolt pattern, torque and the bench's own mass **(unknown)** (GAP-03) | AOU-05 |
| Hazard zone | the reach envelope plus the payload's length, plus the stopping angle at speed **(unknown)**; nobody inside it during motion in the first case | WP-C-06 §3 |
| Operator position | outside the hazard zone with the stop pendant in hand; at the bench edge beyond 650 mm plus the payload | WP-V-07 |
| Cable route | the supply and USB cables leave the base on the side away from the operator and are restrained (HZ-M08) | DM-03 |

### 4.3 Time limits

| Limit | Value | Source |
|---|---|---|
| Duty | continuous, mains-fed; no battery | package |
| Thermal limit | joint 2 reached 90 °C after more than 2 h of reciprocating motion at 1.5 kg over 5 to 70 % reach; the actuator's own protection tripped after 40 min at 2.5 kg and after 45 min at 1.5 kg over 5 to 100 % reach; static holds at 70 % and 100 % reach tripped after 18 min and 3 min. Upstream recommends rests after 2 h and active cooling under sustained load | `performance_testing/Performance_Testing.md` |
| Watchdog, heartbeat, deadline | none exist (GAP-18); targets in WP-C-04 (SF-08, SF-25) | none |
| Service life, maintenance interval | **(unknown)**; fasteners are expected to loosen "after prolonged operation" (BOM note) | BOM |

### 4.4 Other limits

Indoor use only on a dry, level bench; ambient +10 to +35 °C and below 80 % RH non-condensing (package
assumptions, not upstream statements); no IP rating (IPX0 assumed); the arm runs on a 24 V SELV bus, the mains
side stops at the supply's terminals; EMC not declared (GAP-15); noise not measured (HZ-N01).

## 5. Operating modes and states

The modes below are the ones the package proposes and WP-C-04 specifies. **None exists today** (GAP-17): the
published software has no mode machine, and any client can enable an actuator and command torque at any time.

| Mode | Who commands motion | Protective layers planned | Notes |
|---|---|---|---|
| M-01 OFF | nobody; motor power removed by the chain or the disconnect | none needed | the only state the record can claim today |
| M-02 IDLE | nobody; actuators enabled and holding position; commands refused | watchdog, heartbeat, mode gate | entered after power-on and after every stop; left only by a deliberate mode change |
| M-03 TEACH | a person moving the arm by hand under gravity compensation; the host records | reduced torque and speed (25 %, DQ-016); an enabling device **(to be decided, WP-C-06 §4)** | the one mode in which contact is intended |
| M-04 RUN | the SDK, ROS 2, the leader arm or a policy, through the safety layer | watchdog, heartbeat, per-joint clamps, policy clamp, motion-imminent warning; nobody in reach (AOU-06) | entry needs an authenticated session and a live heartbeat |
| M-05 ESTOP | nobody; motor power removed by the chain; gripper holds passively | the chain; manual reset (SF-24) | left only by a deliberate reset with the demand cleared |

Transitions: OFF → IDLE on power-up with the chain closed; IDLE → TEACH or RUN on a deliberate, authenticated
operator action; TEACH or RUN → IDLE on command, on a watchdog or heartbeat timeout (SF-08, SF-25) or on a fault;
any state → ESTOP on an E-stop demand or power loss; ESTOP → IDLE on a manual reset only.

## 6. Legal requirements and standards

| Instrument | Applies because | Status in the record |
|---|---|---|
| Regulation (EU) 2023/1230 (Machinery), from 20 January 2027; Directive 2006/42/EC until then | a robot arm put into service in the EU; the fork places nothing on the market and the frame is open (DQ-002, recommended A) | no conformity file; WP-M-13 plans it |
| ISO 10218-1:2025, ISO 10218-2:2025 | an industrial robot and its application | cited by the package; no clause verified |
| ISO/TS 15066:2016 | only if a collaborative mode is claimed (DQ-005) | no claim in the first case |
| ISO 13849-1:2023, ISO 13849-2:2012 | safety-related parts of the control system | no PL claimed; no reliability data (GAP-14) |
| EN 60204-1:2018, ISO 13850:2015 | electrical equipment and emergency stop | no E-stop, no disconnect (GAP-08, GAP-09) |
| ISO 12100:2010, ISO 13854, ISO 13857 | risk assessment, gaps, safety distances | the package's assessment is the input to WP-C-03 |
| IEC 62443-4-1/-4-2 | a networked controller with a motion path | not cited upstream; WP-M-08 |
| Regulation (EU) 2024/1689 (AI Act) | only if a learned component becomes a safety component | none is (open, DQ-008, recommended A); WP-K-07 |
| CC BY-NC-SA 4.0 | upstream's licence; non-commercial use only | the envelopes the licence allows are an open question (GAP-35) |

## 7. Known hazards and experience from similar items

- **The package's catalogue** (33 hazards, kept as HZ-xx in WP-C-03 §4): mechanical (joint pinch and crush,
  gripper shear, sharp edges, arm sweep at head height, entanglement, tip-over, payload drop, cable trip),
  electrical (24 V at the input, arc and short, ESD, EMI), thermal (motor burn, harness overheat), noise,
  vibration, camera infrared, printing dust, lifting and repetitive strain, temperature and liquids, the four
  collaborative contact hazards, seven control and cyber hazards (loss of communication, unauthenticated
  commands, encoder fault, SDK race, joint overshoot, policy edge case, singularity), and camera privacy.
- **Upstream's own experience:** the thermal test stopped at 90 °C on joint 2; fasteners loosen in prolonged
  use; v1.1 added cable restraints because the three end-joint cables worked loose and disconnected, which on a
  CAN chain is a loss-of-communication event (HZ-C01).
- **Arms of this class** (SO-ARM100, OpenArm, Dummy-Robot, the TRLC-DK1 and similar open desktop arms):
  uncommanded motion on client crash with the last command held, runaway on a wrong actuator parameter, pinched
  fingers at the elbow and wrist in teach mode, a dropped payload when power is cut, and arms pulled off an
  unclamped desk by their own moment. ISO 10218-1 Annex A lists the generic robot hazards; the package traversed
  it with ISO 12100 Annex B.

## 8. Assumptions of use and external measures

| ID | Assumption | Holds today? | Where it is used |
|---|---|---|---|
| AOU-01 | The operator is trained and within reach of an emergency stop at all times in RUN | no stop exists (GAP-08); procedural only | every hazard until SF-32 exists |
| AOU-02 | The supply is a 24 V regulated unit rated for the full bus current, with overcurrent protection | partly: the LRS-350-24 is rated; it has no branch protection (GAP-09, GAP-10) | HZ-E02, HZ-T02 |
| AOU-03 | The structure is genuine sheet metal and declared printed materials, with no substitution on load-bearing brackets | not controlled: the BOM offers printed substitutes (GAP-04) | HZ-M01, HZ-M03 |
| AOU-04 | The harness is built per upstream's wiring guide with correct termination | procedural; termination undocumented | HZ-C01, HZ-E02 |
| AOU-05 | The operating surface is level and dry and the arm is clamped to a workbench | procedural; no bolt pattern (GAP-03) | HZ-M06 |
| AOU-06 | No bystander is within the 650 mm reach envelope while the arm is in RUN | procedural only; no detection | HZ-M04, HZ-P01…HZ-P03 |
| AOU-07 | The arm is not a medical device and is not used for patient care or restraint | holds | scope |
| AOU-08 | The wrist camera, when fitted, does not capture or transmit personal data outside the local network without an explicit operator action | not true as shipped (GAP-25) | HZ-D01 |

## 9. Out of scope for this item

The B601-RS variant until DQ-001 and DQ-017 settle it; any mobile base the arm is mounted on (a second item);
the leader arm as a machine of its own; the Isaac Sim model and any simulation result as evidence; a learned
component as a safety function (open, DQ-008, recommended A: inside the item, outside every safety function);
OE-2 to OE-4 (open, DQ-003); medical, patient-care or public-facing use; outdoor use.

## 10. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Weigh a built arm, record its centre of gravity at full reach with 1.5 kg, and record the base fixing (bolt pattern, torque, the bench it was fixed to) | Electrical and mechanical engineer | G1 |
| OI-2 | Measure the joint gaps against ISO 13854 and record the mechanical end-stop angle of every joint and the gripper | Electrical and mechanical engineer | G1 |
| OI-3 | Determine whether the gripper holds its grasp on power loss, by test; feeds DQ-015 | Test bench owner | G2 |
| OI-4 | Confirm the actuator model fitted to each joint on a built arm and quote the DM4310 and DM4340P datasheet limits | Safety-related control system engineer | G1 |
| OI-5 | Lead decisions on the RS variant (DQ-001, open; DQ-017, queued); until then §1.2 stays a placeholder | Project lead | G0 |
