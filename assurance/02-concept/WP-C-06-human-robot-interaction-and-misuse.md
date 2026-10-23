# WP-C-06 Human-robot interaction, collaborative operation and reasonably foreseeable misuse analysis

| Field | Value |
|---|---|
| Work product | WP-C-06 Human-robot interaction, collaborative operation and reasonably foreseeable misuse analysis |
| Standard reference | Machinery: ISO 10218-2:2025 §5 (collaborative applications); ISO/TS 15066:2016 §5; ISO 12100:2010 §5.3; Other: ISO 13855 §5–§6 (approach speeds, minimum distances); ISO 13854 (minimum gaps); ISO 13857 (safety distances). Clause numbers are to be checked against licensed copies |
| Version | 0.1 (2026-10-20): interaction scenarios IS-01…IS-10, separation-distance derivation with placeholders, the four collaborative modes and what each needs, misuse MU-01…MU-12, operator interface and modes, requirements HR-01…HR-10. 0.0: skeleton |
| Status | Draft |
| PL / scope | PL d target (open, DQ-004); CFG-001 B601-DM v1.1 in OE-1 (open, DQ-003); no collaborative mode claimed in the first case (open, DQ-005, recommended A) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1; someone who has watched people around a desktop arm) |
| Approver | Project lead |
| Baseline | BL-001 |

> [!WARNING]
> Draft. The scenarios and misuses are derived from the package, the gap assessment and the ISO 10218 hazard
> list, not from observation of people around this arm. The separation distances in §3 are a derivation with a
> placeholder for the number nobody has measured, the stopping time of each joint; no distance is claimed until
> WP-V-02 measures it.

## 1. Purpose

Analyses how people interact with the arm in each task and envelope, what each collaborative mode of ISO 10218-2
and ISO/TS 15066 would require before it could be claimed, and the reasonably foreseeable misuse of WP-C-01, with
the approach speeds and distances of ISO 13855 as the quantitative basis for keeping people out of reach.

