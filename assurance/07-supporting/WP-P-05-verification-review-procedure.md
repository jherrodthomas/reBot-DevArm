# WP-P-05 Verification and review procedure

| Field | Value |
|---|---|
| Work product | WP-P-05 Verification and review procedure |
| Standard reference | SRP/CS: 13849-1 §8; 61508-1 §7.18; IEC 62443: 62443-4-1 SVV-1; ASPICE: SUP.2. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: review types, recording reviews at I0 under DQ-010, entry and exit criteria, checklists, record template; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How a work product or a code change is reviewed before it leaves Draft or is merged: the review types, the
independence each needs, how reviews are recorded while the project has one person, the entry and exit criteria, the
checklists, and the record template. Confirmation measures (CR, AUD, FSA) are planned in
[WP-M-06](../01-management/WP-M-06-confirmation-measures-plan.md); they use the template of §6.

No verification review above I0 has been performed, and no review record exists in
[`case/reviews/reviews.yaml`](../case/reviews/reviews.yaml).

## 2. Review types

| Type | What it checks | Method | Credit |
|---|---|---|---|
| Self-review | The author's own check against the entry criteria and the checklist | Read-through, checks run, record on the pull request | I0 |
| Verification review | The work product against its inputs, its requirements and its checklist; the code against its requirements and tests | Pull request review with the §5 checklist | The reviewer's level (§3) |
| Walkthrough | Early direction of a draft, with the author presenting | Meeting or recorded call; findings written on the pull request | As the reviewer's level; does not move status on its own |
| Inspection | Line by line against a checklist, findings logged one by one | Pull request review with a findings table | The reviewer's level; required for SR-A changes and for the PL calculation (WP-H-04) |
| AI pre-review | Anything an AI assistant runs on the author's side (audits, checklist runs) | Input to the author | I0 at most, never above ([WP-M-02 §3.3](../01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)) |
| CI checks | Links, tables, records, register, generated files | The `assurance` and `wiki` workflows | None: evidence a reviewer may use, never a review |

## 3. Independence levels

