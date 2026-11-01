# WP-C-03 Risk Assessment and Required Performance Levels

| Field | Value |
|---|---|
| Work product | WP-C-03 Hazard identification and risk assessment (ISO 12100) and determination of the required Performance Level per safety function (ISO 13849-1) |
| Standard reference | ISO 12100:2010 §5.4–§5.6, Annex B; ISO 13849-1:2023 §5, Annex A (risk graph); ISO 10218-1:2025 Annex A and ISO 10218-2:2025 Annex A (hazard lists, checked against the 2011 editions); ISO/TS 15066:2016 §5, Annex A; ISO 13850:2015; ISO 13854:2019; EN 60204-1:2018 §9.2.2 (stop categories); Regulation (EU) 2023/1230 Annex III §1.1.2 |
| Version | 0.2 (2026-11-01): every row re-rated for OE-1 (§5.3; highest PLr d, no row at e, HZ-P01 and HZ-P02 excluded by IFU-08). 0.1 (2026-10-20): the 34 hazards and ratings of the concept-phase package carried into the record; the package's 31 "safety functions" split into 20 control functions, 7 design measures and 9 instructions; SF-32 emergency stop added; ratings per operating envelope kept, re-rating for OE-1 as an open item |
| Status | Draft |
| PL / scope | Highest PLr in OE-1: **d** (§5.3), the target for the stop functions (DQ-004, answered A); seven rows rate **e** in the package for envelopes with a person in reach during RUN; CFG-001 B601-DM v1.1 in OE-1 (DQ-003, answered A); CFG-002 B601-RS tracked, unrated |
| Author | Assurance team (AI-assisted draft, I0), from the package of J. Herrod-Thomas (2026-05-04) |
| Reviewer(s) | TBD (I1); the ratings need a reviewer who has operated the arm |
| Approver | Project lead |
| Baseline | BL-001; item as defined in [WP-C-01](WP-C-01-item-definition.md) |

> [!WARNING]
> Draft. The severity and probability ratings are the engineering judgement of the concept-phase package
> (`reBot_DevArm_Safety_Case.xlsx`, 07_HARA), not measurement: the arm's mass, stopping time, joint gaps and contact forces
> are unknown (WP-C-01 §10). Each row is rated for the envelopes the package named; the first safety case covers OE-1 only
> (DQ-003, answered A); §5.3 re-rates every row for OE-1, changing exposure and avoidance only where the envelope's rules
> change them. Nothing here lowers a rating to fit the existing hardware. Clause references are to be checked against licensed copies (DQ-011).

## 1. Scope and inputs

- **Item:** the B601-DM v1.1 arm of [WP-C-01](WP-C-01-item-definition.md) (CFG-001) in modes M-01 to M-05 within the limits of WP-C-01 §4, on the
  supervised, fixtured bench of OE-1 ([WP-C-02](WP-C-02-operating-environment-and-tasks.md) §2). Rows rated for OE-2 to OE-4 are kept so the case can
  be extended; they are not claims. CFG-002 (B601-RS) is not rated (DQ-001, DQ-017).
- **Inputs:** WP-C-01 (item, functions, modes, assumptions of use AOU-01…AOU-08); WP-C-02 (operating envelopes OE-1…OE-4, tasks T-01…T-08);
  [WP-C-06](WP-C-06-human-robot-interaction-and-misuse.md) (interaction scenarios IS-nn, misuse MU-nn, separation distances);
  the [gap assessment](../00-assessment/gap-assessment.md) (GAP-01…GAP-36); the package's hazard catalogue (06_Hazards), risk assessment
  (07_HARA), system FMEA (08_FMEA) and functional safety concept (09_FSC); upstream's thermal test; the ISO 10218-1 and ISO/TS 15066 hazard lists; ISO 12100 Annex B.
- **Outputs:** the hazard list (§4), the risk estimation per envelope (§5), the design measures and information for use (§6), the safety
  functions SF-nn with their PLr (§7). The specification of each safety function is [WP-C-04](WP-C-04-safety-functions-and-plr.md);
  the three-step allocation per row is [WP-C-05](WP-C-05-risk-reduction-concept.md).
- **Cyber-induced hazards** (HZ-C02 and any threat scenario that reaches a hazard) are rated here with the hazard's severity;
  Cyber-induced hazards are analysed in WP-C-07 for likelihood and controls.
- **Out of scope:** a mobile base, the leader arm's own hazards, the mains installation beyond the PSU's enclosure, OE-4 (excluded, WP-C-02 §5).

## 2. Method

