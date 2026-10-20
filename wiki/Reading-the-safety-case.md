# Reading the safety case

The safety argument is published while it is being built. This page explains what the safety case is today, what
the dashboard shows, and what it does and does not promise.

## Today

The safety case is the document [WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md), with the
machine-readable records in [`assurance/case/`](../assurance/case/README.md). Its claim structure, from
[WP-M-01 §3.2](../assurance/01-management/WP-M-01-assurance-strategy.md#32-top-level-claim):

- **G0** The B601-DM, fixtured on a bench and operated within its limits by a trained operator with nobody else in
  reach (OE-1), poses no unreasonable risk.
- **G1** Every safety function reaches its required Performance Level: the emergency stop, the safe stop on
  watchdog, the manual reset, the joint torque and speed limits, the joint position limits, the heartbeat, the
  contact detection and stop, the gripper holding, the thermal and overcurrent cut-offs, the shared-workspace
  functions.
- **G2** The complementary electrical and mechanical measures are implemented: the supply, the disconnect and
  fusing, the connectors; the joint gaps, the end-stops, the fixing, the printed parts.
- **G3** The command path cannot defeat the safety functions: every motion path is authenticated and bounded, and
  no learned policy carries a safety function.
- **G4** The evidence was produced under a controlled process: a baseline exists, the hazards are complete, and the
  motion-critical software has verification evidence.

No claim has accepted evidence. The known counter-evidence is GAP-01…GAP-36 in the
[gap assessment](../assurance/00-assessment/gap-assessment.md), one defeater each, all open. The concept-phase
package the fork published before this record is evidence at "partial": a drafted analysis nobody has reviewed.

## What the dashboard shows

![Living Safety Case dashboard: assurance state, baseline, claims and how many have accepted evidence, evidence items and how many are accepted, open defeaters, records digest.](../docs/assets/assurance/dashboard.svg)

[`assurance/case/`](../assurance/case/README.md) holds claims, arguments, evidence items, defeaters, actions,
configurations, baselines and reviews as machine-readable records, a validator, and a generator that draws this
dashboard, the lifecycle-area card and a one-line headline on the README: the assurance state, the baseline, the
number of claims and how many have accepted evidence, the evidence items and how many are accepted, the open
defeaters, and a digest of every record. These rules apply:

- A claim counts as accepted only when a recorded review accepts it, every piece of evidence it cites is available
  and accepted, and no defeater against it is open. The validator refuses anything else.
- A passing CI run, a passing test or the existence of a document never accepts a claim on its own, and an
  AI-generated review is not a substitute for independent confirmation.
- Every figure is generated from the records, never typed by hand, and the assurance workflow fails when the
  committed dashboard is out of date.

![Lifecycle areas: safety management, hazard analysis, safety concepts, technical implementation, verification and validation, safety case and review, each with its status derived from the evidence records.](../docs/assets/assurance/lifecycle.svg)

## Why zero accepted is the honest number

Evidence becomes *accepted* only after a confirmation review by someone independent of the author
([WP-M-06](../assurance/01-management/WP-M-06-confirmation-measures-plan.md)). No work product has had one, no
assessor is engaged (DQ-009), and the project has one person. A dashboard that showed accepted evidence before any
review had happened would be the one to distrust.

## How the records fit together

1. **Hazards and safety functions**, from the [risk assessment](../assurance/02-concept/WP-C-03-risk-assessment.md)
   and the [safety function specification](../assurance/02-concept/WP-C-04-safety-functions-and-plr.md), as trace
   items in [`assurance/trace/`](../assurance/trace/README.md). Each function carries a required PL.
2. **Claims**: the argument that each function achieves its PL and each hazard is reduced, broken into statements
   that can be evidenced, with the assumptions of use AOU-01 to AOU-08 attached.
3. **Evidence**, linked to claims: the PL calculation, the component certificates, the stopping and holding tests,
   the separation or force measurements, the fault-injection results, each with a review state.
4. **Defeaters**, attached to claims: the gap assessment, the open interfaces of the process model, the
   performance limits of the insufficiency analysis.
5. **Baselines and reviews**: named states of the whole, and the confirmation reviews recorded against them.

- [Read the safety case, WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md)
- [Known gaps](../assurance/00-assessment/gap-assessment.md)
- [Gate skeletons](../assurance/10-safety-case/gates/skeletons/), generated from the process model

> Assurance status represents recorded engineering evidence and review state. It does not constitute
> certification or approval for operation with a person in reach.
