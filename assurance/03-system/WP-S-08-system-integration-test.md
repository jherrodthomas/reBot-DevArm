# WP-S-08 System integration and test strategy, specification and report

| Field | Value |
|---|---|
| Work product | WP-S-08 System integration and test strategy, specification and report |
| Standard reference | SRP/CS: 13849-1 §8; IEC 62443: 62443-4-1 SVV-1; ASPICE: SYS.4 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G4** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

How the chain, the controller safety layer, the drives and the host are integrated and tested on the bench before any validation: integration steps, the tests of each interface, the report. Seeded from the integration tests of the package's test plan (TC-I-nn).

## 2. Integration strategy

Order: chain alone, chain plus drives, controller layer, host, policy runtime last.

## 3. Test specification

Per interface: test, expected result, pass criterion.

## 4. Report

Results at the baseline tested.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
