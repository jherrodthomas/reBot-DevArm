# WP-T-01 Requirements and traceability data

| Field | Value |
|---|---|
| Work product | WP-T-01 Requirements and traceability data (machine-readable), consistency evidence |
| Standard reference | SRP/CS: 13849-1 §5; 61508-3 §7.2; IEC 62443: 62443-4-1 SR-5; ASPICE: consistency evidence (SYS.2–5, SWE.1–6) |
| Version | 0.0 (skeleton: structure and clause map; the hazard, safety-function and assumption items exist; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G1→G5** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Machine-readable requirement and trace data: hazards, safety functions, requirements, parameters, tests and their
links, with the consistency checks CI runs; the data behind the trace matrices. The concept-phase package already
holds 104 requirements (SyRS, SRS, HwRS) and 127 test cases with a trace matrix (`reBot_DevArm_Requirements.xlsx`,
`reBot_DevArm_TestPlan.xlsx`); they are the seed, to be re-identified on the record's conventions (WP-P-06) as
WP-S-01, WP-S-02, WP-W-02 and WP-V-01 are written.

## 2. Data files

`items/*.yaml` per identifier family: [`items/hazards.yaml`](items/hazards.yaml) (HZ-M01…HZ-D01 from WP-C-03 and
SF-01…SF-32 from WP-C-04) and [`items/aou.yaml`](items/aou.yaml) (AOU-01…AOU-08 from WP-C-01) exist and are what the
safety-case validator resolves references against; requirements and tests follow with WP-S-02; `maps/` for the
generated matrices.

## 3. Checks

Every hazard has a safety function, a design measure or an instruction; every safety function has SR rows; every
SR row has a test; every ID is unique and never reused (the package's SF numbers reclassified in WP-C-03 §5.2 stay
reserved).

## 4. Figures

Generated trace figures, checked by CI; none yet.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Import the package's requirements and test cases as items once WP-S-02 fixes the identifier scheme | Safety manager | G2 |
