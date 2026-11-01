# WP-P-02 Change management plan

| Field | Value |
|---|---|
| Work product | WP-P-02 Change management plan |
| Standard reference | SRP/CS: 61508-1 §7.16; IEC 62443: 62443-4-1 SM-3; ASPICE: SUP.10. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: change classes, the pull-request procedure, impact records; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How a change to anything under configuration control ([WP-P-01 §2](WP-P-01-configuration-management-plan.md#2-configuration-items))
is requested, classified against the safety-relevant file list, impact-analysed, verified, reviewed and merged, and
which records it leaves. It applies to this repository and, once they exist, to the software forks.

Every change is a pull request into `main`. CI runs on every pull request (the `assurance` and `wiki` workflows in
[`.github/workflows/`](../../.github/workflows/assurance.yaml)), and pull requests are merged with a merge commit, so
each change appears in the history as `Merge pull request #n`. The change board is the configuration and change manager
with the safety manager; today both are Jherrod Thomas, acting ([WP-M-02 §3.1](../01-management/WP-M-02-safety-plan.md#31-role-assignments)).

A question only the lead can answer (risk acceptance, PL, behaviour defaults, envelope limits, money, the assessor,
roles and independence, gate go/no-go) is not settled inside a change: it goes into the
[decision register](../01-management/decisions/README.md), and the change waits for the answer.

## 2. Change classes

The class of a change is the highest class of any file it touches, using the longest-match rule of
[`safety-relevant-paths.txt`](safety-relevant-paths.txt) ([WP-P-01 §3](WP-P-01-configuration-management-plan.md#3-safety-relevant-file-list)).

| Class | Typical change | Impact analysis | Verification | Review |
|---|---|---|---|---|
| SR-A | Safety-chain design, controller safety layer, safety parameters | Record under [`impact/`](impact/README.md) | Tests or analyses named in the record, with results | Two human approvals per the list; cannot be met today (WP-P-01 OI-7) |
| SR-Q | Forked SDK or driver, upstream merge into `hardware/` | Record under `impact/` | Tests or analyses named in the record; CI | One review per [WP-P-05](WP-P-05-verification-review-procedure.md) |
| SR-T | CI workflows, generators, checkers, dependency pins | Statement in the pull request; a record if a pin or a check that evidence relies on changes | CI, including the changed tool's own tests | One review per WP-P-05 |
| NSR | Work product text, wiki, figures' sources | Statement in the pull request ("none" with a reason is valid) | CI; generators re-run | One review per WP-P-05 |

A change to a work product is NSR by path, but [CONTRIBUTING.md](../../CONTRIBUTING.md) treats it as safety-relevant:
its pull request names the work products touched and the hazards, safety functions, requirements and assumptions it
affects, by identifier. While a work product is Draft, that statement is its impact analysis. Once a work product is
Approved or Baselined, a change to its content also gets a record under `impact/`, because it re-opens a review
and possibly a confirmation measure ([WP-M-06 §4.2](../01-management/WP-M-06-confirmation-measures-plan.md#42-procedure) step 6).

The pull request template, `impact/README.md` and CONTRIBUTING.md do not yet agree on when a separate record is
needed (template: SR-A and SR-Q; impact README: SR-A, SR-Q and SR-T; CONTRIBUTING: every safety-relevant change). This
section is the rule proposed here; the other three are to be aligned with it (OI-1).

## 3. Procedure

| Step | Who | What | Record |
|---|---|---|---|
| 1 Request | Anyone | A problem becomes an issue ([WP-P-03](WP-P-03-problem-resolution.md)); a planned change starts as a branch from `main` | Issue, or the pull request itself |
| 2 Classify | Author | Find the class in §2 and state it in the [pull request template](../../.github/PULL_REQUEST_TEMPLATE.md) | Pull request description |
| 3 Analyse impact | Author | Name the hazards (`HZ-`), safety functions (`SF-`), requirements, assumptions (`AOU-`) and work products affected, in the format of [WP-M-11](../01-management/WP-M-11-impact-analysis.md) | Pull request, or `impact/change-<YYYY-MM-DD>-<slug>.md` per §2 |
| 4 Implement | Author | Change the sources; re-run every generator whose input changed; never edit a generated file | Commits on the branch |
| 5 Verify | Author | Run the checks of CONTRIBUTING.md locally; for SR-A and SR-Q, run the tests or analyses the record names | CI run on the pull request; results in the record |
| 6 Review | Reviewer | Review per [WP-P-05](WP-P-05-verification-review-procedure.md); today a self-review at I0, labelled as such | Review record (WP-P-05 §6) on the pull request |
| 7 Merge | Configuration and change manager | Merge with a merge commit only when CI passes and the review outcome is `accepted` | Merge commit |
| 8 Update the record | Author | Add the record to the table in `impact/README.md`; update the register status in [WP-M-00](../01-management/WP-M-00-work-product-register.md), the case records and the decision register's `applied` entry where touched | Same pull request where possible |

Upstream merges follow the same steps: `hardware/` as described in [WP-P-01 §2.1](WP-P-01-configuration-management-plan.md#21-upstream-content-in-this-repository),
and an upstream sync into a software fork as an SR-Q change in that fork, whose record lists the upstream commits taken.
A change merged after a baseline is frozen belongs to the next baseline ([WP-P-01 §4.2](WP-P-01-configuration-management-plan.md#42-cutting-and-freezing-a-baseline)).

A change drafted by a Claude session is the committer's work (WP-M-02 §3.3) and follows the same route; the session
does not merge its own pull request.

## 4. Records

- **The pull request** is the change record: description with the safety-impact statement, the review record, the
  CI run, the merge commit. Pull requests and their reviews are held by GitHub, outside the git history; only the
  merge commit with its number is in the repository (export: [WP-P-04](WP-P-04-documentation-management.md) OI-3).
- **Impact records** under [`impact/`](impact/README.md), one per change that §2 requires, named
  `change-<YYYY-MM-DD>-<slug>.md`. None exists yet: no change to the arm's hardware or software has been made under the
  fork. The first expected are the bench safety chain (DQ-006) and the software forks with their safety layer
  (DQ-007, DQ-020).
- **The git history** of `main`, with merge commits, as the sequence of changes.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Align the pull request template, `impact/README.md` and CONTRIBUTING.md with §2 on when a separate impact record is needed | Configuration and change manager | G0 |
| OI-2 | Add a CI check that classifies a pull request's changed files against `safety-relevant-paths.txt` and fails when the stated class is lower | Configuration and change manager | G1 |
| OI-3 | Bring the pull request template's check list in line with CONTRIBUTING.md (it omits `validate.py`, `generate_dashboard.py --check`, `process_figures.py`, `tour_figures.py`, `banner.py` and the simulation checks) | Configuration and change manager | G0 |
| OI-4 | Branch protection and CODEOWNERS for `main` ([WP-P-01](WP-P-01-configuration-management-plan.md) OI-6) so steps 6 and 7 are enforced, not only described | Configuration and change manager | G0 |
| OI-5 | Write the first impact records: the bench safety chain and the software forks | Safety manager | Before the first powered test with a person in reach; when the forks exist |
| OI-6 | Set how often each software fork is synced with upstream and who reviews the upstream diff ([WP-M-10](../01-management/WP-M-10-upstream-and-supplier-management.md)) | Configuration and change manager | G1 |
