# WP-P-03 Problem resolution management

| Field | Value |
|---|---|
| Work product | WP-P-03 Problem resolution management |
| Standard reference | SRP/CS: 61508-1 §6.2 (anomaly handling); IEC 62443: 62443-4-1 DM-1…DM-6; ASPICE: SUP.9. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: intake routes, classes A to D, root-cause categories, closure rules; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How problems and safety anomalies are raised, classified A to D by worst credible outcome, contained, analysed,
corrected and closed, and who may lift a test stop. It covers defects, test anomalies, findings against work products
and review findings, in this repository and the software forks. Near misses and events in operation enter here and
feed the analyses through [WP-O-04](../09-production-operation/WP-O-04-field-monitoring.md). Vulnerabilities do not:
they are reported privately and handled under [SECURITY.md](../../SECURITY.md) and
[WP-O-05](../09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md), which also carries the
62443-4-1 DM practices. Questions for the lead are not problems; they go to the
[decision register](../01-management/decisions/README.md).

## 2. Intake and triage

| What was found | Route | Labels applied by the template |
|---|---|---|
| A defect, a test anomaly, a finding against a work product | GitHub issue, [Problem report](../../.github/ISSUE_TEMPLATE/problem_report.yml) form | `problem`, `triage` |
| A hazard the analyses may miss, a near miss, contact, injury, damage, an envelope limit that did not hold | GitHub issue, [Safety concern](../../.github/ISSUE_TEMPLATE/safety_concern.yml) form | `safety-concern`, `triage` |
| A security vulnerability | Private advisory per [SECURITY.md](../../SECURITY.md); never a public issue | — |

Blank issues are disabled ([`config.yml`](../../.github/ISSUE_TEMPLATE/config.yml)), so every public report uses one of
the two forms. The problem report requires the configuration (CFG-001, CFG-002, simulation or other) and the baseline:
the commit of this record and the versions of the SDK, driver and policy checkpoint. The wiki's
[Reporting a safety concern](../../wiki/Reporting-a-safety-concern.md) page explains the routes to reporters.

**Safety anomaly.** A report is a safety anomaly if any box of the problem report's safety triage is ticked, if a
safety concern reports contact, injury, damage or a near miss, or if triage finds that it could violate a safety
function, an operating limit or an assumption of the risk assessment ([WP-M-02 §9](../01-management/WP-M-02-safety-plan.md#9-safety-anomaly-handling)).

**Triage.** The safety manager triages a safety anomaly within one working day; other reports within five working
days (a target proposed in this draft). Triage removes `triage`, adds `safety-anomaly` where it applies, sets the class
(§3) as a label `class-A` … `class-D`, and links the work product or repository affected.

**Test stop.** A safety anomaly stops powered testing at once ([WP-V-07 §6](../06-validation/WP-V-07-test-operations.md#6-anomalies)).
Only the safety manager lifts the stop, in writing, as a comment on the issue stating the cause understood and the
containment in place. Lifting the stop does not close the issue.

## 3. Classification

The class rests on the worst credible outcome had the conditions been slightly worse, not on what happened. A near
miss in a scenario that can crush a hand or strike a head is class A.

| Class | Worst credible outcome | Examples |
|---|---|---|
| A | Serious, irreversible injury (S2 in the risk graph of [WP-C-03](../02-concept/WP-C-03-risk-assessment.md)), or a safety function or stop defeated | Uncommanded motion with a person in reach; E-stop late or ineffective; a pre-session chain check that fails |
| B | Slight, reversible injury (S1), significant damage, or an error that would change a hazard rating, a PLr, a safety requirement or a safety parameter | Wrong joint limit in a parameter set; a hazard missing from the risk assessment; a wrong stopping-time figure |
| C | No credible injury; evidence, a non-safety function or a work product is wrong without changing any rating or requirement | A test log that cannot be reproduced; a broken generator; an incorrect cross-reference |
| D | Editorial or convenience | Wording, layout, a slow script |

| Root-cause category | Typically re-opens |
|---|---|
| Hazard or scenario missing from the analyses | WP-C-03, WP-C-06, WP-C-10 |
| Requirement wrong, missing or ambiguous | WP-C-04, WP-S-02, WP-H-01, WP-W-02 |
| Hardware design or component | WP-H-02, WP-H-07 |
| Software design or code (fork or controller) | WP-W-03…WP-W-06 |
| Configuration, pin or parameter | [WP-P-01](WP-P-01-configuration-management-plan.md), WP-W-09 |
| Upstream or supplier element | [WP-M-10](../01-management/WP-M-10-upstream-and-supplier-management.md), WP-P-08 |
| Tool, generator or CI | [WP-P-07](WP-P-07-tool-classification-qualification.md) |
| Procedure not followed or not adequate | The procedure concerned; WP-M-05 |
| Use, instruction or misuse | WP-C-06, WP-O-03 |
| Not reproduced, cause unknown | Stays open as a class of its worst credible outcome |

## 4. Resolution and closure

1. **Containment.** For A and B: testing stopped (§2); the configuration involved is marked not to be powered with a
   person in reach until the stop is lifted; if other people may run the same configuration, a short notice without
   technical detail of any security aspect goes into the issue.
2. **Root cause.** The analyst records the facts, the cause and its category in the issue. For A and B, the analysis
   shows how the cause was reached (a why-chain or a small fault tree) and searches for the same cause elsewhere.
3. **Corrective action.** A pull request under [WP-P-02](WP-P-02-change-management.md), with an impact analysis. For
   A and B the pull request refers to the issue (`Refs #n`), never `Fixes #n`, so the merge does not close it.
4. **Routing to the analyses.** A confirmed finding updates the work product that owns it, using the table of
   [WP-O-04 §3](../09-production-operation/WP-O-04-field-monitoring.md#3-feeding-the-analyses); counter-evidence to a
   claim becomes a defeater in the Living Safety Case.
5. **Verification of effectiveness.** The test or check that showed the problem is repeated on the corrected
   configuration, and the result is recorded in the issue.
6. **Closure.** The closing comment states class, root-cause category, containment, corrective pull request,
   verification result, work products re-opened, and who closed it at which independence. Classes C and D may be
   closed by the analyst. Class A and B are closed only by someone other than the analyst. While the project has one
   person, an A or B issue whose correction is verified is labelled `resolved-pending-independent-closure` and stays
   open; it is listed as an open anomaly in every gate review ([gate records](../10-safety-case/gates/README.md)).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Create the labels this procedure uses (`safety-anomaly`, `class-A` … `class-D`, `resolved-pending-independent-closure`); whether they exist on GitHub is not visible in the repository | Safety manager | G0 |
| OI-2 | Name a second person who can close class A and B issues (WP-M-02 OI-1) | Project maintainer | Before the first powered test with a person in reach |
| OI-3 | Check the five-working-day triage target for reports that are not safety anomalies against the triage times actually recorded, at the first gate review | Safety manager | G0 |
| OI-4 | Add a trend review of closed problems by root-cause category to the QA audits of [WP-M-05](../01-management/WP-M-05-quality-assurance-plan.md) | Quality assurance | G2 |
| OI-5 | Extend the intake to the software forks' issue trackers once the forks exist (templates, labels, link back to this repository) | Configuration and change manager | When the forks exist |
