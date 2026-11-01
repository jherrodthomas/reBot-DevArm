# WP-M-04 Organization-specific rules, safety culture, competence management

| Field | Value |
|---|---|
| Work product | WP-M-04 Organization-specific rules, safety culture, competence management |
| Standard reference | SRP/CS: 61508-1 §6.2 (competence); 13849-1 §4; IEC 62443: 62443-4-1 SM-4. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: approval rules today and with a second person, competence per role, safety culture, operator training record; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

The rules of the organisation that produces the reBot-DevArm record: who may approve what, how competence is shown
for each role of [WP-M-02 §3.1](WP-M-02-safety-plan.md#31-role-assignments), how a safety concern is raised and what
happens then, and how AI-assisted authoring is bounded ([WP-M-02 §3.3](WP-M-02-safety-plan.md#33-ai-assisted-authoring)).

The organisation today is one person, Jherrod Thomas, who holds every assigned role, with drafting done in Claude
Code sessions under his direction. The rules below are written for that and say what changes when a second person
joins.

## 2. Organisation rules

### 2.1 How work enters the record

| Rule | Where it is set | State in the repository |
|---|---|---|
| Every change goes by pull request into `main` | [CONTRIBUTING.md](../../CONTRIBUTING.md) | In use: pull requests #1 to #8 |
| Every pull request answers the safety-impact statement: class (`SR-A`, `SR-Q`, `SR-T`, `NSR`), affected items, impact record, verification | [Pull request template](../../.github/PULL_REQUEST_TEMPLATE.md); [safety-relevant file list](../07-supporting/safety-relevant-paths.txt) | Template in place |
| CI runs the `assurance` and `wiki` workflows on every pull request; a stale generated file fails it | [`assurance.yaml`](../../.github/workflows/assurance.yaml), [`wiki.yaml`](../../.github/workflows/wiki.yaml) | In place |
| A passing CI run accepts nothing; it can be evidence a reviewer accepts | CONTRIBUTING.md | Rule |
| Questions for the lead go into the decision register, not issues | [Decision register](decisions/README.md) | In use: DQ-001…DQ-020 |
| Generated files are never edited by hand | [CLAUDE.md](../../CLAUDE.md) | Checked by CI |
| Branch protection on `main` (CI required, review required) and a CODEOWNERS file | — | Not recorded: no `CODEOWNERS` file exists, and branch protection is a GitHub setting the repository does not show (OI-1) |

### 2.2 Who may approve what

| Act | Today (one person) | Once a second person is a member |
|---|---|---|
| Approve a work product (Draft → Approved) | The safety manager, recorded as self-approval at I0 in the Approver field (DQ-010, answered A) | A verification review by someone other than the author ([WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md)), then the safety manager's approval |
| Merge a pull request on an `SR-A` path | The maintainer, at I0; no such path has content yet | Two human approvals, neither by the author; no self-merge |
| Merge a pull request on an `SR-Q` or `SR-T` path, or on a work product | The maintainer, at I0 | One approval by someone other than the author |
| Accept a claim in the safety case | Nobody: only a confirmation review at the independence of [WP-M-06](WP-M-06-confirmation-measures-plan.md) accepts a claim, and none can be performed (DQ-009, answered A) | Unchanged until an assessor is engaged |
| Answer a decision in the register | The project lead; `decider: claude` entries are assumed and the lead may change them | Unchanged |
| Lift a test stop after a safety anomaly | The safety manager, in writing ([WP-V-07 §6](../06-validation/WP-V-07-test-operations.md#6-anomalies)) | Unchanged; the operator involved may not lift it alone |
| Gate go/no-go | The safety manager chairs; the project lead decides | Unchanged; an assessor is informed where engaged |

### 2.3 AI-assisted authoring

The rules of WP-M-02 §3.3 apply. In addition:

- The assistant holds no role in WP-M-02 §3.1 and its competence is not claimed. Its output is the committer's work at
  I0.
- A session follows [CLAUDE.md](../../CLAUDE.md): it marks every clause reference as to be checked, never claims that
  an activity was performed, reviewed or measured unless the repository shows it, and asks the lead only what the
  lead alone can decide.
- An AI-generated review, checklist or audit is an author-side pre-review. It is never recorded as a verification
  review, a QA audit or a confirmation measure.

## 3. Competence

Per role: the knowledge it needs and the evidence kept. Evidence is a short entry in the training and competence
record (§5): courses, certificates, prior work, or supervised practice on this record. **No competence evidence is
recorded for any role yet** (OI-2).

| Role (WP-M-02 §3.1) | Knowledge needed | Evidence kept |
|---|---|---|
| Safety manager | ISO 12100 risk assessment; ISO 10218-1/-2 and ISO/TS 15066 robot safety; ISO 13849-1/-2 at the level of reading a PL argument; IEC 61508-1 management concepts; the record's own process (WP-M-01, WP-M-02, WP-M-06) | Training or prior safety-management work; gate reviews chaired |
| Project maintainer | The fork's scope and licence; GitHub workflow; the decision register | None beyond holding the repository |
| Configuration and change manager | Git, baselines and tags, the safety-relevant file list, impact analysis (WP-P-01, WP-P-02, WP-M-11) | Baselines and impact records produced |
| Cybersecurity manager | IEC 62443-4-1 practices, IEC 62443-4-2 component requirements, CAN bus and ROS 2 attack surface | Training or prior security work |
| ML safety lead | ISO/IEC TR 5469 classes and usage levels; LeRobot policies; the AI Act's high-risk trigger | Training or prior ML work |
| Safety-related control system engineer | ISO 13849-1 categories, MTTFD, DCavg, CCF; ISO 13849-2 fault lists; safety relays and contactors; SISTEMA or equivalent | Training; a PL calculation reviewed by a competent person |
| Electrical and mechanical engineer | EN 60204-1 (disconnect, overcurrent, protective bonding); 24 V DC distribution; ISO 13854 gaps; fixing and strength of printed parts | Qualification in electrical work; the WP-H-02 wiring checked under its §9 |
| Firmware and software engineer | Embedded C or Rust on the dedicated controller (DQ-020); CAN-bus motor control; the Damiao (and later RobStride) actuator protocols; the `motorbridge` SDK and the ROS 2 driver; IEC 61508-3 techniques for the safety layer | Code reviewed in the forks; tests written |
| Verification reviewer | The work product's subject; WP-P-05; independence from the author | Declared in each review record |
| Quality assurance | [WP-M-05](WP-M-05-quality-assurance-plan.md); audit practice; independence from the author | Declared in each audit record |
| Test bench owner, test operator | [WP-V-07](../06-validation/WP-V-07-test-operations.md) in full; the bench chain's behaviour; the arm's modes and limits | Training record (§5) before any powered test |
| External assessor | As [WP-M-06 §6.1](WP-M-06-confirmation-measures-plan.md#61-assessor-qualification-and-independence) sets: machinery functional safety (ISO 13849-1, ISO 10218-1/-2, ISO/TS 15066, EN 60204-1) with evidence | Declared in each report |

Where the one person holds a role without recorded evidence, the work product stays Draft or is self-approved at I0
and the gap is visible in its header; nothing in this table lowers a requirement of WP-M-06.

## 4. Safety culture

| Principle | What it means on this project |
|---|---|
| A concern stops the test | Anyone at the bench may press the E-stop at any time without asking. A safety anomaly stops testing until the safety manager lifts the stop in writing (WP-M-02 §9; WP-V-07 §6) |
| Nobody is blamed for a stop | An E-stop press, a failed pre-session check or a report that turns out unfounded is recorded as data, never held against the person who made it |
| Near misses are recorded | A near miss, a hazard the analyses may miss, or contact in operation is raised with the [safety concern form](../../.github/ISSUE_TEMPLATE/safety_concern.yml); an anomaly during testing with the [problem report form](../../.github/ISSUE_TEMPLATE/problem_report.yml), whose safety boxes make it a safety anomaly triaged within one working day |
| Security problems are reported privately | Through GitHub private vulnerability reporting, per [SECURITY.md](../../SECURITY.md) |
| Limitations stay visible | The record states what it cannot claim: Draft status, I0 self-approval, unperformed confirmation measures, unchecked clause references. A schedule never removes a hold point |
| The lead is both project and safety authority | A recorded conflict of interest while one person holds both. Bounded by the hold points written in advance (WP-M-01 §7), decisions recorded with their options and recommendation, and the assessor revisit at G1 (DQ-009) |

## 5. Training record

Operators are trained on WP-V-07 before any powered test. The training covers: the conditions C-1 to C-8 and the
limits of WP-V-07 §2 and §3; where the pendant and bench E-stops are and what they switch; the pre-session checks of
WP-V-07 §4 done once under supervision; the test log; what counts as an anomaly and how it is raised. An observer is
briefed on the E-stop and the bench area before each session.

While the lead is the only person, he trains himself from the procedure; that is recorded as self-training at I0.

| Person | Role | Training or competence item | Date | Trainer or source | Evidence |
|---|---|---|---|---|---|
| — | — | No entry yet: no one has been trained and no powered test has been run under the fork | — | — | — |

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Record the branch protection of `main` (required CI checks, required review) and add a CODEOWNERS file for `assurance/` and the `SR-A` paths; until a second person exists, record that review cannot be required | Configuration and change manager | G0 |
| OI-2 | Enter the competence evidence of the role holder for each role he holds in §5, or mark the role as held without evidence | Safety manager | G0 |
| OI-3 | Train and record the first test operator per §5 before the first powered test (WP-V-07 OI-2, WP-M-02 OI-6) | Project maintainer | Before the first powered test |
| OI-4 | Define the competence a second contributor must show to act as verification reviewer at I1 for each work product area | Safety manager | G1 |
