# WP-S-02 Safety requirements specification for the SRP/CS

| Field | Value |
|---|---|
| Work product | WP-S-02 Safety requirements specification for the SRP/CS |
| Standard reference | Machinery: 10218-1 §5; SRP/CS: 13849-1 §5; 62061 §6; Other: 60204-1 §9; ASPICE: SYS.2 |
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

Breaks every safety function of WP-C-04 into testable requirements SR-nn.mm: demand, safe state, response time measured at the drive input, stop category, diagnostics, reset behaviour, the modes it applies in. Seeded from the SAFE rows of the package's SyRS, SRS and HwRS.

## 2. Conventions

SR-<SF>.<nn>; response time runs from the demand to the start of power removal or the controlled stop at the drive input.

## 3. Requirements per safety function

One subsection per SF-nn.

## 4. Verification methods

Per requirement: inspection, analysis, test; the test lands in WP-V-02…V-05.

## 5. Traceability

To WP-C-04, WP-C-06 and the hazards of WP-C-03.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
