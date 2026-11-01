# WP-M-12 Process capability baseline

| Field | Value |
|---|---|
| Work product | WP-M-12 Process capability baseline (ASPICE self-assessment) |
| Standard reference | ASPICE: All in scope. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: scope, PA 1.1 self-rating per process at 2026-11-01, targets per gate, improvement plan; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

A self-assessment of the fork's engineering processes against ASPICE PAM 4.0, used as the process capability frame
([WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring) T-12): where the project stands and what each gate needs.
T-12 sets the end targets: CL2 for the management, support, system and software processes, CL1 for hardware and
machine learning.

This is not an ASPICE assessment. It was made by the author at I0, without a licensed copy of the PAM, and no
qualified assessor has seen it. Process names and IDs are from memory of PAM 4.0 and are to be checked (OI-1).

## 2. Scope

MAN.3, MAN.5, SUP.1, SUP.8, SUP.9, SUP.10, SYS.1–5, SWE.1–6, HWE.1–4, VAL.1, MLE.1–4. ACQ.4 (supplier monitoring,
for upstream and the actuator makers) and SUP.11 (machine-learning data management) are added because the register's
ASPICE column names them for [WP-M-10](WP-M-10-upstream-and-supplier-management.md) and
[WP-W-10](../05-software/WP-W-10-ml-engineering.md).

Outside this baseline: the cybersecurity processes the register names (MAN.7, SEC.1–4) belong to a separate
cybersecurity extension of ASPICE and are left to [WP-M-08](WP-M-08-cybersecurity-plan.md). The register also names
SUP.2 and SUP.7, which are not in the process list above (OI-1).

## 3. Assessment