1. **Situations** (§3): the tasks of WP-C-02 in each operating envelope, with who is in reach.
2. **Hazard identification** (§4): ISO 12100 Annex B origins crossed with ISO 10218-1 Annex A and ISO/TS 15066; the package's
   catalogue is kept with its identifiers `HZ-<category><nn>` so the DFMEA, the requirements and the test plan stay traceable.
3. **Risk estimation** (§5): the ISO 13849-1 Annex A risk graph per row: severity S1 (slight, normally reversible) or S2 (serious,
   normally irreversible, or death); frequency or exposure F1 (seldom, or short) or F2 (frequent to continuous, or long); possibility
   of avoiding P1 (possible under specific conditions) or P2 (scarcely possible). The graph gives PLr a to e.
4. **Type-C check.** ISO 10218-1 assigns PL d, category 3 to the safety-related control functions of an industrial robot (emergency
   stop, protective stop, the limiting functions; **to be checked against a licensed copy**). Where the type-C value and the graph
   differ, the higher is adopted unless the row says why not; where the graph gives **e**, the situation is excluded from the operating
   envelope rather than argued down (the seven rows below).
5. **Risk evaluation** (§6): per ISO 12100 §6, inherently safe design first (DM-nn), then safeguarding and complementary measures
   (the safety functions SF-nn with their PLr), then information for use (IFU-nn).
6. **Safety functions** (§7): each SF-nn with its adopted PLr and the hazards it addresses; the package's "safety functions" that
   are design measures or instructions are reclassified (§6) and their numbers reserved.

## 3. Situations

| ID | Envelope | Task (WP-C-02) | Who is in reach | In the first case |
|---|---|---|---|---|
| OS-01 | OE-1 | T-01 teach by hand-guiding (TEACH) | The operator, by design, hand on the arm | yes |
| OS-02 | OE-1 | T-02 dataset collection with the leader arm (RUN) | Nobody; operator at the leader arm outside reach | yes |
| OS-03 | OE-1 | T-03 learned-policy execution (RUN) | Nobody; operator watching with the pendant | yes |
| OS-04 | OE-1 | T-04 scripted pick-and-place, T-05 ROS 2 motion (RUN) | Nobody | yes |
| OS-05 | OE-1 | T-07 maintenance and repair (OFF, IDLE) | The maintainer, hands on the arm | yes |
| OS-06 | OE-1 | T-08 assembly and commissioning (OFF to IDLE) | The builder | yes |
| OS-07 | OE-2 | T-01, T-02, T-06 demo with students in reach during teach | Students, instructor | no (DQ-003) |
| OS-08 | OE-3 | T-04 collaborative pick-and-place with a cell operator in reach | Trained cell operator | no (DQ-003, DQ-005) |
| OS-09 | OE-4 | T-06 public demo | Bystanders, children | excluded (WP-C-02 §5) |

## 4. Hazard identification

