# WP-M-05 Quality management and quality assurance plan

| Field | Value |
|---|---|
| Work product | WP-M-05 Quality management and quality assurance plan |
| Standard reference | SRP/CS: 61508-1 §6.2; IEC 62443: 62443-4-1 SM-5; Other: ISO 9001 (informative); ASPICE: SUP.1. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: QA independence, gate QA checks and the two audits, review records, nonconformance and corrective action, kit assembly; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

The quality assurance plan for the reBot-DevArm record: how the process and the work products are checked by
someone independent of their author, and the subset of ISO 9001 the concept-phase package found missing (design
review records, nonconformance and corrective action: GAP-32, package GAP-9001-01, -02, -04, -05). No ISO 9001
certification is sought ([WP-M-00 §5](WP-M-00-work-product-register.md#5-not-applicable)).

**QA is not performed today.** The QA role in [WP-M-02 §3.1](WP-M-02-safety-plan.md#31-role-assignments) is TBD and
must be independent of the author. While one person writes everything (DQ-010), no QA check or audit in this plan can
be performed; they are planned, not held. What exists meanwhile is the automated checking of §2.3, which supports QA
and replaces none of it.

## 2. Audit plan

### 2.1 Process QA at each gate

Before each gate review the QA role checks a sample of the phase's work against this plan. The result is a QA finding
list, an input to the gate review ([WP-M-02 §10](WP-M-02-safety-plan.md#10-progress-tracking-and-gate-reviews)).

| Check | Sample | Pass when |
|---|---|---|
| Status discipline | Every work product of the gate | No status past Draft without a review record (§3) |
| Safety-impact statements | Every merged pull request of the phase touching an `SR-A` or `SR-Q` path, and five others | The statement is answered; an impact record exists under [`07-supporting/impact/`](../07-supporting/impact/README.md) where the class needs one |
| Document-control headers | Every work product changed in the phase | The fields of the [assurance README](../README.md#document-control-header) are present and current |
| Open items | Every work product of the gate | Each open item has an owner and a due gate; none due at this gate is left without a decision |
| Decisions applied | Every register entry answered in the phase | `applied` names where it was applied, or the entry says why not yet |
| Problems and corrective actions | Every issue labelled `safety-anomaly`, `problem` or `confirmation-finding` opened in the phase | Triaged; closed ones have a verified corrective action (§4) |

### 2.2 Functional safety audits

| Audit | Gate | Samples | Independence |
|---|---|---|---|
| AUD-1 | G2 | Configuration management across this repository and the software forks (baselines, pins, the safety-relevant file list); three changes traced from request through impact analysis to merge; review records of the G1 work products; the decision register as the record of risk acceptance | I3 ([WP-M-06 §5](WP-M-06-confirmation-measures-plan.md#5-functional-safety-audit)) |
| AUD-2 | G4 | The bench campaign: test logs against WP-V-07; three test records traced to their requirement; problem resolution of every safety anomaly; the tools in use against their WP-P-07 classification | I3 |

Both are unscheduled while no assessor is engaged (DQ-009, answered A).

### 2.3 Automated checks that support QA

CI runs these on every pull request ([`assurance.yaml`](../../.github/workflows/assurance.yaml),
[`wiki.yaml`](../../.github/workflows/wiki.yaml)). A pass is evidence a reviewer may use; it accepts nothing.

| Check | What it shows |
|---|---|
| Case records valid, dashboard current | The Living Safety Case records are consistent and no claim is shown accepted without a review |
| Decision register | Entries follow the lifecycle; the inbox page builds |
| Folder indexes | Every registered work product exists and the indexes match WP-M-00 |
| Process model, maps, gate skeletons, swimlane figures | The model agrees with WP-M-00, WP-M-02 and WP-M-06; generated files are current |
| Links and tables | Relative links resolve; every table row has the header's cell count |
| Figures, banner, scene catalogue, wiki build | Generated pictures are current; the wiki builds |

## 3. Design review records

Every verification review leaves a record, per [WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md):
the pull request review itself, and an entry in the case's review records (`assurance/case/reviews/reviews.yaml`)
with the reviewed object, reviewer, independence, date, outcome and baseline. Self-approval at I0 is recorded the
same way, marked I0. Gate reviews are recorded under [`10-safety-case/gates/`](../10-safety-case/gates/README.md),
confirmation measures under [`10-safety-case/confirmation/`](../10-safety-case/confirmation/README.md).

At this version the review records file holds no record, no gate review has been held and no confirmation record
exists. This section closes the design-review part of GAP-32 once the first records exist and AUD-1 has sampled them.

## 4. Nonconformance and corrective action

| Source | Raised as | Handled under |
|---|---|---|
| Defect, test finding, finding against a work product | Issue from the problem report form, labelled `problem` | [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md) |
| Safety anomaly during testing | The same form with a safety box ticked; labelled `safety-anomaly` at triage, within one working day | WP-P-03; [WP-M-02 §9](WP-M-02-safety-plan.md#9-safety-anomaly-handling) |
| Hazard missed, near miss, event in operation | Safety concern form, labelled `safety-concern` | WP-P-03; [WP-O-04](../09-production-operation/WP-O-04-field-monitoring.md) |
| Confirmation finding | Issue labelled `confirmation-finding` | WP-P-03; WP-M-06 §10 |
| Process nonconformance (for example a status moved past Draft without a record, a generated file edited by hand, a missing impact record) | Issue labelled `problem`, naming the rule broken | WP-P-03 |

A corrective action records the cause, the change that removes it, the verification that the change worked, and who
closed it. For a safety anomaly the closer is not the analyst. Actions that the safety case depends on are also
tracked as assurance actions in `assurance/case/actions/` (ACT-001…ACT-010 at this version). No nonconformance has
been raised at this version.

## 5. Kit assembly

The arm is a kit upstream sells, also sold pre-assembled; the fork manufactures nothing (WP-M-01 T-07). Kit assembly
has no production controls today (GAP-33).

| The fork can control | The fork cannot control |
|---|---|
| The assembly checks, installation and commissioning tests it publishes ([WP-O-01](../09-production-operation/WP-O-01-assembly-installation-commissioning.md), due G5): fastener torque, harness termination, cover gaps, fixing, the E-stop test | How a builder follows them, or whether they do |
| The inspection and assembly record of the arm on its own bench, kept in the change record before the first powered test, and the pre-session checks of [WP-V-07 §4](../06-validation/WP-V-07-test-operations.md#4-pre-session-and-per-session-checks) | Upstream's part changes and the 3D-printed substitutes upstream allows for machined parts (GAP-04) |
| Which configuration it claims for (CFG-001) and the commissioning tests a build must pass before that claim applies to it | The quality of the actuators, the adapter and the supply from their makers ([WP-M-10](WP-M-10-upstream-and-supplier-management.md)) |

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Fill the QA role with a person independent of the author (WP-M-02 OI-1); until then no QA check of §2.1 can be performed | Project maintainer | G0 |
| OI-2 | Create the labels `safety-anomaly`, `problem`, `safety-concern`, `confirmation-finding` and `triage` on GitHub if missing, and record that they exist | Configuration and change manager | G0 |
| OI-3 | Add a review-record template to WP-P-05 matching the fields of `reviews.yaml` | Safety manager | G0 |
| OI-4 | Write the bench arm's inspection and assembly checklist (from the WP-O-01 seed) before the first powered test | Electrical and mechanical engineer | G1 |
| OI-5 | Schedule AUD-1 and AUD-2 once an assessor or an auditor of equivalent independence is engaged (DQ-009 revisit) | Safety manager | G1 |
