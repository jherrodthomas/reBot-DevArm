# Contributor guide

Contributions are welcome in machinery safety, safety-related control systems, electrical and mechanical
engineering, embedded and ROS 2 software, robot learning, cybersecurity, verification, documentation and review.
This page is the short version of [contributing](../CONTRIBUTING.md), which is the rule book.

![What a change goes through before it is merged: a pull request against main is classified by the paths it touches, must carry rationale, impact analysis, verification and record updates when safety-relevant, is checked by the workflows, and is reviewed and merged by a person.](change-path.svg)

*Rendered from the [safety-relevant file list](../assurance/07-supporting/safety-relevant-paths.txt) and the [workflow files](../.github/workflows) by [`infographics.py`](../tools/wiki/infographics.py) at every wiki sync.*

## Setting up

This repository is the record; only Python 3 is needed (PyYAML for the decision register).

```sh
git clone https://github.com/jherrodthomas/reBot-DevArm.git
cd reBot-DevArm
python3 assurance/01-management/decisions/check_decisions.py     # the questions for the lead
python3 assurance/tools/folder_index.py --check                  # folder indexes match the register
python3 assurance/process/tools/process_model.py --check         # process maps and gate skeletons current
python3 docs/assets/rebot/make_assets.py --check                 # README figures match their generator
python3 assurance/tools/check_links.py                           # every relative link resolves
python3 assurance/tools/check_tables.py                          # every table row matches its header
python3 tools/wiki/build_wiki.py                                 # these pages check clean
```

Changes to the software that moves the arm go to the forked SDK and driver repositories once they exist (DQ-007);
the tests they need are described in [WP-W-01](../assurance/05-software/WP-W-01-software-development-environment-guidelines.md).
Until then the software is upstream's and is not changed here.

## Branches and pull requests

- Branch from `main` and open the pull request against `main`. The pull request template asks for a
  safety-impact statement; "none" is a valid answer with a reason.
- Questions and bugs go to the [issues](https://github.com/jherrodthomas/reBot-DevArm/issues) with the
  problem report or safety concern template. A review of an analysis is as valuable as code.
- Decisions for the project lead are not issues; they go into the [decision register](How-decisions-are-made.md).

## Is my change safety-relevant?

A change is safety-relevant if it touches a path on the
[safety-relevant file list](../assurance/07-supporting/safety-relevant-paths.txt) or changes an assurance work
product. The list has three classes:

| Class | What it covers | Examples |
|---|---|---|
| `SR-A` | Safety-related parts of the control system | The chain design files, the controller safety layer, the safety parameter sets (joint limits, torque and speed caps, watchdog timings) |
| `SR-Q` | Functional layers that feed hazards or configure limits | The forked SDK and ROS 2 driver, the policy runtime integration, upstream's hardware record under `hardware/` |
| `SR-T` | Build, test, CI, toolchain or dependency configuration that changes evidence or binaries | Workflows, package pins, the generators and checkers |

Anything not matched is not safety-relevant and takes the standard route. The list is owned by
[WP-P-01](../assurance/07-supporting/WP-P-01-configuration-management-plan.md) and changes only through a change
request.

## What a safety-relevant pull request must include

1. **Rationale.** What the change does and why.
2. **Impact analysis.** Which hazards, safety functions, requirements and assumptions it affects, following
   [WP-M-11](../assurance/01-management/WP-M-11-impact-analysis.md) and
   [WP-P-02](../assurance/07-supporting/WP-P-02-change-management.md), recorded under
   [`07-supporting/impact/`](../assurance/07-supporting/impact/README.md). "No assurance object affected" is a valid
   result, with a reason.
3. **Verification.** The tests or analyses that show the change is correct, and their results.
4. **Record updates.** The affected work products, with every generator re-run.

## What can and cannot change a review state

- A work product leaves `Draft` only through a verification review by someone other than its author
  ([WP-P-05](../assurance/07-supporting/WP-P-05-verification-review-procedure.md)); a claim is accepted only through a
  confirmation measure at the independence [WP-M-06](../assurance/01-management/WP-M-06-confirmation-measures-plan.md)
  requires.
- A passing CI run, a passing test or an existing file does not accept anything. It can be evidence that a
  reviewer accepts.
- An AI-generated review is not a substitute for the required independent confirmation.
- Never edit generated files (process maps, gate skeletons, folder READMEs, README figures) by hand. Change the
  source and regenerate.

## Upstream content

`hardware/` is Seeed Studio's record and is never edited here; it changes only by merging from upstream, with an
impact analysis under [WP-M-10](../assurance/01-management/WP-M-10-upstream-and-supplier-management.md). The
concept-phase package files at the repository root (`reBot_DevArm_*`) are an input to the record and are not
edited either. Upstream's licence is CC BY-NC-SA 4.0: contributions stay non-commercial, keep the notices, and must
not imply Seeed Studio's endorsement.

## Working with Claude sessions

Much of the drafting is done in Claude Code sessions under the project lead's direction. The rules those sessions
follow are in [CLAUDE.md](../CLAUDE.md): sort questions before asking, keep every question self-contained, ask in
batches of ten, and record decisions in the [register](How-decisions-are-made.md). A session's pull request is
reviewed like any other. The [session log](Session-log.md) lists what has been merged.

## Where to get help

- [Issues](https://github.com/jherrodthomas/reBot-DevArm/issues) for anything about the project.
- Security problems go through [SECURITY.md](../SECURITY.md), never a public issue. See
  [reporting a safety concern](Reporting-a-safety-concern.md).