| ID | Category | Origin | Hazardous event | Standard (to be checked) | Envelopes |
|---|---|---|---|---|---|
| HZ-M01 | Mechanical | Crushing | Joint pinch between adjacent links during motion; finger/hand caught | 10218-1 §5.10 / 13854 | All |
| HZ-M02 | Mechanical | Shearing | Scissor action between gripper jaws and links | 13854 | All |
| HZ-M03 | Mechanical | Cutting | Sharp edges on sheet-metal brackets; loose fastener projectile | 12100 B.1 | All |
| HZ-M04 | Mechanical | Impact | Arm sweep strikes operator/bystander head/torso during RUN | TS 15066 §5 | OE-2..4 |
| HZ-M05 | Mechanical | Drawing-in | Hair, jewellery, clothing entanglement at joint axes | 13857 | OE-2..4 |
| HZ-M06 | Mechanical | Stability — tip | 4.5 kg arm with 1.5 kg payload at 650 mm = ~22 N·m moment; unfixtured base tips | ASS-A-05 | All |
| HZ-M07 | Mechanical | Payload drop | Gripper releases payload during motion or on power loss | 10218-1 §5.6 | All |
| HZ-M08 | Mechanical | Slip / trip | PSU cable trip hazard at base | 12100 B.1 | OE-1..3 |
| HZ-E01 | Electrical | Electric shock | 24 V DC limited risk but poor isolation at barrel-jack input | 60204-1 §6 | All |
| HZ-E02 | Electrical | Arc / short | PSU short circuit; motor cable damage | 60204-1 §6 | All |
| HZ-E03 | Electrical | ESD | Static damage to motor controllers / Jetson during handling | 60204-1 | OE-1..2 |
| HZ-E04 | Electrical | EMI / EMC | RF interference disrupts CAN bus or USB camera link | 60204-1 §4.4.2 | All |
| HZ-T01 | Thermal | Burn (motor) | Joint motor stator surface > 60 °C under sustained load (HT scenarios) | 12100 B.2 | All |
| HZ-T02 | Thermal | Cable overheat | Motor harness conductor undersized for sustained current | 60204-1 §13 | All |
| HZ-N01 | Noise | Hearing | Servo gear noise > 70 dBA in classroom — chronic exposure | 12100 B.3 | OE-2 |
| HZ-V01 | Vibration | Hand-arm | Hand-on-arm during teach mode — likely low | 12100 B.4 | All |
| HZ-R01 | Radiation | Optical | Camera IR illuminator (D435i) — eye exposure if directed | 12100 B.5 | All |
| HZ-X01 | Materials | 3D print fumes | PLA/ABS dust during repair sanding | 12100 B.6 | OE-1 |
| HZ-G01 | Ergonomic | Lifting | 4.5 kg arm + base manual handling injury | 12100 B.7 | All |
| HZ-G02 | Ergonomic | Repetitive teach | Operator wrist strain during long demonstration sessions | 12100 B.7 | OE-2 |
| HZ-V02 | Environment | Operating temp | Outside +10..+35 °C: motor torque drift, bearing pre-load change | 12100 B.8 | OE-3..4 |
| HZ-V03 | Environment | Wet | No IP rating; coolant or beverage spill into joints | 12100 B.8 | OE-2..4 |
| HZ-P01 | Collaborative | Quasi-static contact (head) | Persistent contact between TCP and forehead exceeding TS 15066 thresholds | TS 15066 A.2 | OE-3..4 |
| HZ-P02 | Collaborative | Transient contact (hand) | Impact on hand exceeding 280 N transient threshold | TS 15066 A.2 | OE-3..4 |
| HZ-P03 | Collaborative | Pinch (finger) | Joint motion traps finger between link and external surface | TS 15066 / 13854 | OE-2..4 |
| HZ-P04 | Collaborative | Restart after E-Stop | Auto-restart whilst operator inside reach envelope | 10218-1 §5.5.5 | OE-2..4 |
| HZ-C01 | Control / cyber | Loss of comm | ROS topic stall in RUN — joint last-cmd hold (NOT safe) | 13849-1 §6 | All |
| HZ-C02 | Control / cyber | Unauth cmd | Network-exposed ROS / Python SDK without auth | 10218-1 §5.4 | OE-2..4 |
| HZ-C03 | Control / cyber | Sensor failure | Encoder fault — pose drift; balance unaffected (no IMU) but trajectory diverges | 13849-1 | All |
| HZ-C04 | Control / cyber | SDK race/deadlock | Python GIL / async race in motorbridge holds last command | 13849-1 | All |
| HZ-C05 | Control / cyber | Joint limit overshoot | Position cmd exceeds soft limit → mech end-stop or singularity | 10218-1 §5.10 | OE-2..4 |
| HZ-C06 | Control / cyber | LeRobot policy edge case | Imitation policy outputs unsafe trajectory under OOD scene | GAP-LP-01 | OE-3..4 |
| HZ-C07 | Control / cyber | Singularity | IK at workspace boundary causes joint speed spike | 10218-1 §5.10 | All |
| HZ-D01 | Data / privacy | Camera capture | Wrist camera records persons / private spaces inadvertently | GDPR ref. | OE-3..4 |

The categories follow ISO 12100 Annex B (mechanical, electrical, thermal, noise, vibration, radiation, materials, ergonomic,
environment), ISO/TS 15066 (collaborative contact: HZ-P) and this record's own (control and cyber: HZ-C; data: HZ-D). HZ-D01 is not a
safety hazard; it is kept because its measure (SF-31) is a camera posture the lead decides (DQ-014).

## 5. Risk estimation

Ratings as in the package; `Residual` is the package's estimate with its safety functions in place and is not evidence.
Where the package named a design measure or an instruction as the "safety function", the record's DM-nn or IFU-nn is shown.

