# WP-M-10 Upstream

| Field | Value |
|---|---|
| Work product | WP-M-10 Upstream (Seeed Studio) and supplier (Damiao, RobStride) management |
| Standard reference | SRP/CS: 61508-1 §6.2 (subcontracted activities); IEC 62443: 62443-4-1 SM-9, SM-10; ASPICE: ACQ.4 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

How the fork takes changes from upstream Seeed Studio, what it asks of the actuator suppliers (Damiao, RobStride) and of the other component suppliers (the PSU, the CAN-USB adapter, the gripper servo), and how a supplier's data enters the record.

## 2. Upstream

Read-only use of `Seeed-Projects/reBot-DevArm` and the software repositories it points to; upstream changes arrive by merge with an impact analysis (WP-M-11 format); the fork never implies Seeed Studio's endorsement; the CC BY-NC-SA 4.0 licence is kept.

## 3. Suppliers

Damiao DM4310 and DM4340P (V4) and the RobStride equivalents: datasheets, firmware versions, the fault behaviour on over-temperature and bus loss, and the reliability data (MTTFD or B10D) that WP-H-04 needs (DQ-019).

## 4. Supplier evidence

What counts as evidence from a supplier (a datasheet value, a certificate, a test report) and how it is stored under WP-H-07.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
