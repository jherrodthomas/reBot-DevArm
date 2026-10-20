# WP-P-08 Qualification of software components

| Field | Value |
|---|---|
| Work product | WP-P-08 Qualification of software components (motorbridge SDK, ROS 2, MoveIt 2, Pinocchio, LeRobot, third-party) |
| Standard reference | SRP/CS: 61508-3 §7.4.2.12; IEC 62443: 62443-4-1 SM-9, SM-10 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G3** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Per software component the fork relies on: what it does in the architecture, whether any safety function depends on it (none should), its version pin, its known defects, and what qualification argument, if any, is made.

## 2. Component list

motorbridge SDK, the Damiao and RobStride drivers, ROS 2 Humble, MoveIt 2, Pinocchio, LeRobot, the YOLO demo, the web UI.

## 3. Qualification arguments

Per component, or the statement that none is needed because no safety function depends on it.

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