| ID | Envelopes | Scenario | S | F | P | PLr | Cat. target | Initial risk | Residual | Measures |
|---|---|---|---|---|---|---|---|---|---|---|
| HZ-M01 | All | Joint pinch / crushing finger or hand during RUN | S2 | F2 | P2 | e | 4 | V.High | Med | SF-03, SF-04 |
| HZ-M02 | All | Gripper-jaw shearing | S2 | F1 | P2 | d | 3 | High | Low | SF-04, SF-13 |
| HZ-M03 | All | Sharp edge / loose fastener | S1 | F2 | P1 | b | 1 | Low | Low | DM-01 |
| HZ-M04 | OE-2..4 | Arm sweep strike on torso/head | S2 | F2 | P2 | e | 4 | V.High | Med | SF-03, SF-06, SF-15 |
| HZ-M05 | OE-2..4 | Hair / clothing entanglement at joint axis | S2 | F1 | P2 | d | 3 | High | Med | DM-02 |
| HZ-M06 | All | Tip-over of unfixtured base under payload moment | S1 | F1 | P1 | a | B | Low | Low | IFU-01 |
| HZ-M07 | All | Gripper drops payload on power loss | S1 | F2 | P1 | b | 1 | Low | Low | SF-08, SF-13 |
| HZ-M08 | OE-1..3 | Trip over PSU cable | S1 | F2 | P1 | b | 1 | Low | Low | DM-03 |
| HZ-E01 | All | 24 V DC shock at barrel jack | S1 | F1 | P1 | a | B | Low | Low | DM-04 |
| HZ-E02 | All | Motor harness short → arc | S2 | F1 | P1 | c | 2 | Med | Low | DM-04, SF-11 |
| HZ-E03 | OE-1..2 | ESD damage during build/repair | S1 | F2 | P1 | b | 1 | Low | Low | IFU-02 |
| HZ-E04 | All | EMI disrupts CAN / USB camera | S1 | F1 | P1 | a | B | Low | Low | DM-05 |
| HZ-T01 | All | Motor stator burn | S1 | F2 | P1 | b | 1 | Low | Low | SF-14 |
| HZ-T02 | All | Motor harness overheat / insulation fail | S2 | F1 | P1 | c | 2 | Med | Low | SF-11, SF-14 |
| HZ-N01 | OE-2 | Servo noise > 70 dBA in classroom | S1 | F2 | P1 | b | 1 | Low | Low | IFU-03 |
| HZ-V01 | All | Hand-arm vibration during teach | S1 | F1 | P1 | a | B | Low | Low | — |
| HZ-R01 | All | Camera IR illumination eye exposure | S1 | F1 | P1 | a | B | Low | Low | — |
| HZ-X01 | OE-1 | PLA / ABS dust during repair | S1 | F1 | P1 | a | B | Low | Low | IFU-04 |
| HZ-G01 | All | Lifting injury (4.5 kg + base) | S1 | F2 | P1 | b | 1 | Low | Low | IFU-05 |
| HZ-G02 | OE-2 | Repetitive wrist strain during teach | S1 | F2 | P1 | b | 1 | Low | Low | IFU-06 |
| HZ-V02 | OE-3..4 | Out-of-spec ambient temp | S1 | F1 | P1 | a | B | Low | Low | IFU-07 |
| HZ-V03 | OE-2..4 | Liquid spill into joint | S1 | F1 | P1 | a | B | Low | Low | IFU-07 |
| HZ-P01 | OE-3..4 | Quasi-static contact head exceeds TS 15066 limit | S2 | F1 | P2 | d | 3 | High | Med | SF-01, SF-02 |
| HZ-P02 | OE-3..4 | Transient hand impact > 280 N | S2 | F2 | P2 | e | 4 | V.High | Med | SF-01, SF-02, SF-23 |
| HZ-P03 | OE-2..4 | Pinch finger between link and external surface | S2 | F2 | P2 | e | 4 | V.High | Med | SF-03, SF-04 |
| HZ-P04 | OE-2..4 | Auto-restart after E-Stop with operator in envelope | S2 | F1 | P2 | d | 3 | High | Low | SF-24 |
| HZ-C01 | All | ROS topic loss in RUN — last-cmd hold | S2 | F2 | P2 | e | 4 | V.High | Med | SF-08, SF-25 |
| HZ-C02 | OE-2..4 | Unauth tele-op command via ROS / Python | S2 | F1 | P2 | d | 3 | High | Low | SF-26, SF-27 |
| HZ-C03 | All | Encoder fault — pose drift | S1 | F2 | P2 | c | 2 | Med | Low | SF-28 |
| HZ-C04 | All | SDK race holds last command | S2 | F2 | P2 | e | 4 | V.High | Med | SF-25 |
| HZ-C05 | OE-2..4 | Joint limit overshoot | S1 | F2 | P2 | c | 2 | Med | Low | SF-29 |
| HZ-C06 | OE-3..4 | LeRobot policy edge case → unsafe trajectory | S2 | F2 | P2 | e | 4 | V.High | High | SF-01, SF-04, SF-08 |
| HZ-C07 | All | Singularity → joint speed spike | S1 | F2 | P2 | c | 2 | Med | Low | SF-30 |
| HZ-D01 | OE-3..4 | Wrist camera privacy capture | S1 | F1 | P1 | a | B | Low | Low | SF-31 |

