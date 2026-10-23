# WP-M-08 Cybersecurity plan

| Field | Value |
|---|---|
| Work product | WP-M-08 Cybersecurity plan |
| Standard reference | IEC 62443: 62443-4-1 §5 (SM-1…SM-13); 62443-4-2 §4; ASPICE: MAN.7 (CS) |
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

How cybersecurity is managed for the fork under IEC 62443-4-1 (secure product development lifecycle) and 62443-4-2 (component requirements), and how it interfaces with safety. The arm is treated as one component; the security level target is decision DQ-013 for the lead.

## 2. Scope and security context

The host PC with the Python SDK and the ROS 2 driver, the CAN-USB adapter, the motor bus, the optional web UI and tele-operation path, the optional wrist camera, the update path. The site network and the operator's computer are external zones.

## 3. Practices of IEC 62443-4-1 and where each lands

SM (management) here and WP-M-04/M-05; SR (requirements) WP-C-07, WP-C-08; SD (design) WP-S-07; SI (implementation) WP-W-01, WP-W-05, WP-W-11; SVV (verification) WP-W-11, WP-V-06; DM (defect management) WP-P-03, WP-O-05; SUM (updates) WP-P-10, WP-O-05; SG (guidelines) WP-S-06, WP-O-02.

## 4. Interface to safety

Threat scenarios that can cause a hazard are rated against the hazard list (WP-C-07 ↔ WP-C-03); the safety chain is a zone with no network conduit (WP-S-07 ↔ WP-S-03); safety parameters are protected assets (WP-W-09 ↔ WP-W-11).

## 5. Roles

| Role | Holder (today) | Duty |
|---|---|---|
| Cybersecurity manager | Jherrod Thomas (acting); permanent holder TBD | Owns this plan, the TRA and the security level target |
| External cybersecurity assessor | TBD | CS-I1 at G1, CS-A1 at G5 (WP-M-06 §7) |

## 6. Known starting position

Any process that can open the CAN-USB adapter can command every joint (gap assessment GAP-22); the tele-operation path has no authentication (GAP-23); the wrist camera stream is default-on where fitted (GAP-25).

## 7. Schedule

WP-C-07 and WP-C-08 by G1; WP-S-07 by G2; WP-W-11 by G3; WP-V-06 and WP-K-03 by G5.

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
