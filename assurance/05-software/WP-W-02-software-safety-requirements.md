# WP-W-02 Software safety requirements specification

| Field | Value |
|---|---|
| Work product | WP-W-02 Software safety requirements specification (SRESW, SRASW) |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.2; ASPICE: SWE.1 |
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

Software safety requirements SWSR-nn for the controller safety layer and for the hardened SDK and ROS 2 driver: command validation (finite, bounded, fresh), joint, torque and speed clamps, the watchdog and heartbeat, the mode state machine, the fault reactions, the parameter integrity. Seeded from the SRS rows of the package.

## 2. Requirements

SWSR-nn with the SR-nn.mm each implements.

## 3. Interfaces

What the software reads from the chain (WP-S-05) and what it may conclude.

## 4. Traceability

To WP-S-02 and to the tests of WP-W-06.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
