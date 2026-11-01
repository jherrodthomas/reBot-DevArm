# WP-M-07 Project risk management plan and register

| Field | Value |
|---|---|
| Work product | WP-M-07 Project risk management plan and register |
| Standard reference | ASPICE: MAN.5 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

How the project identifies, analyses, treats and monitors project risks: events that could stop the fork from achieving the assurance path on its planned scope, effort and quality. Product risks belong to the risk assessment (WP-C-03), not here. Strategic decisions D-nn of WP-M-01 §8 are logged in §5.

## 2. Risk management process

Identification sources (gap assessment, WP-M-01 §9, gate reviews, QA and confirmation findings, upstream changes); probability and impact scales 1–5; exposure = P × I with High ≥ 15, Medium 8–14, Low ≤ 7; treatments avoid, mitigate, transfer, accept; review at every gate.

## 3. Roles

Project maintainer owns the register; safety manager agrees accepted risks that touch a safety claim.

## 4. Risk register

R-nn rows: description, P, I, exposure, treatment, owner, trigger, status. Seeded from WP-M-01 §9: no funding for the bench safety hardware; one person in every role; no supplier reliability data for the actuators; the software stack lives in upstream repositories the fork does not control; no licensed standards; the non-commercial licence.

## 5. Decision log

D-01…D-nn of WP-M-01 §8 with the register entry, the answer and where it was applied. The decision register is the place a question is asked; this log is where a strategic decision is recorded once applied.

The lead answered batch 1 of the register on 2026-11-01, in chat, with the recommended option of each, and batch 2 the
same day on the inbox page, choosing option B for D-11 and D-19. The answers are copied into the register
(`status: answered`); each moves to `applied` when the change below is made.

| ID | Decision | Register | Answer (2026-11-01) | What applying it takes |
|---|---|---|---|---|
| D-01 | Reference configuration | DQ-001 | A: the B601-DM v1.1 now, the RS tracked as CFG-002 | How the RS is tracked is DQ-017 |
| D-02 | Regulatory frame | DQ-002 | A: the EU frame | The record already cites it; WP-M-13 to be written to it |
| D-03 | First operating envelope | DQ-003 | A: OE-1 only, the supervised bench | WP-C-02 OI-1: rewrite §2 to the answer |
| D-04 | Required PL for the stop functions | DQ-004 | A: PL d for the stops, PL c for the limits and diagnostics | WP-C-04 §4 already carries it |
| D-05 | Collaborative claim | DQ-005 | A: none; separation only | WP-C-06 OI-1: rewrite §4 to the answer |
| D-06 | Bench safety chain | DQ-006 | A: wired two-channel E-stop, safety relay, contactor, fuse, lockable disconnect | Design and buy it; fit it before any powered test (WP-V-07 OI-1) |
| D-07 | Fork the software that moves the arm | DQ-007 | A: fork the SDK and the ROS 2 driver now; pin them in BL-001 | Create the two fork repositories and pin them |
| D-08 | Learned policies | DQ-008 | A: in the item, outside every safety function, behind the clamps | WP-C-09 to be written to it |
| D-09 | Independent assessor | DQ-009 | A: not for now; revisit at G1 | Recorded in WP-M-02 §3.1 and WP-M-06 |
| D-10 | Roles while one person holds them | DQ-010 | A: self-approval at I0, recorded as such | Recorded in WP-M-02 §3.1 |
| D-16 | Bench speed and torque ceilings | DQ-016 | A, assumed (decider: claude): 50 % in RUN, 25 % in TEACH until WP-V-02 | Configured and read back before the first powered test (WP-V-07) |
| D-11 | Buying the standards | DQ-011 | B (inbox): buy nothing until an assessor is engaged | Every clause reference stays marked to be checked through G1; revisited with the assessor at G1 |
| D-12 | Conformity route | DQ-012 | A (inbox): Module A, internal control | NB-1 withdrawn in WP-M-06; WP-M-13 §3 to be written to it |
| D-13 | Security level target | DQ-013 | A (inbox): SL 2 for FR 1, 3, 4; SL 1 for the rest | WP-C-08 §2 to be written to it |
| D-14 | Camera privacy default | DQ-014 | A (inbox): default-off, opt-in recording, local storage | SF-31 in WP-C-04; WP-C-08 |
| D-15 | Gripper holding on power loss | DQ-015 | A (inbox): holding required above 0.5 kg; below, a payload and height limit | SF-13 in WP-C-04; the holding test in WP-V-02 |
| D-17 | The RS variant | DQ-017 | A (inbox): CFG-002, tracked, every value unverified | WP-C-01 §1.2 |
| D-18 | Supply disconnect | DQ-018 | A (inbox): enclosed PSU with a mains switch, and a lockable DC disconnect and fuse | WP-H-02 E-09 and OI-4; WP-H-05 |
| D-19 | Supplier reliability data | DQ-019 | B (inbox): generic values only; the actuators are a channel of no PL d function | WP-H-02 already removes power by contactor; WP-H-04 and WP-M-10 to say no request is made |
| D-20 | Where the safety layer runs | DQ-020 | A (inbox): a dedicated controller between the host and the bus | WP-S-03 allocation; WP-A-05; the bench BOM |

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
