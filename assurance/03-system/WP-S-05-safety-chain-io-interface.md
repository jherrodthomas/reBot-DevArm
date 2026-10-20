# WP-S-05 Hardware-software interface of the safety chain

| Field | Value |
|---|---|
| Work product | WP-S-05 Hardware-software interface of the safety chain (I/O map, signal semantics) |
| Standard reference | SRP/CS: 13849-1 §6, §7; ASPICE: SYS.3 |
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

The I/O map between the safety chain and the controller: the relay feedback, the contactor mirror contact, the enable and reset inputs, the drive enable lines, and the semantics of each signal (level, timing, what the controller may conclude from it). The signals are informative to the controller and never a channel of a safety function.

## 2. I/O map

Signal, source, sink, electrical level, timing, failure state.

## 3. Semantics

What each signal means and what the controller does on each transition.

## 4. Traceability

To WP-S-03 and WP-W-03.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