### 5.1 Counts

| PLr | Rows |
|---|---|
| a | 9 |
| b | 8 |
| c | 5 |
| d | 5 |
| e | 7 |

The seven rows that reach **e** (HZ-M01, HZ-M04, HZ-P02, HZ-P03, HZ-C01, HZ-C04, HZ-C06 as the package rates them) all have a person
inside the reach during RUN or a last-command hold with a person in reach. In OE-1 nobody but the operator is in reach and the
operator holds the pendant, so the exposure term changes; the re-rating for OE-1 is §5.3.

### 5.2 What this record changes against the package

| Change | Why |
|---|---|
| SF-32 emergency stop added as a safety function in its own right | The package carried the E-stop inside SF-08 (safe stop) and SF-24 (reset); ISO 10218-1 and ISO 13850 treat it as a function with its own PLr, devices and validation (GAP-08) |
| Package SF-05, SF-07, SF-09, SF-10, SF-17 reclassified as design measures DM-01…DM-05; SF-12, SF-16, SF-18…SF-22 as information for use IFU-01…IFU-07 | A chamfer, a cover gap or a procedure has no Performance Level; keeping them as SFs would let a PL claim rest on a manual. The numbers are reserved and never reused |
| SF-01 (power-and-force limiting) kept but not claimed | No measurement exists (GAP-28); whether the fork makes the claim at all is DQ-005 |
| Every row carries its envelope; the first case covers OE-1 only | The package rated OE-2 to OE-4 rows as if all were in scope; DQ-003 limits the scope |
| HZ-M06 (tip-over) raised in priority | The package rated it PLr a with a procedure; the gap assessment (GAP-03) shows the fixing is undocumented, so DM-07 and IFU-01 are both required and the rating is to be re-checked |

### 5.3 Re-rating for OE-1

The first safety case covers OE-1 only (DQ-003, answered A): a supervised bench, the arm fixtured, a trained operator
with the pendant, one observer, nobody in reach while the arm moves in RUN, and in TEACH only the operator's hands on
the arm (WP-C-02 §2). Each row is rated again for that envelope with the same risk graph. Severity is never lowered:
only the exposure (F) and the possibility of avoiding (P) change, and only where the envelope's rules change them.
Foreseeable misuse stays in: reaching into the envelope during RUN is rated, not ruled out (WP-C-06). No collaborative
claim is made (DQ-005, answered A), so the contact rows HZ-P01 and HZ-P02 are excluded from OE-1 by IFU-08 rather
than reduced.

