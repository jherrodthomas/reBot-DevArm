# WP-C-10 Functional insufficiency analysis of sensing and the learned policy

| Field | Value |
|---|---|
| Work product | WP-C-10 Functional insufficiency analysis of sensing and the learned policy (performance limits, triggering conditions) |
| Standard reference | Machinery: 10218-1 §5 (collision detection limits); 12100 §5.4; Other: ISO 21448 §6–§7 (informative method); IEC 62998-1 |
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

Where the sensing and the learned components fall short without any fault: the joint torque estimator (no joint torque sensor; current-based estimation with gravity compensation), the wrist camera, the policy. What the joint torque estimator cannot sense bounds the claim SF-02 and SF-04 can make: a contact that produces less motor current than the estimation noise is invisible to every software layer.

## 2. Functional insufficiencies

FI-nn: torque estimation resolution and latency, friction and payload masking of contact, encoder resolution, camera occlusion and lighting, policy distribution shift.

## 3. Triggering conditions

TC-nn: a slow contact, a contact near the base with high mechanical advantage, a heavy payload, an unlit scene, an object outside the training set.

## 4. Consequences

Per pair: which hazard, which safety function's claim is bounded, and what measure (speed limit, separation, measurement) covers it.

## 5. Open items

The measurement that would settle the estimator's floor (WP-V-03).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