Operating envelopes and people presence are taken from WP-C-02. Hazards are those of
[WP-C-03](WP-C-03-risk-assessment.md) §4 (the package's HZ-xx identifiers); the safety functions are those of
[WP-C-04](WP-C-04-safety-functions-and-plr.md). The outputs are: the scenarios WP-V-03 validates against, the
separation-distance formula WP-S-04 budgets, the misuse list WP-O-03 warns about, and the requirements HR-01…HR-10
(§7) that go to WP-C-04 and WP-S-02.

## 2. Interaction scenarios

One scenario per way a person and the arm can meet. "Closest" is the distance at which the scenario becomes a
contact if nothing stops the arm.

| ID | Who | Envelope | Task (WP-C-02 §3) | What the person is doing | Closest | Hazard | Measure needed |
|---|---|---|---|---|---|---|---|
| IS-01 | operator | OE-1 | T-02…T-05 | stands at the bench edge outside reach, hand on the pendant, watching the arm | > 650 mm | HZ-M04 if they lean in | marked area (WP-C-02 §6); SF-32 in hand; SF-15 before motion |
| IS-02 | operator | OE-1 | T-01 | hand-guides the arm in TEACH: both hands on a link, fingers near the elbow and wrist joints, face within reach | 0 m by design | HZ-M01, HZ-P03, HZ-M05, HZ-V01 | 25 % torque and speed (SF-03); an enabling device **(to be decided, §4)**; joint gaps per ISO 13854 (DM-02); no RUN command accepted in TEACH |
| IS-03 | operator | OE-1 | T-02 | tele-operates with the leader arm while looking at the follower, not the leader; the follower meets the bench or an object | > 650 mm for the operator | HZ-M04, HZ-C01 | SF-25 heartbeat; SF-04 collision detection as defence in depth; the operator outside reach |
| IS-04 | operator | OE-1 | T-03 | watches a policy run; the policy moves fast toward an object outside its training set; the operator reaches in to catch it | 0 m when they reach in | HZ-C06, HZ-P02 | SF-32 in hand; policy clamp (WP-C-09); SF-03; training: never reach in (MU-01) |
| IS-05 | a second person | OE-1 | any RUN task | walks up to the bench to talk, leans on it or reaches across the arm's area for an object | 0 m | HZ-M04, HZ-P01 | marked area; SF-15; the operator stops the arm (SF-32); no detection exists |
| IS-06 | technician | OE-1 | T-07 | adjusts a fastener or a cover with the arm powered and holding in IDLE; a stale command or a client restart moves a joint | 0 m | HZ-C01, HZ-C04, HZ-M01 | disconnect locked or the chain open for any work inside reach (WP-S-06); SF-24 |
| IS-07 | operator | OE-1 | T-04 | reaches into the envelope between motions to reposition an object, assuming the script is paused | 0 m | HZ-M04, HZ-P02 | IDLE indicated at the arm (HR-05); motion only from IDLE after a warning (SF-15); SF-24 |
| IS-08 | student | OE-2 (excluded) | T-01 | a student hand-guides while another student types at the host; a command arrives in TEACH | 0 m | HZ-C02, HZ-M01 | TEACH refuses motion commands (HR-02); authenticated session (SF-26); the envelope is outside the first case |
| IS-09 | anyone | OE-1 | any | stands under or beside the gripper while it holds a payload; power is cut by the E-stop or a fault | 0 m | HZ-M07 | SF-13 holding on power loss (queued, DQ-015); payload under 1.5 kg; nobody under the gripper |
| IS-10 | operator | OE-1 | any | presses the on-screen stop in the UI expecting the arm to stop; the host is the thing that has frozen | none | HZ-C01, HZ-C04 | SF-08 and SF-25 stop the arm when the host falls silent; SF-32 is the stop the operator uses; labelling (HR-06) |

## 3. Approach speeds and separation distances

The minimum separation between a person and the hazard zone follows ISO 13855 (minimum distance of a safeguard
from a hazard zone as a function of the approach speed), the basis of speed-and-separation monitoring in
ISO/TS 15066. Clause references are to be checked; the form of the derivation is standard, the numbers are not
yet.

| Symbol | Meaning | Value | Source |
|---|---|---|---|
| K | approach speed of a person | 1600 mm/s for a walking approach; 2000 mm/s for a hand reaching in (ISO 13855 values, to be checked) | 13855 §6 |
| T | overall stopping performance: detection and reaction time of the stop function plus the stopping time of the arm | reaction **(TBC, WP-S-04)** + stopping time per joint **(TBC, WP-V-02)** | WP-S-04, WP-V-02 |
| C | intrusion allowance (the distance a hand reaches past the detection boundary before it is detected) | 850 mm for a hand reaching over a plane; smaller for a detection device the arm does not have | 13855 §6 |
| R | reach of the arm plus the payload and the stopping angle at speed | 650 mm + payload + stopping angle **(TBC)** | WP-C-01 §4.2 |

```
S  =  K · T  +  C
```

With no detection device and no measured stopping time, S cannot be computed; what can be said is that for any
plausible T of a few hundred milliseconds, K·T alone is several hundred millimetres and with C it exceeds the
arm's reach. On a desk that means the separation distance is the whole bench: **separation means nobody inside
the reach envelope during motion**, which is what OE-1 and AOU-06 already say. A speed-and-separation claim that
lets a person approach a moving arm needs a detection device, a measured T and a validated S (WP-V-03), none of
which exists.

Consequences for the design:

- The marked area of WP-C-02 §6 is R plus a margin until WP-V-02 measures the stopping angle; the margin is a
  placeholder, not a safety distance.
- In TEACH the person is inside R by design; the separation argument does not apply and §4 says what does.
- The reach-in scenarios (IS-04, IS-05, IS-07) cannot be covered by distance; they are covered by the operator's
  stop, the motion-imminent warning and the mode indication, and recorded as residual risk in WP-C-05.

## 4. Collaborative operation

ISO 10218-2 and ISO/TS 15066 define four collaborative modes (clauses to be checked). None is claimed in the first
case (open, DQ-005, recommended A); the table says what each would need before it could be.

| Mode | What it means for this arm | Claimed? | What a claim would need |
|---|---|---|---|
| Safety-rated monitored stop | the arm is stopped and monitored whenever a person is in reach; motion resumes only when the space is clear | no; functionally this is OE-1 with the operator as the detector | a safety-rated detection of a person in reach (a light curtain, a scanner or a mat) feeding the chain; today nothing detects a person (GAP-06) |
| Hand guiding | a person moves the arm by hand (TEACH, T-01) | no; TEACH is used, but as a bench activity with no claim | a three-position enabling device in the chain, a safely-limited speed and torque in TEACH (SF-03 at 25 %), and the joint gaps of ISO 13854 verified (GAP-01); DQ-005 option C |
| Speed and separation monitoring | the arm slows and stops as a person approaches, keeping S of §3 | no | a detection device, the measured T, the validated S (WP-V-03); on a desk the distance exceeds the reach, so this mode has little use |
| Power and force limiting | contact between the arm and a person is permitted and limited to the body-region thresholds of ISO/TS 15066 Annex A | no | a force and pressure measurement campaign on a body-region fixture, joint torque caps bound to the results, a category 3 contact-force stop (SF-01, SF-02), and no joint torque sensor exists, only current-based estimation (GAP-28; WP-C-10); DQ-005 option B |

What the first case does claim: nobody but the operator is in reach during motion (AOU-06); in TEACH the arm runs
at reduced torque and speed and accepts no motion command; the stop in the operator's hand removes motor power.
Contact detection (SF-04) and the contact-force stop (SF-02) are specified as defence in depth and carry no
collaborative claim until measured.

## 5. Reasonably foreseeable misuse

Likelihood: **H** (expected in normal use of this arm by its intended users), **M** (will happen occasionally or
with untrained people), **L** (needs effort or bad luck). Consequence uses the WP-C-03 severity classes.

| ID | Misuse | Likelihood | Consequence | Hazard | Why it is foreseeable | Measure (design / safeguard / information) |
|---|---|---|---|---|---|---|
| MU-01 | Reaching into the reach envelope during RUN to catch, adjust or hand over an object | H | S2 | HZ-M04, HZ-P02, HZ-P03 | helping an arm that fumbles is what people do; the arm looks slow and small | information and training; SF-15 warning; SF-32 in hand; SF-04 as defence in depth |
| MU-02 | Loading above 1.5 kg, or a long or off-centre payload | H | S1 | HZ-M06, HZ-M07, HZ-T01 | the arm lifts more than it is rated for until it overheats | design: payload limit in WP-W-09 (torque cap); information: marking |
| MU-03 | Running the arm unfixtured, or on a light desk, because the clamps are in the way | H | S2 | HZ-M06 | the kit ships with G-clamps, not bolts | design: fixing points and torque (WP-H-08); information; procedure in WP-V-07 C-3 |
| MU-04 | Editing the joint torque or speed limits in the client because a motion keeps tripping | M | S2 | HZ-M04, HZ-C05 | the limits are client-side constants today (GAP-19) | design: limits as protected parameters of the safety layer (WP-W-09); SF-03 |
| MU-05 | Powering from a non-rated supply, a bench supply without current limit, or a battery | M | S1 | HZ-E01, HZ-E02 | any 24 V source fits an XT30 | design: keyed input, fuse, polarity protection (WP-H-05); information |
| MU-06 | Fitting a non-OEM gripper or tool without re-validation | M | S2 | HZ-M02, HZ-M07, HZ-P03 | the mount is open and the README invites it | information: re-validation rule in WP-O-03; SF-13 requirement on any gripper |
| MU-07 | Running with a cracked cover, a damaged finger or a printed substitute for a load-bearing bracket | M | S2 | HZ-M01, HZ-M03 | the BOM offers printed substitutes; covers crack | information: inspection before use (WP-O-02); AOU-03 |
| MU-08 | Running a policy on a scene it was not trained on, with the operator's hands near the bench | H | S2 | HZ-C06, HZ-P02 | that is what experimentation is | design: policy clamp (WP-C-09), SF-03, SF-04; information |
| MU-09 | Relying on a wireless E-stop that is out of range or out of battery | M | S2 | HZ-P04, HZ-C01 | upstream suggests a XIAO wireless stop | design: a wired chain (DQ-006 A); a wireless stop only in addition, with link surveillance |
| MU-10 | Two clients commanding at once (a notebook and the ROS driver, or two people) | M | S2 | HZ-C02, HZ-M04 | the bus accepts any sender | design: single authenticated session (SF-26, SF-27); mode gate (HR-02) |
| MU-11 | Leaving the arm powered and enabled unattended, or in RUN while away | M | S2 | HZ-C01, HZ-M04 | the arm holds position quietly | design: session lock (SF-27), IDLE on timeout; information |
| MU-12 | Children or visitors at the bench, reaching for the arm | L in OE-1, H in OE-4 | S2 | HZ-M04, HZ-P01 | a small arm looks like a toy | OE-4 excluded (WP-C-02 §5); marked area; information |

## 6. Operator interface and modes

| Topic | Requirement on the interface | Today |
|---|---|---|
| Mode selection | The operator selects TEACH or RUN deliberately in an authenticated session; the arm does not enter RUN because a client connected; the mode is indicated at the arm and in the UI | no modes (GAP-17) |
| Mode indication | A light on the base: green RUN, amber TEACH, white IDLE, red stopped or fault, flashing red reset required; the same states in the UI | nothing on the arm |
| The physical stop | A pendant E-stop in the operator's hand and a bench-mounted button, both in the chain; the UI shows the chain state and cannot clear it | none (GAP-08) |
| The on-screen stop | Labelled "stop request", not styled as an emergency stop; its effect (IDLE, hold) stated next to it | depends on the UI; a software command only |
| Tele-operation | Motion only while the operator holds a control; release stops the arm through the watchdog; the leader arm path runs through the same safety layer as every other source | no deadman; no watchdog (GAP-18) |
| Motion from IDLE | A warning of **(TBC: 1 s)** before the first motion after IDLE (SF-15) | none (GAP-30) |
| Reset | At the arm, deliberate, impossible while a stop demand is present; the UI shows "reset required" | none |
| Camera | An indicator when the camera streams or records; default-off (queued, DQ-014) | default-on (GAP-25) |

## 7. Requirements derived here (to WP-C-04, WP-S-02 and WP-O-03)

| ID | Requirement | Goes to |
|---|---|---|
| HR-01 | The arm shall not move with anyone but the operator inside the reach envelope, and the operator only in TEACH (IS-01, IS-05; AOU-06) | WP-O-03; WP-C-02 §2; WP-V-07 |
| HR-02 | In TEACH the arm shall accept no motion command from any client and shall run at the teach torque and speed limits (IS-02, IS-08, MU-10) | WP-C-04 SF-03; WP-S-02 |
| HR-03 | Hand-guiding shall require a held enabling device once one is specified; until then TEACH is a bench activity with no claim (§4) | WP-C-04 (open item); WP-S-03 |
| HR-04 | Every motion from IDLE shall be preceded by an audible or visible warning (IS-07, MU-01) | WP-C-04 SF-15 |
| HR-05 | The mode and the stop state shall be visible at the arm from every side (IS-06, IS-07) | WP-S-02; WP-H-02 (indicator) |
| HR-06 | The on-screen stop shall not be presented as an emergency stop; the pendant stop shall be the one the operator is trained to use (IS-10) | WP-O-03; WP-S-02 |
| HR-07 | Any work inside the reach envelope with the arm powered shall be done with the chain open or the disconnect locked (IS-06, T-07) | WP-S-06; WP-O-02 |
| HR-08 | Tele-operation and policy execution shall run through the same safety layer as every other command source, with a deadman for tele-operation (IS-03, IS-04, MU-08, MU-10) | WP-C-04 SF-25, SF-26; WP-C-09 |
| HR-09 | The payload limit, the fixing requirement and the no-reach-in rule shall be marked on the arm and its base (MU-01, MU-02, MU-03) | WP-O-03 §4; WP-H-08 |
| HR-10 | A wireless stop, if any, shall be in addition to the wired chain and shall fail safe on link loss (MU-09) | WP-C-04 SF-32; WP-S-03 |

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Lead decision on the collaborative claim (DQ-005, open, recommended A); rewrite §4 to the answer | Project lead | G1 |
| OI-2 | Decide whether an enabling device is required for TEACH in OE-1 and specify it (HR-03); the package's hand-guiding scenario has none | Safety manager | G1 |
| OI-3 | Measure the stopping time per joint (WP-V-02) and compute S of §3 with the confirmed K and C from a licensed ISO 13855 | Safety-related control system engineer | G2 |
| OI-4 | Observe one session of people around a running arm and correct the likelihood ratings of §5 | Reviewer | G1 |
| OI-5 | Specify the indicator light and the warning sounder (HR-04, HR-05) in WP-H-02 | Electrical and mechanical engineer | G2 |