| ID | Situation in OE-1 | S | F | P | PLr OE-1 | PLr package | What changes, and why | Measures |
|---|---|---|---|---|---|---|---|---|
| HZ-M01 | TEACH: the operator's fingers between links while hand-guiding at the 25 % torque ceiling | S2 | F2 | P1 | d | e | P1: the operator moves the arm and controls its speed; in RUN nobody is in reach (HZ-M04 covers reach-in) | SF-03, SF-04, SF-32, DM-02, DM-06 |
| HZ-M02 | TEACH or object placement: hand at the gripper jaws when they close | S2 | F1 | P2 | d | d | same | SF-04, SF-13, SF-32 |
| HZ-M03 | Assembly, repair and teach: sharp edge or loose fastener | S1 | F2 | P1 | b | b | same | DM-01 |
| HZ-M04 | RUN: foreseeable reach-in by the operator or the observer (WP-C-06 MU-01) and the arm sweeps into the head or torso | S2 | F1 | P2 | d | e | F1: nobody is in reach in RUN by rule (IFU-08); a reach-in is the misuse case, seldom and short | SF-03, SF-15, SF-32, IFU-08 |
| HZ-M05 | TEACH and maintenance: hair, a sleeve or jewellery at a joint axis | S2 | F1 | P1 | c | d | P1: the arm moves only under the operator's hand or at the TEACH ceiling while anyone is close | DM-02, IFU-06 |
| HZ-M06 | Any mode: the base tips under the payload moment if the fixing fails | S1 | F1 | P1 | a | a | same; the fixing of DM-07 and IFU-01 is a condition of OE-1 (WP-V-07 C-3) | DM-07, IFU-01 |
| HZ-M07 | Power removed by the E-stop or lost: the gripper drops its payload | S1 | F2 | P1 | b | b | same; DQ-015 requires holding above 0.5 kg | SF-13, SF-08 |
| HZ-M08 | Bench: trip on the supply or pendant cable | S1 | F2 | P1 | b | b | same | DM-03 |
| HZ-E01 | 24 V input touched during assembly or repair | S1 | F1 | P1 | a | a | same | DM-04 |
| HZ-E02 | Harness short or arc at the 24 V supply | S2 | F1 | P1 | c | c | same; the fuse F1 and disconnect Q1 of WP-H-02 are bench conditions | DM-04, SF-11, WP-H-02 F1 |
| HZ-E03 | ESD during assembly or repair | S1 | F2 | P1 | b | b | same | IFU-02 |
| HZ-E04 | EMI on the CAN bus or the camera link | S1 | F1 | P1 | a | a | same | DM-05 |
| HZ-T01 | TEACH or repair: touching a hot actuator | S1 | F2 | P1 | b | b | same | SF-14 |
| HZ-T02 | Sustained load overheats the harness | S2 | F1 | P1 | c | c | same | SF-11, SF-14 |
| HZ-N01 | Lab: gear noise near the bench | S1 | F1 | P1 | a | b | F1: one operator, sessions of limited length; the classroom exposure of the package does not arise | IFU-03 |
| HZ-V01 | TEACH: hand-arm vibration | S1 | F1 | P1 | a | a | same | IFU-06 |
| HZ-R01 | Depth camera IR illuminator pointed at an eye | S1 | F1 | P1 | a | a | same | — |
| HZ-X01 | Repair: dust from sanding printed parts | S1 | F1 | P1 | a | a | same | IFU-04 |
| HZ-G01 | Moving the arm and base | S1 | F2 | P1 | b | b | same | IFU-05 |
| HZ-G02 | TEACH: wrist strain in long sessions | S1 | F1 | P1 | a | b | F1: one operator, sessions of limited length (IFU-06) | IFU-06 |
| HZ-V02 | Lab ambient outside +10 to +35 °C | S1 | F1 | P1 | a | a | same; a lab bench is inside the envelope of IFU-07 | IFU-07 |
| HZ-V03 | A drink spilled on the bench into a joint | S1 | F1 | P1 | a | a | same | IFU-07 |
| HZ-P01 | Quasi-static contact with the head | — | — | — | — | d | not in OE-1: no contact during motion is permitted (DQ-005, no collaborative claim); reach-in is rated under HZ-M04 | excluded by IFU-08 |
| HZ-P02 | Transient contact with a hand | — | — | — | — | e | not in OE-1: as HZ-P01; hand contact in TEACH is rated under HZ-M01 and HZ-P03 | excluded by IFU-08 |
| HZ-P03 | TEACH: a finger trapped between a link and the bench or a fixture | S2 | F2 | P1 | d | e | P1: the operator guides the arm and controls the closing motion | SF-03, SF-04, SF-32, DM-02 |
| HZ-P04 | After an E-stop the operator reaches in to clear a part; the arm restarts unexpectedly | S2 | F1 | P2 | d | d | F1: reaching in after a stop is occasional in OE-1 | SF-24, SF-32, IFU-09 |
| HZ-C01 | RUN: the command stream stalls and the drives hold the last command; harm only if someone is in reach | S2 | F1 | P2 | d | e | F1: nobody is in reach in RUN except by misuse (HZ-M04) | SF-08, SF-25, SF-32 |
| HZ-C02 | An unauthenticated command starts motion while the operator is in TEACH with hands on the arm | S2 | F1 | P2 | d | d | F1: one client, a private network or none (WP-V-07 §3) | SF-26, SF-27, SF-32 |
| HZ-C03 | Encoder fault: the pose drifts and the trajectory diverges | S1 | F2 | P2 | c | c | same | SF-28 |
| HZ-C04 | RUN: an SDK race holds the last command; harm only if someone is in reach | S2 | F1 | P2 | d | e | F1: as HZ-C01 | SF-25, SF-08, SF-32 |
| HZ-C05 | A position command beyond the soft limit drives a joint into its end-stop | S1 | F2 | P2 | c | c | same | SF-29, DM-06 |
| HZ-C06 | RUN: a learned policy outputs an unsafe trajectory on an unfamiliar scene; harm only if someone is in reach | S2 | F1 | P2 | d | e | F1: the policy runs only with nobody in reach (WP-V-07 §3); the clamps of WP-C-09 bound it | SF-03, SF-04, SF-08, SF-32, WP-C-09 clamp |
| HZ-C07 | IK near a singularity spikes a joint speed | S1 | F2 | P2 | c | c | same | SF-30, SF-03 |
| HZ-D01 | The wrist camera records the operator | S1 | F1 | P1 | a | a | not a safety hazard; default-off with opt-in recording (DQ-014) | SF-31 |

