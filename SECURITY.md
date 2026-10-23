# Security Policy

This fork of reBot-DevArm carries the safety-assurance record for a desktop robot arm. A security problem in the
arm's software can move a machine with a person in reach, so please report it privately.

## Reporting a vulnerability

- Use GitHub private vulnerability reporting on this repository: **Security** tab → **Report a vulnerability**
  (or [open a report directly](https://github.com/jherrodthomas/reBot-DevArm/security/advisories/new)).
- Do not open public issues, pull requests or discussions for security problems.

Please include the affected repository and commit (this record, or one of the software forks once they exist), the
arm configuration, a description of the issue and its impact, and how you found it. Proof-of-concept material is
welcome but not required. Do not send personal data of other people.

### What to expect

- Acknowledgement within 3 working days.
- Initial assessment within 5 working days (2 if the issue could move the robot or defeat a stop).
- If the issue can affect safety, we may say to stop powering the arm with anyone in reach before a fix is ready. Such notices contain
  no technical detail.
- We aim to release a fix and publish an advisory within 90 days, and we coordinate disclosure timing with you. We
  credit reporters who wish to be credited.

### Scope

In scope: this repository, the fork's software repositories once they exist (the forked SDK and ROS 2 driver, the
controller safety layer), their builds, and the fork's update and release process.

Out of scope here: upstream reBot-DevArm and its software (Seeed Studio), the actuators' firmware (Damiao,
RobStride), ROS 2, LeRobot and third-party services. Report those to their owners. If you are unsure, report to us
and we will route it.

### Testing rules

Test only on equipment you own or are authorised to test. Never test on an arm with anyone inside its reach.
Do not access other people's devices, networks or accounts, and do not attack upstream or third-party
infrastructure.

### Supported releases

The fork publishes no release yet. When it does, only the latest release receives security fixes.

The process behind this policy is [WP-O-05](assurance/09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md);
the cybersecurity plan is [WP-M-08](assurance/01-management/WP-M-08-cybersecurity-plan.md).

## Cybersecurity engineering under IEC 62443

Cybersecurity is treated as an engineering discipline alongside machinery safety, not only as vulnerability
intake. The fork follows IEC 62443-4-1 (secure product development lifecycle) and IEC 62443-4-2 (component
requirements) with a security level target the project lead decides (DQ-013). The known starting position, from the
[gap assessment](assurance/00-assessment/gap-assessment.md): anyone with the CAN-USB adapter open can command every
joint (GAP-22), tele-operation and the web UI are unauthenticated (GAP-23), the wrist camera streams by default
(GAP-25), and the software is unpinned (GAP-16). Threats that can cause a hazard are rated against the hazard list,
and the hardwired safety chain is designed as a zone with no conduit from the host or the network, so that no attack
on the software can hold the contactor closed.
