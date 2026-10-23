# WP-C-09 ML component definition and safety requirements

| Field | Value |
|---|---|
| Work product | WP-C-09 ML component definition and safety requirements (learned policies, perception models) |
| Standard reference | Other: TR 5469 §6–§8 (classes, usage levels, properties); AI Act Annex IV; ASPICE: MLE.1 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G1** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Defines each learned component the arm runs (LeRobot imitation policies, the YOLO grasping demo, any vision-language-action model), its AI technology class and usage level under ISO/IEC TR 5469, and the requirements AIR-nn on it. No safety function is allocated to a learned component; the controller safety layer and the chain are the independent safeguard, so every policy output is clamped to the joint, torque and speed limits before it reaches a drive.

## 2. Learned components

ML-nn: what it is, which inputs, which outputs, where it runs, which checkpoint.

## 3. Classification

Class and usage level per component; the argument that each sits outside every safety function (WP-C-04 §5).

## 4. Requirements

AIR-nn: output clamping, out-of-distribution handling (stop, not guess), a recorded checkpoint per test, no learned component in the stop path.

## 5. Open items

Which policies the first safety case covers at all (DQ-008).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
