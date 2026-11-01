# WP-M-03 Project plan

| Field | Value |
|---|---|
| Work product | WP-M-03 Project plan (scope, WBS, schedule, resources) |
| Standard reference | ASPICE: MAN.3. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: scope, work breakdown per phase, sequence to the first powered test, resources and recorded costs; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

This plan sets the scope, the work breakdown, the sequence and the resources of the assurance path for the
reBot-DevArm fork. It does not repeat the strategy ([WP-M-01](WP-M-01-assurance-strategy.md)) or the safety
activities per phase ([WP-M-02 §4](WP-M-02-safety-plan.md#4-lifecycle-activities-per-phase)); it says what has to be
done, in what order, by whom, and with what money and hardware.

The project as it stands on 2026-11-01: one maintainer, no gate passed, phase P0 Governance under way. The record
was drafted from 2026-10-20 in Claude Code sessions and merged as pull requests #1 to #8 between 2026-10-23 and
2026-11-01, each merged by the maintainer. All twenty decisions DQ-001…DQ-020 are answered or assumed
([WP-M-07 §5](WP-M-07-risk-management.md#5-decision-log)). No safety hardware has been bought, no software has been
forked and no powered test has been run under the fork.

## 2. Scope

| In scope | Out of scope |
|---|---|
| CFG-001, the B601-DM v1.1, on a fixtured, supervised bench in OE-1 ([WP-M-01 §3.1](WP-M-01-assurance-strategy.md#31-reference-configuration-the-only-scope-claims-apply-to); DQ-001, DQ-003) | Any claim for the B601-RS: tracked as CFG-002, every value unverified until its BOM is released (DQ-017) |
| The work products of [WP-M-00 §3](WP-M-00-work-product-register.md#3-register), 90 rows across gates G0…G6 | Other operating envelopes (the package's OE-2…OE-4), a mobile base, a second arm, a non-upstream end effector (WP-M-01 T-14) |
| The bench safety chain of [WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md) (DQ-006, DQ-018) | Placing any build on the market; the licence forbids commercial use (GAP-35) |
| Forks of the SDK and the ROS 2 driver, pinned in the baseline (DQ-007), and a dedicated safety controller between the host and the bus (DQ-020) | Changes to `hardware/`, which is upstream's record and only merged |
| The decision register, the Living Safety Case records, the process model, the wiki | Upstream's software, the actuators' closed firmware, the site network (WP-M-01 T-02, T-11) |

## 3. Work breakdown

One line per phase. The work products and their gates are those of WP-M-00 §3; the engineering work is the work that
produces evidence outside the documents. No effort estimate is recorded for any phase (OI-2).

| Phase | Gate | Work products (WP-M-00) | Engineering work outside the documents | Starts when |
|---|---|---|---|---|
| P0 Governance | G0 | 21: WP-M-00…M-13, WP-P-01…P-06, WP-P-11 (6 Draft, 15 Skeleton in the register at this version) | Branch protection and CODEOWNERS on GitHub ([WP-M-04 §2](WP-M-04-organization-competence-safety-culture.md#2-organisation-rules)); the two software forks created and pinned (ACT-004) | Under way |
| P1 Concept | G1 | 12 gated at G1 (WP-C-01…C-10, WP-V-07, WP-P-12), plus the first versions of WP-K-01 and WP-T-01 | Weigh the arm and record the fixing (ACT-001); measure the joint gaps and end-stop angles (ACT-002); buy, wire and check the bench chain (ACT-005); the holding test on power loss (ACT-003) | G0 passed; the unpowered measurements may start earlier as at-risk work (WP-M-02 §4.1) |
| P2 System design | G2 | 13 (WP-S-01…S-07, WP-H-08, WP-A-01…A-05) | The response-time and stopping budget needs the stopping angles of the first powered tests | G1 passed |
| P3 HW/SW development | G3 | 18 (WP-H-01…H-05, H-07, WP-W-01…W-06, W-09…W-11, WP-P-07…P-09) | The dedicated controller: board, firmware, unit verification (DQ-020); host hardening in the forks | G2 passed |
| P4 Integration and verification | G4 | 9 (WP-S-08, S-09, WP-H-06, WP-W-07, W-08, WP-V-02…V-05) | The bench campaign: stopping, holding, separation, E-stop, fault injection | G3 passed; bench available |
| P5 Validation and release | G5 | 13 (WP-V-01, V-06, V-08, WP-P-10, WP-O-01…O-03, WP-K-02…K-07) | Validation runs on the arm; the functional safety assessment (needs an assessor, DQ-009) | G4 passed |
| P6 Operation | G6 | 2 (WP-O-04, O-05) | Field monitoring and updates of the fork releases | G5 passed |

## 4. Schedule and resources

### 4.1 Sequence

No gate date is set. The lead answered both decision batches on 2026-11-01, so dates can now be planned (OI-1).
The order below follows the dependencies in the record:

| # | Milestone | Depends on | Source |
|---|---|---|---|
| M-1 | The G0 work products written to Draft | This batch of G0 drafts | WP-M-00 §3 |
| M-2 | G0 gate review held | M-1; the verification reviewer and QA roles (WP-M-02 OI-1); a decision whether G0 may pass with CR-01 and CR-03 scheduled rather than performed (WP-M-06 OI-5) | WP-M-02 §10 |
| M-3 | Software forks created and pinned in the baseline | DQ-007 (answered A) | ACT-004 |
| M-4 | Arm weighed, fixing recorded, joint gaps and end-stop angles measured, without power | An arm on the bench (OI-3) | ACT-001, ACT-002 |
| M-5 | Bench chain bought, wired and checked | Money (§4.3); WP-H-02 §4 parts confirmed against datasheets | ACT-005; WP-H-02 |
| M-6 | First powered test with a person in reach | M-5; WP-V-07 approved; an operator trained per WP-M-04 §5 | [WP-V-07 §2](../06-validation/WP-V-07-test-operations.md#2-conditions-before-any-powered-test) |
| M-7 | G1 gate review, with the assessor (DQ-009) and the standards purchase (DQ-011) revisited | The G1 work products; M-4; the stopping and holding results that need M-6 | WP-M-06 §9 |

Until M-5 holds, the arm may be run only with the whole bench area empty and the operator at the supply's switch
(WP-V-07 §1).

### 4.2 People

One person, Jherrod Thomas, holds every assigned role in [WP-M-02 §3.1](WP-M-02-safety-plan.md#31-role-assignments);
the verification reviewer, QA, electrical and mechanical engineer, test bench owner, test operator and assessor roles
are TBD. Drafting is done in Claude Code sessions under the lead's direction (WP-M-02 §3.3); that adds authoring
capacity, not review capacity. Every approval is self-approval at I0 until a second person joins (DQ-010).

### 4.3 Money and hardware

No budget is recorded. The costs the record names:

| Item | Cost in the record | State | Source |
|---|---|---|---|
| Bench safety chain: E-stop stations, safety relay, two contactors, lockable DC disconnect, fuses, enclosure, PSU enclosure and inlet, wiring | Roughly €500 to €800, excluding VAT (the DQ-006 option estimated €250 to €450 before the chain was designed) | Designed, not bought | [WP-H-02 §4](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md#4-parts); DQ-006, DQ-018 |
| Dedicated safety controller board | Roughly €30 to €80, plus firmware effort | Decided, not designed | DQ-020 |
| Standards | €600 for three or €1,500 for the set (option figures) | Deferred until an assessor is engaged | DQ-011 (B) |
| Independent assessor | €2,000 to €6,000 for G0 and G1 (option figure) | Not for now; revisit at G1 | DQ-009 (A) |
| Notified body | None planned | Module A | DQ-012 (A) |

The repository does not record that an arm is on hand for the bench, or which one (OI-3).

### 4.4 Tools

GitHub (issues, pull requests, private vulnerability reporting), GitHub Actions running the `assurance` and `wiki`
workflows on every pull request, Python 3 for the checkers and generators, and Claude Code for drafting. The tools'
classification is [WP-P-07](../07-supporting/WP-P-07-tool-classification-qualification.md) (WP-M-02 OI-4).

### 4.5 Tracking

Progress is tracked as [WP-M-02 §10](WP-M-02-safety-plan.md#10-progress-tracking-and-gate-reviews) sets out: the
status column of WP-M-00, the open items of each work product, the open risks of WP-M-07, the decision register, the
generated gate skeletons and the safety-case dashboard. This plan is updated at every gate review and when a
milestone of §4.1 moves.

## 5. Risks to the plan

Project risks are registered in [WP-M-07 §4](WP-M-07-risk-management.md#4-risk-register). The ones rated High that
bear on this plan: the bench chain not yet bought (R-01), one person in every role (R-02), the volume of AI-drafted
work against one reviewer (R-03), and G0 and G1 confirmation measures with no assessor (R-04).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Set target dates for M-2 to M-7 with the lead | Project maintainer | G0 |
| OI-2 | Estimate effort per phase of §3, using the P0 pull requests as the first data point | Project maintainer | G0 |
| OI-3 | Record which arm the bench uses (configuration, serial or kit batch, assembled by whom) or plan its purchase | Project maintainer | G1 |
| OI-4 | Record a budget, or that the lead funds purchases case by case, for the bench chain and the controller board | Project maintainer | G0 |
