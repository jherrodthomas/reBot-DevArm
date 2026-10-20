# WP-A-05 Independence of the safety chain from the functional stack

| Field | Value |
|---|---|
| Work product | WP-A-05 Independence of the safety chain from the functional stack (freedom from interference) |
| Standard reference | SRP/CS: 13849-1 §6, §7; 61508-3 Annex F; IEC 62443: 62443-3-3 §5 (zoning) |
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

The argument that the chain cannot be defeated by the host stack, the SDK, a policy or the network: no electrical path from a host output to a chain input, no shared power rail that keeps the contactor closed, no software in the chain; and that the safety layer is free of interference from the host stack where both run on the same computer (DQ-020).

## 2. Interference paths considered

Electrical, logical, timing, power.

## 3. Argument per path

Why it cannot defeat the chain, with the evidence.

## 4. Residual dependencies

What the safety layer still shares with the host and what that costs.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
