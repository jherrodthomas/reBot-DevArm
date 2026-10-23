# WP-H-03 Hardware failure analysis

| Field | Value |
|---|---|
| Work product | WP-H-03 Hardware failure analysis (FMEA, fault lists, fault exclusions) |
| Standard reference | SRP/CS: 13849-1 §6; 13849-2 Annex A–D; Other: IEC 60812; ASPICE: HWE.2 |
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

Failure modes of every part of the safety chain and of the drive path (relay, contactor, E-stop contacts, wiring, the drives' enable and fault lines, the actuator's brake or holding behaviour), the ISO 13849-2 fault lists applied, the fault exclusions claimed with their rationale. Seeded from the DFMEA of the package (`reBot_DevArm_DFMEA.xlsx`).

## 2. FMEA

Per component: failure mode, effect, detection, action.

## 3. Fault lists

ISO 13849-2 Annexes A–D applied to the chain.

## 4. Fault exclusions

Each with the rationale and the condition it depends on.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