| PLr in OE-1 | Rows |
|---|---|
| a | 11 |
| b | 6 |
| c | 6 |
| d | 9 |
| e | 0 |
| excluded | 2 |

No row reaches **e** in OE-1: the seven package rows at **e** all assumed a person in reach during RUN or a
classroom's exposure, and in OE-1 they rate **d** with the reason in the table. The highest PLr is **d**, which is the
target the lead set for the stop functions (DQ-004). These ratings are a draft for the reviewer of OI-2; they hold only
while the conditions of WP-V-07 hold.

## 6. Risk evaluation and reduction

Measures by step (ISO 12100 §6). The allocation per rated row is [WP-C-05](WP-C-05-risk-reduction-concept.md).

### 6.1 Inherently safe design measures

| ID | Measure | Reduces |
|---|---|---|
| DM-01 | Sharp-edge mitigation by design (chamfer, fillet) on the sheet-metal links (package SF-05) | HZ-M03 |
| DM-02 | Guarding of the joint pinch zones: covers and gaps at or below the ISO 13854 minimum (package SF-07) | HZ-M01, HZ-M05, HZ-P03 |
| DM-03 | Cable management and harness restraint at every joint (package SF-09; v1.1 cable restraints) | HZ-M08, HZ-T02, HZ-E02 |
| DM-04 | 24 V SELV supply isolation and a keyed input connector (package SF-10) | HZ-E01, HZ-E02 |
| DM-05 | EMC-shielded harness and ferrites (package SF-17) | HZ-E04 |
| DM-06 | Mechanical end-stops on every joint with the software limit inboard (with SF-29) | HZ-C05, HZ-M01 |
| DM-07 | Base fixing points documented with bolt size and torque (with IFU-01) | HZ-M06 |

### 6.2 Safeguarding and complementary protective measures

The safety functions of §7, implemented by the safety-related parts of the control system ([WP-S-03](../03-system/WP-S-03-technical-safety-concept.md)),
plus the bench chain of [WP-V-07](../06-validation/WP-V-07-test-operations.md) during development.

### 6.3 Information for use

| ID | Instruction | Reduces |
|---|---|---|
| IFU-01 | Workbench fixturing procedure before power-up (package SF-12) | HZ-M06 |
| IFU-02 | ESD-safe assembly process (package SF-16) | HZ-E03 |
| IFU-03 | Acoustic guidance for classroom use (package SF-18) | HZ-N01 |
| IFU-04 | Respiratory protection when sanding printed parts (package SF-19) | HZ-X01 |
| IFU-05 | Two-handed lift of the arm and base (package SF-20) | HZ-G01 |
| IFU-06 | Teach-mode duration and rest-break guidance (package SF-21) | HZ-G02, HZ-V01 |
| IFU-07 | Indoor-only, dry, +10 to +35 °C envelope (package SF-22) | HZ-V02, HZ-V03 |
| IFU-08 | Nobody inside the 650 mm reach while the arm is in RUN (AOU-06) | HZ-M04, HZ-P01, HZ-P02, HZ-P03 |
| IFU-09 | E-stop functional test before every session (WP-V-07 §4) | HZ-P04, HZ-C01 |

## 7. Safety functions

Identified here, specified in [WP-C-04](WP-C-04-safety-functions-and-plr.md). The PLr is the higher of the risk graph and the
ISO 10218-1 type-C value; the adopted target for the stop functions is decision DQ-004 (answered A: d).

