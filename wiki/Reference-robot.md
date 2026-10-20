# Reference arm

The first configuration the assurance work analyses is the **reBot Arm B601-DM v1.1**: the variant with a released
BOM, STEP assembly and thermal test. It is a starting point, not a limit: the B601-RS variant is tracked and joins
the claimed scope when its BOM and software reach a repository, through a documented impact analysis. This page
says what the reference configuration is, why it was chosen, and what the fork adds to it before any powered test.

> **Nothing about this arm is approved for operation with a person inside its 650 mm reach.** As inherited it has
> no emergency stop in its documented design, no supply disconnect or fuse, no watchdog between the host and the
> actuators, and no declared joint limits ([gap assessment](../assurance/00-assessment/gap-assessment.md)).

## The B601-DM v1.1 at a glance

| Attribute | Value | Source |
|---|---|---|
| Arm | Six actuated joints plus one gripper; sheet-metal and CNC aluminium links, 3D-printed covers and fingers; about 4.5 kg; 650 mm reach; 1.5 kg payload, recommended continuous load under 1.5 kg within 70 % of reach; repeatability under 0.2 mm | upstream README; `hardware/reBot_B601_DM/readme.md` |
| Actuators | 4 × Damiao DM4310 (V4) and 3 × DM4340P (V4); joint 1 moved to a DM4340P in v1.1; closed actuator firmware with its own limits and over-temperature protection | BOM v1.1 changelog; gap assessment GAP-13, GAP-14 |
| Bus and harness | One CAN daisy chain on XT30 2+2 cables, terminated at the ends; a DM CAN-USB adapter to the host | BOM; gap assessment GAP-10, GAP-22 |
| Supply | MEAN WELL LRS-350-24, 24 V 14.6 A, open frame, mains-fed; no disconnect, no fuse, no keyed input | BOM; GAP-09, GAP-11, GAP-12 |
| Host and software | A PC (Jetson, Raspberry Pi or desktop) running the Python `motorbridge` SDK, the ROS 2 Humble driver with MoveIt 2 (in progress), Pinocchio kinematics, LeRobot policies, the YOLO grasping demo, a web UI; all in upstream repositories | upstream README roadmap; GAP-16 |
| Tele-operation and sensing | The Star Arm 102 leader arm; optional wrist cameras (D435i, D405, Gemini 305 or 2, UVC) | upstream README |
| Stop | A software command over the same CAN bus that drives the motors; a XIAO ESP32 wireless stop is mentioned upstream but not specified | GAP-08 |
| Thermal | Joint 2 reached 90 °C after more than two hours at 1.5 kg over 5 to 70 % of reach; the actuator's protection stopped a 2.5 kg run after 40 minutes | `performance_testing/Performance_Testing.md` |
| Mass distribution, fixing, joint gaps, end-stop angles, stopping time, gripper holding | Not stated anywhere | GAP-01, GAP-02, GAP-03, GAP-07 |

## What the fork adds before any powered test

The hold point [WP-V-07](../assurance/06-validation/WP-V-07-test-operations.md) requires bench safety hardware on any
arm the fork powers with a person in reach: a lockable disconnect and a fuse on the 24 V supply, a dual-channel
emergency stop on a pendant through a safety relay that drops the motor supply by contactor, the arm bolted to the
bench, a pinned software build, and a bench clear of everyone but the operator, whose hand is on the button. Buying
that hardware is a decision for the lead (DQ-006). The bench chain is carried forward as the first draft of the
product chain, not thrown away.

## What the reference configuration fixes

[WP-M-01 §3.1](../assurance/01-management/WP-M-01-assurance-strategy.md#31-reference-configuration-the-only-scope-claims-apply-to)
makes the reference configuration the only scope the claims apply to:

| Element | Reference configuration |
|---|---|
| Arm | The B601-DM v1.1 as a full kit or pre-assembled, plus the bench safety hardware; later the product chain of WP-S-03 |
| Function | Position, velocity and torque control from the SDK or ROS 2, teach by hand guiding for dataset collection, policy execution in RUN mode behind the clamps (DQ-008); the gripper; no mobile base |
| Software | A tagged fork release that pins the SDK and driver forks (DQ-007), the controller safety layer, the ROS 2 distribution and the policy checkpoints |
| Operating envelope | OE-1 as defined in [WP-C-02](../assurance/02-concept/WP-C-02-operating-environment-and-tasks.md): an indoor bench, the arm fixtured, a trained operator, nobody else inside the 650 mm reach while the arm can move (DQ-003) |
| Operator | A trained test operator with a hand on the pendant E-stop during development; briefed personnel after release |

## Why the B601-DM and not the RS variant

The B601-RS (RobStride actuators) shares the mechanical envelope but its BOM, assembly guide and software were
"in progress" at the baseline, and the two variants differ exactly where the safety case looks: the actuator's own
limits, its fault and over-temperature behaviour, and the bus protocol. A safety case can only be built on what can
be read and measured. The recommendation (decision DQ-001) is to assess the DM arm now and track the RS as a second
configuration, CFG-002, every value unverified until its BOM is released (DQ-017).

## Adding the RS variant or a second configuration

1. Record the new configuration with its item boundary and the actuator rows the DM case already states (limits,
   holding, thermal cut-off, bus, reliability data).
2. Write the impact analysis ([WP-M-11](../assurance/01-management/WP-M-11-impact-analysis.md) format): which
   hazards, safety functions, requirements and assumptions hold, which differ, and what evidence each needs.
3. Add the variant detection the package asked for, so the safety layer refuses an actuator it does not know.
4. Re-run the stopping, holding and thermal tests on the new actuators.
5. Run the generators and open a pull request.
