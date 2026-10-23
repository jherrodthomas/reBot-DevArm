# Frequently asked questions

Short answers with a link to the record that holds the long one.

## Is the arm safe, certified or CE-marked?

No. reBot-DevArm is research and education hardware. As inherited it has no emergency stop in its documented
design, no supply disconnect or fuse, no watchdog between the host and the actuators, no declared joint limits and
no force measurement; its only stop is a software command on the motor bus. The fork's record exists to change that
in the open, starting with the [gap assessment](../assurance/00-assessment/gap-assessment.md). No safety function
reaches any Performance Level today, no assessment has taken place, and nothing is approved for operation with a
person in reach. [For the assessor](For-the-assessor.md) says what an assessment would involve.

## Is the fork safer than upstream reBot-DevArm?

Not yet, and the project does not claim it is. The fork has changed no hardware and no code; what it adds today is
the record: the concept-phase package, the gap assessment, the strategy, the plans, the register and the process
model. The first engineering change will be bench safety hardware on any arm the fork powers, and it waits on a
decision by the lead (DQ-006).

## Why machinery standards and not ISO 26262?

Because a robot arm on a bench is machinery under Regulation (EU) 2023/1230, and an industrial robot under
ISO 10218, not a road vehicle. The standards are ISO 12100, ISO 10218-1/-2, ISO/TS 15066, ISO 13849-1, EN 60204-1,
IEC 62443 and ISO/IEC TR 5469. [How we use each standard](How-we-use-each-standard.md) has the mapping.

## What is a Performance Level, and why PL d?

ISO 13849-1's measure of how reliably a safety function performs, PL a to PL e. ISO 10218-1 expects PL d, category
3, for the emergency stop and the protective stop of an industrial robot, and the package's risk graph lands most
contact hazards on d or e. That is the planning assumption; whether the lead accepts it, or restricts the arm to a
supervised bench at a lower level, is an open decision (DQ-004). See the [glossary](Glossary.md).

## Where are the safety functions implemented?

The emergency stop on a hardwired chain: two-channel buttons into a safety relay that drops a contactor on the
24 V motor supply. The safe stop on watchdog, the manual reset, the joint, torque and speed limits and the contact
detection in a controller safety layer between every command source and the motor bus, where it runs being a
decision for the lead (DQ-020). The host stack (the SDK, ROS 2, the policies, the UI) is hardened as defence in
depth and carries no Performance Level claim in the first safety case. The argument is in
[WP-M-01 §6](../assurance/01-management/WP-M-01-assurance-strategy.md#6-safety-architecture-argument-the-central-strategy).

## Can a person be inside the reach while the arm moves?

Not inside the first safety case. The recommended envelope (DQ-003) is a supervised, fixtured bench with nobody but
the operator in reach, and no power-and-force-limiting claim is made (DQ-005): the arm has no joint torque sensors
and no force or pressure measurement exists (GAP-28). Contact detection by torque estimation is defence in depth,
not permission to touch.

## Why a fork rather than contributing upstream?

The assurance work needs a record that moves at its own pace, with its own baselines, gates and decision
authority, and must be free to say what the evidence does not support. Upstream's hardware record is merged, never
edited, and the fork is not affiliated with or endorsed by Seeed Studio
([WP-M-10](../assurance/01-management/WP-M-10-upstream-and-supplier-management.md)). Whether the software that moves
the arm is forked too is an open decision (DQ-007).

## What does the non-commercial licence mean for the record?

Upstream publishes under CC BY-NC-SA 4.0: the record and any build of it stay non-commercial and share alike. A
safety-assured arm placed in a workplace may be commercial use under upstream's own statement, which is one reason
the first safety case covers the research bench only (GAP-35, [WP-M-13](../assurance/01-management/WP-M-13-regulatory-conformity-strategy.md)).

## Where is the Living Safety Case dashboard?

On the README, generated from the records in [`case/`](../assurance/case/README.md) by CI. No number on it is a
safety claim: a claim counts as accepted only when a recorded review accepts it, its evidence is available and
accepted, and no defeater against it is open. Today nothing is accepted and every defeater is open.

## Who decides what?

The project lead is the safety authority and decides risk acceptance, the required PL, arm behaviour defaults,
operating-envelope limits, money, hardware, the assessor, roles and gates. Everything else is a technical choice,
recorded so the lead can change it. See [how decisions are made](How-decisions-are-made.md).

## I found a safety problem. Where do I report it?

- A security vulnerability: follow [SECURITY.md](../SECURITY.md).
- A hazard, a near miss or an event: the Safety concern issue template.
- Anything else: the Problem report template. See [reporting a safety concern](Reporting-a-safety-concern.md).

## Why is so much of it written with Claude?

Drafting is done in Claude Code sessions under the project lead's direction; the working rules are in
[CLAUDE.md](../CLAUDE.md). Every change goes through pull request review and the workflows described in
[how the repository is organized](How-the-repository-is-organized.md). The lead holds every safety decision, AI-drafted
work counts at independence level I0, and no work product leaves draft without a review by someone else
([WP-M-02 §3.3](../assurance/01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)).

## Something is missing here

Open an [issue](https://github.com/jherrodthomas/reBot-DevArm/issues). Questions that come up more than
once get added to this page by pull request against [`wiki/`](../wiki/README.md).
