# WP-M-04 Organization-specific rules, safety culture, competence management

| Field | Value |
|---|---|
| Work product | WP-M-04 Organization-specific rules, safety culture, competence management |
| Standard reference | SRP/CS: 61508-1 §6.2 (competence); 13849-1 §4; IEC 62443: 62443-4-1 SM-4 |
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

Rules of the organisation that produces the record: who may approve what, how competence is shown for each role of WP-M-02 §3.1, how a safety concern is raised, and how AI-assisted authoring is bounded (WP-M-02 §3.3).

## 2. Organisation rules

Branch protection, CODEOWNERS, two approvals on safety-relevant paths, no self-merge of safety work once a second person exists.

## 3. Competence

Per role: the knowledge needed (ISO 10218, ISO/TS 15066, ISO 13849, EN 60204-1, CAN-bus motor control, the Damiao and RobStride actuators) and the evidence kept.

## 4. Safety culture

Raising a concern stops the test; nobody is blamed for a stop; near misses are recorded.

## 5. Training record

Operators trained on WP-V-07 before any powered test.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
