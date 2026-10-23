# WP-W-03 Software architectural design

| Field | Value |
|---|---|
| Work product | WP-W-03 Software architectural design (controller safety layer, separation from the host stack) |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.4.3; IEC 62443: 62443-4-1 SD-2; ASPICE: SWE.2 |
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

The software architecture: a small safety layer between every command source (SDK, ROS 2, leader arm, policy runtime) and the motor bus, which validates, clamps, times out and reports; the host stack above it; the chain below it. The I/O semantics of WP-S-05 are the controller's contract with the safety chain.

## 2. Layers

Host stack, safety layer, drives; what each may and may not do.

## 3. Safety layer design

Components, data flow, timing, the mode state machine (OFF, IDLE, TEACH, RUN, ESTOP).

## 4. Separation

How the safety layer is kept free of interference from the host stack (WP-A-05).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