Rating: process attribute PA 1.1 (process performance) as N, P, L or F (not, partly, largely, fully achieved). A
process is at CL1 when PA 1.1 is at least L. No PA 2.x is rated because no process reaches CL1. Evidence is the
repository on `main` at 2026-11-01 (merge of pull request #8, `9758f68`). A plan that exists but has not been carried
out is a work product, not a performed process, and counts only toward planning outcomes.

| Process | PA 1.1 | CL | Evidence in the repository | CL1 by | CL2 by |
|---|---|---|---|---|---|
| MAN.3 Project management | P | 0 | Scope, lifecycle, gates and work products defined (WP-M-00, WP-M-01, WP-M-02, the process model); decisions recorded in the register. No schedule, no effort estimate, no gate held, no progress monitored against a plan | G0 | G2 |
| MAN.5 Risk management | P | 0 | Risks to the plan listed in WP-M-01 §9 and answered through the decision register; no register reviewed over time | G0 | G2 |
| SUP.1 Quality assurance | N | 0 | No QA role filled, no QA check or audit performed ([WP-M-05](WP-M-05-quality-assurance-plan.md)) | G1 | G2 |
| SUP.8 Configuration management | P | 0 | Git and pull requests; BL-001 recorded in `case/baselines/`; the safety-relevant file list; CI fails on stale generated files. No tagged baseline; the software the arm runs is unpinned (GAP-16) | G0 | G2 |
| SUP.9 Problem resolution management | P | 0 | Problem report and safety concern forms with safety triage; no problem raised and handled yet | G0 | G2 |
| SUP.10 Change request management | P | 0 | Pull request template with a safety-impact statement and change classes; no impact record yet under `07-supporting/impact/` | G0 | G2 |
| SYS.1 Requirements elicitation | P | 0 | Stakeholder decisions DQ-001…DQ-020 recorded; WP-C-01 and WP-C-02 Draft; the package's 104 requirements are an unreviewed input | G1 | G2 |
| SYS.2 System requirements analysis | P | 0 | Safety functions with PLr in WP-C-04 (Draft); WP-S-01 and WP-S-02 Skeleton | G1 | G2 |
| SYS.3 System architectural design | P | 0 | The three-layer argument of WP-M-01 §6; the bench chain design WP-H-02 (Draft); WP-S-03 Skeleton | G2 | G3 |
| SYS.4 System integration and integration verification | N | 0 | Nothing built or integrated | G4 | G5 |
| SYS.5 System verification | N | 0 | No verification performed (GAP-31) | G4 | G5 |
| SWE.1 to SWE.4 Software requirements, architecture, detailed design and units, unit verification | N | 0 | The software is upstream and not forked (GAP-16, DQ-007 answered A, ACT-004 open); no tests or static analysis (GAP-21) | G3 | G4 |
| SWE.5, SWE.6 Software integration and software verification | N | 0 | As above | G4 | G5 |
| HWE.1 Hardware requirements analysis | P | 0 | Part requirements for the bench chain in WP-H-02 §4; WP-H-01 Skeleton | G3 | — |
| HWE.2 Hardware design | P | 0 | WP-H-02 bench chain designed (Draft), not built | G3 | — |
| HWE.3, HWE.4 Hardware verification | N | 0 | Nothing built; WP-H-02 §9 bench checks not run | G4 | — |
| VAL.1 Validation | N | 0 | No validation performed (GAP-31); the WP-V-07 procedure is Draft | G4 | G5 |
| MLE.1 to MLE.4 Machine learning requirements, architecture, training, testing | N | 0 | The learned policies are upstream and unclamped (GAP-24); WP-C-09 and WP-W-10 Skeleton | MLE.1 at G1; MLE.2–4 at G3 | — |
| ACQ.4 Supplier monitoring | N | 0 | No interface agreement or monitoring of upstream or the actuator makers (WP-M-01 T-08) | G1 | — |
| SUP.11 Machine learning data management | N | 0 | No datasets under the fork's control | G3 | — |

**Result at 2026-11-01:** every process in scope is at CL0. The management and support processes have partly
performed outcomes because the record itself is planned and version-controlled; the engineering processes have not
started on anything the fork controls. The "CL1 by" and "CL2 by" columns are this document's proposed path to the
T-12 targets; a dash means T-12 sets CL1 as the end target.

## 4. Improvement plan

| Gap | What closes it | Owned by | Gate |
|---|---|---|---|
| MAN.3: no schedule, effort or monitoring | Dates and effort estimates in [WP-M-03](WP-M-03-project-plan.md) (its OI-1, OI-2); progress tracked per WP-M-02 §10; the G0 review held | Project maintainer | G0 |
| MAN.5: risks not monitored | The register of [WP-M-07](WP-M-07-risk-management.md) reviewed at each gate review | Project maintainer | G0 |
| SUP.1: no QA | A QA role holder independent of the author; the gate QA checks of WP-M-05 §2.1 performed and recorded | Project maintainer | G1 |
| SUP.8: no tagged baseline, software unpinned | Forks created and pinned (ACT-004); a tagged baseline under [WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md) | Configuration and change manager | G0 (forks), G1 (tag) |
| SUP.9, SUP.10: procedures not yet exercised | [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md) and [WP-P-02](../07-supporting/WP-P-02-change-management.md) written; the bench chain fitted as the first impact-analysed change (WP-M-02 §4.1) | Configuration and change manager | G0 (procedures), G1 (first records) |
| SYS.1 to SYS.3 | The concept and system design work products of WP-M-02 §4 approved after review | Safety manager | G1, G2 |
| SYS.4, SYS.5, VAL.1 | The bench campaign of P4 and validation of P5 | Safety-related control system engineer | G4, G5 |
| SWE.1 to SWE.6 | The dedicated controller and the forked host software developed under the software work products (WP-W-01…W-08) | Firmware and software engineer | G3, G4 |
| HWE.1 to HWE.4 | WP-H-01 written; the chain built and checked per WP-H-02 §9 and WP-H-06 | Electrical and mechanical engineer | G3, G4 |
| MLE.1 to MLE.4, SUP.11 | [WP-M-09](WP-M-09-ml-safety-plan.md), WP-C-09 and WP-W-10 | ML safety lead | G1, G3 |
| ACQ.4 | WP-M-10 written and its monitoring of upstream merges performed | Project maintainer | G1 |
| Any CL2 rating | Someone other than the author rates PA 2.1 and 2.2; a self-rating at I0 gives no credit above CL1 | Safety manager | G2 |

This baseline is repeated at every gate review from G1, with the date and commit of the evidence.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Check the process IDs and names against PAM 4.0, including whether SUP.2 and SUP.7 (named in the register for WP-P-05 and WP-P-04) exist in 4.0, and correct the register's ASPICE column if not | Safety manager | G1 |
| OI-2 | Have a person other than the author repeat the ratings of §3 | Safety manager | G1 |
| OI-3 | Repeat the self-assessment at the G0 gate review against the commit of that review | Safety manager | G0 |
