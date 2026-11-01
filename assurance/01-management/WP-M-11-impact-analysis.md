# WP-M-11 Impact analysis of the inherited reBot-DevArm baseline

| Field | Value |
|---|---|
| Work product | WP-M-11 Impact analysis of the inherited reBot-DevArm baseline (modification of existing machinery) |
| Standard reference | Machinery: 12100 §4; SRP/CS: 61508-1 §7.16 (modification); IEC 62443: 62443-4-1 SM-3; Other: Machinery Reg. Art. 3 (substantial modification); ASPICE: SUP.10. Clause numbers are to be checked against licensed copies ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1) |
| Version | 0.1 (first draft: the baseline including the three software repositories found on 2026-11-01, reuse class per element E-01…E-10, consequences for the lifecycle, the format of change impact records; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

Impact analysis of using the inherited reBot-DevArm as the starting point of a machine that is to carry a safety
case: what is reused, what is hardened, what is replaced or added, what is new, and what each inherited element's
state means for the lifecycle entry (tailoring T-01, [WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring)). It
also sets the format of every later change impact record (§5). It is an analysis on paper: nothing in it was built,
measured or tested.

## 2. Baseline

| Part | State analysed | Source |
|---|---|---|
| Hardware record | `jherrodthomas/reBot-DevArm@206ebda`: upstream hardware v1.1 of 2026-04-25 (STEP, BOM, performance test) | [gap assessment](../00-assessment/gap-assessment.md) header; BL-001 in `assurance/case/baselines/baselines.yaml` |
| Concept-phase package | The workbooks and documents of 2026-05-04 at the repository root | gap assessment §1 |
| Software | Unpinned at `206ebda`. On 2026-11-01 the stack was found to be three upstream repositories, recorded at `motorbridge/motorbridge@d5700bc`, `Seeed-Projects/reBotArm_control_py@d4f3591` and `Yang-Ci/ReBot_Arm_DigitalTwin_DM@7456d8b` (full hashes in [WP-M-10 §2.2](WP-M-10-upstream-and-supplier-management.md#22-the-software-that-moves-the-arm)); these become the BL-001 software pins once the forks exist (DQ-007, answered A) | WP-M-10 |
| Actuator firmware | Closed Damiao firmware; version not recorded | GAP-16 |
| Configuration | CFG-001, the B601-DM v1.1 (DQ-001, answered A); CFG-002 the B601-RS tracked only (DQ-017, answered A) | [WP-C-01 §1](../02-concept/WP-C-01-item-definition.md#1-item-identification) |

Every finding GAP-01…GAP-36 of the gap assessment is an input. The analysis is against BL-001 as inherited, with no
fork change made to hardware or software ([`impact/`](../07-supporting/impact/README.md) holds no record yet).

## 3. Reuse classification per element

Classes: **R** reuse unchanged; **R-V** reuse once a measurement or test confirms an assumption; **H** reuse with
hardening (changed by the fork, no PL claim); **P** reuse pinned, unmodified (no right or no need to change);
**A** replace or add; **N** new; **X** not reused. Elements are those of [WP-C-01 §3.1](../02-concept/WP-C-01-item-definition.md#31-inside-the-item).

| Element | Inherited state | Class | Rationale | Gaps carried | Work products |
|---|---|---|---|---|---|
| E-01 Mechanical structure | v1.1 links, covers, limit blocks; gaps, end-stop angles, mass and fixing unmeasured | R-V | Sound design reused; the limits it implies must be measured before WP-C-03 rates them. Printed substitutes for load-bearing machined parts are excluded (AOU-03) | GAP-01…GAP-05 | WP-H-08, WP-C-01 OI-1, OI-2 |
| E-02 Actuators (DM4310, DM4340P) | Closed firmware; no reliability data | R | Not safety-related (T-05); a channel of no PL d function (DQ-019, answered B); firmware version recorded per arm | GAP-13, GAP-14 | WP-M-10 §3, WP-H-07 |
| E-03 Gripper | Holding on power loss unknown | R-V | Reused if the test shows holding above 0.5 kg (DQ-015, answered A); otherwise it becomes A | GAP-07 | SF-13, WP-V-02 |
| E-04 Harness and bus | One XT30 chain; termination and branch protection undocumented; input not polarised | H | Termination checked; polarised input and branch protection added | GAP-10, GAP-12, GAP-15 | WP-H-05 |
| E-05 CAN-USB adapter | The host's direct path to the bus | R, role changed | With the controller between the host and the bus (DQ-020, answered A) the host no longer reaches the bus directly; where the adapter sits is settled in WP-S-03 and WP-S-05 | GAP-22 | WP-S-03, WP-S-07 |
| E-06a `motorbridge` | MIT; unpinned | H | Forked, pinned, changed: authenticated session, bounds mirrored from the controller; built from source | GAP-16, GAP-19, GAP-22, GAP-23 | WP-W-02…W-07, WP-W-11 |
| E-06b `reBotArm_control_py` | No licence; unpinned | P | Forked and pinned; may not be modified until a licence is stated (WP-M-10 OI-2); its gravity compensation and IK run behind the controller clamps | GAP-16, GAP-26 | WP-P-08 |
| E-06c `ReBot_Arm_DigitalTwin_DM` | Licence ambiguous; unpinned; web control and agents | P | Forked and pinned, not modified (WP-M-10 OI-3); web control and agents unused in OE-1 until authenticated | GAP-16, GAP-23, GAP-24 | WP-P-08, WP-C-07, WP-C-09 |
| E-06d Other host software (ROS 2, MoveIt 2, Pinocchio, LeRobot, YOLO demo, web UI) | Upstream, unpinned | P | Pinned by version; no safety function depends on it (T-04) | GAP-16, GAP-24 | WP-P-08, WP-M-09 |
| E-07 Controller safety layer | Does not exist | N | Watchdog, mode machine, clamps, plausibility on a dedicated controller (DQ-020, answered A) | GAP-17…GAP-20, GAP-24 | WP-S-03, WP-W-01…W-09 |
| E-08 Bench safety chain | Does not exist; no E-stop in the BOM | N | Two-channel E-stop, safety relay, two contactors (DQ-006, answered A; [WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md)) | GAP-08, GAP-31 | WP-H-02, WP-H-04, WP-V-04 |
| E-09 24 V supply | Open-frame LRS-350-24, no disconnect, no fuse | R (PSU), A (installation) | PSU reused; enclosure, switched fused inlet, lockable disconnect and fuses added (DQ-018, answered A) | GAP-09, GAP-11 | WP-H-02, WP-H-05 |
| E-10 Camera and leader arm | Camera streams by default; leader arm unauthenticated | H | Camera default-off, opt-in recording (DQ-014, answered A; SF-31); leader arm as an authenticated client | GAP-23, GAP-25 | WP-C-08, WP-W-11 |
| Upstream wireless stop (XIAO ESP32) | Mentioned, unspecified | X | Not accepted as a stop; at most an addition to the pendant | GAP-08 | WP-V-07 §3 |
| Concept-phase package | 33 hazards, 31 SF candidates, 104 requirements, 127 test cases; unreviewed, no test run | Input | Identifiers kept; content re-derived in the concept work products; never edited, never a reused safety work product (T-01) | GAP-27, GAP-31 | WP-C-03, WP-C-04, `trace/` |
| Upstream thermal test and documentation | One thermal test; assembly video, wiki | Input | Supporting evidence only (T-06) | GAP-29, GAP-33 | WP-P-09, WP-O-01, WP-O-03 |

## 4. Consequences for the lifecycle

1. **Full concept phase.** No safety function exists on the inherited arm, so there is nothing to modify in the
   sense of IEC 61508-1 §7.16: the safety functions are new development. Modification analysis applies only to the
   reused elements of §3, each through its class.
2. **No inherited safety work product.** The concept-phase package is an input to every concept work product, never
   evidence until reviewed ([WP-K-01](../10-safety-case/WP-K-01-safety-case.md) Sn-04).
3. **Regulatory status.** The inherited arm was never CE-marked, so the fork's arm is not a substantial
   modification of a conforming machine but new machinery with a whole technical file
   ([WP-M-13 §2](WP-M-13-regulatory-conformity-strategy.md#2-what-the-fork-is-in-regulatory-terms)).
4. **The controller safety layer and the chain are new** and follow the full hardware and software lifecycle of
   [WP-M-02 §4](WP-M-02-safety-plan.md#4-lifecycle-activities-per-phase); the chain is built early as bench equipment
   under [WP-M-02 §4.1](WP-M-02-safety-plan.md#41-early-implementation-of-at-risk-work).
5. **The host software is hardened as defence in depth** with no PL claim (T-04). Where hardening is needed in a
   repository the fork may not modify (E-06b, E-06c), the measure goes to the controller or to `motorbridge` instead.
6. **Cybersecurity applicability (62443-4-1 SM-3).** The 4-1 practices apply to the fork's repositories; the three
   upstreams and the other host software are externally provided components ([WP-M-08 §2.3](WP-M-08-cybersecurity-plan.md#23-software-supplied-from-upstream)).
7. **CFG-002 is not covered by this entry.** It joins through its own impact record when the RS BOM is released.

## 5. Change impact analysis records

Later changes are analysed one by one under [`07-supporting/impact/`](../07-supporting/impact/README.md); this
document covers only the entry. A record is required for every change on an SR-A, SR-Q or SR-T path of
[`safety-relevant-paths.txt`](../07-supporting/safety-relevant-paths.txt), for every upstream merge or pin bump
([WP-M-10 §2](WP-M-10-upstream-and-supplier-management.md#2-upstream)), and for every change to a learned component
([WP-M-09](WP-M-09-ml-safety-plan.md)). File name `change-<YYYY-MM-DD>-<slug>.md`, with this table:

| Field | Content |
|---|---|
| Change | What changes, the pull request(s) and the repositories touched |
| Class | SR-A, SR-Q or SR-T per the path list; NSR needs no record |
| Configurations | CFG-001, CFG-002 |
| Elements | E-nn of WP-C-01 and their reuse class from §3 (a change of class is stated) |
| Hazards and functions | HZ-nn, SF-nn, requirements, AOU-nn, threat scenarios TS-nn, learned components ML-nn affected, or "none" with the reason |
| Work products re-opened | Each with the section to update |
| Regulatory screen | Does the change alter the intended use, add a hazard or raise a risk; does it allocate anything to a learned component (WP-M-09 §4.1); if yes, the lead decides before merge |
| Verification | Planned and done, with results |
| Open items | Residual items with owner and due |
| Approval | Approver and independence level (I0 while DQ-010 holds) |

The first records expected are the bench safety chain build (WP-H-02 OI-8), the creation and pinning of the three
forks, and the first `motorbridge` change.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Confirm the three forks exist and write the first impact record for their creation and pinning, with the fork URLs | Configuration and change manager | G0 |
| OI-2 | Extend BL-001 with the software pins and the actuator firmware version, or cut BL-002 if BL-001 is to stay the inherited state (WP-P-01) | Configuration and change manager | G0 |
| OI-3 | Record the reuse class change for E-06b and E-06c from P to H if their authors state a permissive licence | Safety manager | When answered |
| OI-4 | Settle where the CAN-USB adapter sits once the controller is in the path (E-05) | Safety-related control system engineer | G2 |
| OI-5 | Re-run §3 for CFG-002 when the RS BOM is released (DQ-017) | Safety manager | At release |
