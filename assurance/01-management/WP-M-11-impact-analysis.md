# WP-M-11 Impact analysis of the inherited reBot-DevArm baseline

| Field | Value |
|---|---|
| Work product | WP-M-11 Impact analysis of the inherited reBot-DevArm baseline (modification of existing machinery) |
| Standard reference | Machinery: 12100 §4; SRP/CS: 61508-1 §7.16 (modification); IEC 62443: 62443-4-1 SM-3; Other: Machinery Reg. Art. 3 (substantial modification); ASPICE: SUP.10 |
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

Impact analysis of using the inherited reBot-DevArm baseline as the starting point of a machine that is to carry a safety case: what is reused, what is reworked, what is discarded, and what each inherited element's state means for the lifecycle entry (WP-M-01 T-01).

## 2. Baseline

The commits of the gap assessment header; every finding GAP-01…GAP-34 is an input.

## 3. Reuse classification per element

Per element: reuse unchanged (the mechanical design, the actuators), reuse with hardening (the motorbridge SDK and the ROS 2 driver, once forked), replace or add (the emergency-stop chain, the supply disconnect, the fusing), new (every safety work product). With the rationale and the gaps it inherits.

## 4. Consequences for the lifecycle

Full concept phase; no inherited safety work product beyond the concept-phase engineering package, which is an input; the controller safety layer is hardened as defence in depth; the chain is new hardware.

## 5. Change impact analysis records

Later changes are analysed per change under `07-supporting/impact/`; this document covers only the entry.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
