# WP-M-07 Project risk management plan and register

| Field | Value |
|---|---|
| Work product | WP-M-07 Project risk management plan and register |
| Standard reference | ASPICE: MAN.5. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: process, scales, roles, register R-01…R-13 seeded from WP-M-01 §9 and the decision answers; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How the project identifies, analyses, treats and monitors project risks: events that could stop the fork from
achieving the assurance path on its planned scope, effort and quality. Product risks (hazards to people) belong to
the risk assessment ([WP-C-03](../02-concept/WP-C-03-risk-assessment.md)), not here; a project risk that would
weaken a safety claim is also raised as a defeater in the safety case
([WP-K-01](../10-safety-case/WP-K-01-safety-case.md)). Strategic decisions D-nn of
[WP-M-01 §8](WP-M-01-assurance-strategy.md#8-strategic-decisions) are logged in §5.

## 2. Risk management process

| Step | What is done |
|---|---|
| Identify | Sources: the [gap assessment](../00-assessment/gap-assessment.md), [WP-M-01 §9](WP-M-01-assurance-strategy.md#9-risks-to-the-plan), gate reviews, QA and confirmation findings ([WP-M-05](WP-M-05-quality-assurance-plan.md), [WP-M-06](WP-M-06-confirmation-measures-plan.md)), upstream changes ([WP-M-10](WP-M-10-upstream-and-supplier-management.md)), answers in the decision register. Anyone may propose a risk by issue or pull request |
| Analyse | Probability P and impact I on the scales below; exposure = P × I |
| Treat | Avoid (change the plan so the event cannot occur), mitigate (reduce P or I), transfer (to a party who accepts it in writing), or accept (recorded, with the owner's name) |
| Monitor | Each risk has a trigger that makes it due for review; the whole register is reviewed at every gate review ([WP-M-02 §10](WP-M-02-safety-plan.md#10-progress-tracking-and-gate-reviews)) and when a decision is answered |
| Close | When the event can no longer occur or has occurred and been handled; the row stays with status Closed |

| Score | Probability (before the next gate) | Impact |
|---|---|---|
| 1 | Rare: below 10 % | Negligible: no effect on a gate |
| 2 | Unlikely: 10 to 30 % | Minor: delays a work product, not a gate |
| 3 | Possible: 30 to 60 % | Moderate: delays a gate, or the record must state a new limitation |
| 4 | Likely: 60 to 90 % | Major: blocks a gate or a claim until treated |
| 5 | Almost certain, or already the case | Severe: blocks safe powered testing or the whole assurance path |

Exposure bands: **High** 15 and above, **Medium** 8 to 14, **Low** 7 and below. A High risk is reviewed at every gate
review and named in the gate record; a High risk accepted without mitigation needs the project lead's answer in the
decision register.

## 3. Roles

The project maintainer owns this register and each risk has a named owner. The safety manager agrees every accepted
risk that touches a safety claim. Today both are the same person, so that agreement is self-approval at I0
(DQ-010, answered A). The scores below are the author's judgement at I0 and have not been reviewed.

## 4. Risk register

| ID | Risk | P | I | Exposure | Treatment | Owner | Trigger | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | The bench safety chain is not bought in time: it is designed ([WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md)), its estimate grew from €250–450 (DQ-006) to €500–800 (WP-H-02 §4), and no budget is recorded. Without it no powered test with a person in reach, so no stopping or holding measurement for G1 | 3 | 5 | 15 High | Mitigate: buy per WP-H-02 §4 (ACT-005); record a budget (WP-M-03 OI-4). Meanwhile the empty-bench rule of WP-V-07 §1 | Project maintainer | No purchase by the G0 review; any plan for a powered test | Open |
| R-02 | One person holds every role: no review above I0, no QA, no confirmation measure, self-approval everywhere | 5 | 4 | 20 High | Accept for now (DQ-010, answered A) and mitigate: any second contributor's review counts ([CONTRIBUTING.md](../../CONTRIBUTING.md)); the assessor is revisited at G1 (DQ-009) | Project maintainer | Each gate review; a contributor offers to review | Open |
| R-03 | AI-drafted work outpaces review: most of the record is drafted in Claude Code sessions and one person reviews and merges it, so an unsupported claim or a wrong clause reference can pass unnoticed | 4 | 4 | 16 High | Mitigate: the session rules of [CLAUDE.md](../../CLAUDE.md); the pull request checklist line on unsupported claims; Draft status until reviewed; CI checks; tool classification in WP-P-07 (WP-M-02 OI-4) | Safety manager | A claim found unsupported; each gate review | Open |
| R-04 | No assessor: CR-01 and CR-03 are due at G0 and CR-02, CR-04 and FSA-I1 at G1, and none can be performed | 5 | 3 | 15 High | Accept at G0 (DQ-009, answered A); whether G0 may pass with its measures scheduled is the gate decision (WP-M-06 OI-5); revisit at G1 | Safety manager | G0 review; G1 planning | Open |
| R-05 | The software forks are decided (DQ-007) but not made; until they exist no watchdog, mode machine, clamp or authentication can be built, and upstream may diverge meanwhile | 3 | 4 | 12 Medium | Mitigate: create and pin the forks (ACT-004); track upstream changes under WP-M-10 | Configuration and change manager | G0 review without the forks; an upstream SDK or driver release | Open |
| R-06 | No supplier reliability data for the actuators, so no PL calculation can close on a channel that includes one | 2 | 4 | 8 Medium | Avoid: generic values only and no actuator in a PL d channel (DQ-019, answered B; WP-M-01 T-05) | Safety-related control system engineer | WP-H-04 or WP-S-03 puts an actuator in a channel | Open |
| R-07 | No standard is held, so clause numbers may be wrong, and the 2025 editions of ISO 10218 changed the collaborative text | 4 | 3 | 12 Medium | Accept until an assessor is engaged (DQ-011, answered B); every clause reference marked as to be checked (WP-M-06 OI-1) | Safety manager | Assessor engaged; G1 review | Open |
| R-08 | The CC BY-NC-SA 4.0 licence: a safety-assured build used in a workplace may be commercial use upstream forbids (GAP-35) | 3 | 3 | 9 Medium | Mitigate: settle which envelopes the licence allows (ACT-010); [WP-M-13](WP-M-13-regulatory-conformity-strategy.md) | Project maintainer | A proposal to use a build outside OE-1; G1 review | Open |
| R-09 | A learned component becomes a safety component, pulling the arm into Annex I Part A of the Machinery Regulation and the AI Act | 2 | 4 | 8 Medium | Avoid: no safety function on a learned component (DQ-008, answered A; WP-M-01 T-03) | ML safety lead | Any proposal to give a policy a safety role; WP-C-09 | Open |
| R-10 | The limits the analyses rest on (mass, fixing, joint gaps, end-stop angles, stopping performance) stay unmeasured, so the risk assessment rates estimates | 4 | 3 | 12 Medium | Mitigate: measure without power in P1 (ACT-001, ACT-002); stopping after the chain is fitted (WP-V-02) | Safety manager | G1 planning; no arm on the bench (WP-M-03 OI-3) | Open |
| R-11 | Upstream changes the hardware (a new revision, the RS BOM) and invalidates analyses already written | 3 | 3 | 9 Medium | Mitigate: impact analysis on every upstream merge ([WP-M-11](WP-M-11-impact-analysis.md)); CFG-002 tracked, every value unverified (DQ-017) | Configuration and change manager | An upstream merge that touches `hardware/` | Open |
| R-12 | The dedicated safety controller (DQ-020) needs firmware written and verified, and no firmware engineer other than the lead is named | 3 | 4 | 12 Medium | Mitigate: keep the controller's scope to the watchdog, mode machine, clamps and plausibility checks; seek a contributor before G3 | Project maintainer | WP-S-03 allocation at G2 | Open |
| R-13 | Decisions wait on one lead who reviews from a phone, and a gate waits with them | 2 | 3 | 6 Low | Mitigate: questions in batches of ten on the inbox page; `proceed_after` for easy questions (decision register README) | Project maintainer | A blocking question open for two weeks | Open |

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
| OI-1 | Review the register and its scores at the G0 gate review and record the result in the gate record | Project maintainer | G0 |
| OI-2 | Raise R-02, R-03 and R-04 as defeaters in the case records where they weaken a claim, or record why not | Safety manager | G1 |
| OI-3 | Move each D-nn of §5 to applied in the decision register as its change is made | Safety manager | G1 |