The levels are those of [WP-M-06 §3](../01-management/WP-M-06-confirmation-measures-plan.md#3-independence-levels):
I0 the author may do it; I1 a person other than the author; I2 a person independent of the team; I3 a person
independent of the organisation. The person who commits an AI-drafted change is its author, so a lead who reviews a
Claude session's pull request is doing a self-review at I0. The target for a work product to leave Draft is I1
(WP-M-01 T-09); confirmation measures need I2 or I3 as WP-M-06 sets.

### 3.1 How reviews are recorded today (DQ-010)

The project has one person. The lead decided on 2026-11-01 (DQ-010, answered A) that the safety manager may approve
work they authored, recorded as self-approval at I0, and that no review above I0 and no confirmation measure exists
until a second person or an assessor joins. So, for now:

1. Every change is a pull request into `main`, with CI passing.
2. GitHub does not let an author approve their own pull request, so the self-review is a pull request comment that
   starts with **"Self-review at I0 — not an independent review"** and follows the §6 template.
3. A work product may move to Approved on that basis only by the safety manager, and its header then reads
   Reviewer(s) `<name> (self-review, I0)` and Approver `Safety manager (self-approval at I0, DQ-010)`.
4. A Claude session never approves or merges its own pull request; its drafts carry
   `Assurance team (AI-assisted draft, I0)` as author.
5. Self-reviews are not entered in `case/reviews/reviews.yaml`. The validator's acceptance rule (V6) does not look
   at independence, so an I0 entry would show claims as accepted on the dashboard (OI-3).
6. A gate review that relies on I0 approvals lists them in its record ([gate records](../10-safety-case/gates/README.md)).

[CONTRIBUTING.md](../../CONTRIBUTING.md) states the same rule.

### 3.2 When a second reviewer joins

- The second person reviews with GitHub's **Approve**, which records name and date; their review is I1 for work
  they did not author. Branch protection then requires one approval on `main`, two on SR-A paths, and a CODEOWNERS
  file routes `assurance/` and the SR-A paths to them ([WP-P-01](WP-P-01-configuration-management-plan.md) OI-6).
- Work products approved at I0 are re-reviewed at I1, those the next gate needs first; the header's Reviewer(s) field
  is updated and the I0 approval stays visible in the history.
- I1 reviews that accept a claim, an evidence item or a configuration are entered in `case/reviews/reviews.yaml`
  with their independence.
- When an assessor is engaged (DQ-009, revisited at G1), the I2 and I3 measures of WP-M-06 become schedulable.

## 4. Entry and exit criteria

**Entry.** The document-control header is complete ([WP-P-04 §2.1](WP-P-04-documentation-management.md#21-header)); the
content has no Skeleton note; inputs and sources are named; every clause reference is marked to be checked; the open
items table lists what is missing; generated files are regenerated; the pull request carries its class and
safety-impact statement ([WP-P-02](WP-P-02-change-management.md)); CI passes.

**Exit.** Every finding has a disposition: fixed, rejected with a reason, or moved to an open item or an issue. Major
findings (a wrong or unsupported claim, wrong safety content, missing required content) are fixed and re-checked
before exit. The outcome is recorded as `accepted`, `changes-requested` or `rejected`, the vocabulary of the case
records. CI passes on the final commit.

## 5. Checklists

| Family | Checks beyond the entry criteria |
|---|---|
| All | Says only what the record shows; no compliance claim; identifiers resolve and are not reused; links point to the right section |
| Plans and procedures (WP-M, WP-P) | Roles named or TBD with a gate; procedure matches what the repository does (CI, templates, folders); decisions cited by their register entries |
| Concept and analyses (WP-C, WP-A) | Every hazard per envelope rated with its inputs; package identifiers kept; gaps restated as GAP-nn; assumptions listed as AOU |
| Requirements and architecture (WP-S, WP-H-01, WP-W-02, WP-W-03) | Per [WP-P-06 §2](WP-P-06-requirements-management-traceability.md#2-identifiers-and-attributes): one testable statement each, allocated, traced up and down |
| Hardware and PL calculation (WP-H) | Parts with certificates or the fault exclusions argued; category, MTTFD, DCavg, CCF inputs sourced; units and margins |
| Software and forks (WP-W, fork code) | Requirement per change; tests added and run; no safety function on the host or a learned component (WP-M-01 T-03, T-04) |
| Verification and validation (WP-V) | Procedure, pass criteria, configuration and baseline stated; results raw and reproducible; WP-V-07 hold point respected |
| Tools (SR-T) | The tool's tests pass; the change to its output is shown; generated files regenerated |

## 6. Review record template

Used on the pull request for verification reviews, and as a file under
[`10-safety-case/confirmation/`](../10-safety-case/confirmation/README.md) for confirmation, audit and assessment.

```markdown
| Field | Value |
|---|---|
| Review ID | REV-nnn (when entered in case/reviews), else the pull request number |
| Type | self-review / verification / walkthrough / inspection / confirmation / audit / assessment |
| Object | WP-x-nn v<version>, or PR #n at commit <SHA> |
| Baseline | BL-nnn (<SHA>) |
| Reviewer | Name |
| Independence | I0 / I1 / I2 / I3, with one sentence on why (e.g. "author of the work product") |
| Date | YYYY-MM-DD |
| Method and checklist | Type and the WP-P-05 §5 rows used |
| Outcome | accepted / changes-requested / rejected |

| # | Location | Finding | Severity (major, minor, editorial) | Disposition |
|---|---|---|---|---|
```

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Name at least one verification reviewer other than the author (WP-M-02 OI-1) | Project maintainer | G0 |
| OI-2 | Branch protection and CODEOWNERS as in §3.2 | Configuration and change manager | When the second reviewer joins |
| OI-3 | Make the validator's acceptance rule require the independence WP-M-06 sets, so an I0 review can be recorded without accepting a claim | Safety manager | G1 |
| OI-4 | Bring WP-M-02 OI-1 in line with DQ-010 and §3.1 (CONTRIBUTING.md is done) | Safety manager | G0 |
| OI-5 | Expand the §5 rows into one checklist per work product family as each family reaches review | Safety manager | G1 |
