# WP-W-10 ML engineering: data, training, testing and deployment of learned components

| Field | Value |
|---|---|
| Work product | WP-W-10 ML engineering: data, training, testing and deployment of learned components |
| Standard reference | Other: TR 5469 §8–§10; AI Act Art. 10, Art. 15; ASPICE: MLE.1–4, SUP.11 |
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

How the learned components of WP-C-09 are built and deployed: datasets and their provenance, training, testing against the hazard list (the policy edge-case coverage matrix the package asked for, GAP-24), checkpoint identity at run time, the clamping that keeps them outside every safety function.

## 2. Data and training

Per component: datasets, training record, checkpoint hash.

## 3. Testing

Coverage of the hazard list and of the triggering conditions of WP-C-10.

## 4. Deployment

Checkpoint pinning, run-time identity, logging.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
