# WP-S-07 Cybersecurity architecture

| Field | Value |
|---|---|
| Work product | WP-S-07 Cybersecurity architecture (zones, conduits, controls) |
| Standard reference | IEC 62443: 62443-4-1 SD-1…SD-4; 62443-3-3 §5; ASPICE: SEC.1, SYS.3 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G2** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Zones and conduits of the arm: the host zone, the motor-bus zone, the camera, the network. The safety chain is a zone of its own with no conduit from the host network; every path that can command motion is authenticated; the safety parameters are protected assets.

## 2. Zones and conduits

Diagram and table.

## 3. Controls per conduit

Authentication, integrity, rate limiting, logging.

## 4. Traceability

To WP-C-08 and WP-S-03.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
