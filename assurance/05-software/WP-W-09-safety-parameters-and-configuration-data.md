# WP-W-09 Safety-related parameters and configuration data

| Field | Value |
|---|---|
| Work product | WP-W-09 Safety-related parameters and configuration data (joint, torque and speed limits, contact thresholds, watchdog timings) |
| Standard reference | Machinery: 10218-1 §5; SRP/CS: 13849-1 §7 (parameterization); IEC 62443: 62443-4-2 CR 3.4; ASPICE: SWE.3 |
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

The safety-related parameters of the arm: per-joint position limits inboard of the end-stops, torque and speed caps per operating envelope, the contact-force thresholds, the watchdog and heartbeat timings, the actuator variant table (Damiao, RobStride). Parameter integrity is a cybersecurity requirement verified in WP-W-11.

## 2. Parameter sets

PAR-nn per parameter: value per operating envelope, source, who may change it.

## 3. Integrity

How a parameter set is signed, loaded and checked at boot.

## 4. Change control

A parameter change is an SR-A change (WP-P-02).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