| ID | Safety function | PLr | Cat. | Hazards addressed | Package source |
|---|---|---|---|---|---|
| SF-32 | Emergency stop | d | 3 | HZ-M01,  HZ-M04,  HZ-P01,  HZ-P02,  HZ-P03,  HZ-P04,  HZ-C01,  HZ-C04,  HZ-C06 | new in this record (GAP-08) |
| SF-08 | Safe stop on watchdog timeout | d | 3 | HZ-C01, HZ-C04, HZ-M07 | package SF-08 |
| SF-24 | Manual reset after a stop (prevention of unexpected start-up) | d | 3 | HZ-P04 | package SF-24 |
| SF-25 | Heartbeat and deadline monitor | d | 3 | HZ-C01, HZ-C04 | package SF-25 |
| SF-03 | Joint torque and speed limiting per joint | d | 3 | HZ-M01, HZ-M04, HZ-P03 | package SF-03 |
| SF-02 | Contact-force stop | d | 3 | HZ-M04, HZ-P01, HZ-P02 | package SF-02 |
| SF-04 | Collision detection by torque estimation | d | 3 | HZ-M01, HZ-M02, HZ-P02, HZ-P03 | package SF-04 |
| SF-23 | Trajectory jerk limit for transient contact | d | 3 | HZ-P02 | package SF-23 |
| SF-01 | Power-and-force limiting (ISO/TS 15066) | d | 3 | HZ-M04, HZ-P01, HZ-P02, HZ-C06 | package SF-01 |
| SF-06 | Reduced speed in the shared workspace | c | 2 | HZ-M04, HZ-P02 | package SF-06 |
| SF-11 | Overcurrent cut-off per branch | c | 2 | HZ-E02, HZ-T02 | package SF-11 |
| SF-13 | Gripper holding on power loss | c | 2 | HZ-M02, HZ-M07 | package SF-13 |
| SF-14 | Stator over-temperature shutdown | c | 2 | HZ-T01, HZ-T02 | package SF-14 |
| SF-15 | Motion-imminent annunciation | b | 1 | HZ-M04 | package SF-15 |
| SF-26 | Authenticated command channel | c | 2 | HZ-C02 | package SF-26 |
| SF-27 | Operator session lock | b | 1 | HZ-C02 | package SF-27 |
| SF-28 | Encoder plausibility cross-check | c | 2 | HZ-C03 | package SF-28 |
| SF-29 | Software joint limits with mechanical end-stops | c | 2 | HZ-C05 | package SF-29 |
| SF-30 | Singularity avoidance in inverse kinematics | c | 2 | HZ-C07 | package SF-30 |
| SF-31 | Camera default-off and opt-in recording | b | 1 | HZ-D01 | package SF-31 |

SF-01 exists in the list so that the identifier is reserved; it is **not claimed** in the first safety case (DQ-005).

## 8. Residual risk and conditions

No safety function exists on the configuration at BL-001: there is no emergency stop, no watchdog, no limit enforced outside the
client library (gap assessment §4, §5). The residual column of §5 is the package's estimate of what the functions would leave,
not a statement about the arm as built. Until the bench chain of WP-V-07 is fitted and the controller safety layer exists, no
operation with a person inside the 650 mm reach while the arm is powered in RUN is within this assessment; hand-guiding in
TEACH is within it only with the enabling and reduced-speed measures WP-C-06 §4 names, which do not exist yet either.

## 9. Hazard log cross-references

The hazards and safety functions of this document are the trace items of [`trace/items/hazards.yaml`](../trace/items/hazards.yaml),
which the safety-case validator resolves claims against; AOU-01…AOU-08 are in [`trace/items/aou.yaml`](../trace/items/aou.yaml).
The package's DFMEA failure modes FM-01…FM-27 are the seed of [WP-A-01](../08-analyses/WP-A-01-system-fmea.md) and
[WP-H-03](../04-hardware/WP-H-03-hardware-failure-analysis.md); its requirements SYRS/SRS/HWRS seed [WP-S-01](../03-system/WP-S-01-system-requirements.md)
and [WP-S-02](../03-system/WP-S-02-safety-requirements.md).

Twelve of the hazards above are drawn on upstream's CAD in [WP-P-12](../sim/README.md): the pose at the moment the
hazard occurs, a person where WP-C-06 puts them, the link gap or distance against the ISO 13854 gaps, and the stop
functions at BL-001, one dashboard per scene ([gallery](../sim/blender/dashboards/README.md)). They are pictures
for the reviewers of OI-1 and OI-2, synthetic and without evidence credit; the ratings there are this table's.

## 10. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Done in v0.2: §5.3 re-rates every row for OE-1; the package ratings stay in §5 for OE-2…OE-4. Closes when the reviewer of OI-2 confirms §5.3 | Safety manager | G1 |
| OI-2 | A reviewer who has operated the arm confirms the severity ratings, in particular HZ-M04, HZ-P02 and HZ-M06 | Verification reviewer | G1 |
| OI-3 | Done in v0.2: SF-01 is not claimed (DQ-005, answered A); HZ-P01 and HZ-P02 are excluded from OE-1 by IFU-08 in §5.3 | Safety manager | G1 |
| OI-4 | Rate the threat scenarios of WP-C-07 that reach a hazard and add the resulting rows | Cybersecurity manager | G1 |
| OI-5 | Add the CFG-002 (RobStride) rows once the RS BOM is released (DQ-001 and DQ-017, answered A: tracked, unverified) | Safety manager | G1 |
