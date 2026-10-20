# WP-S-03 Technical safety concept: safety-related control system architecture

| Field | Value |
|---|---|
| Work product | WP-S-03 Technical safety concept: safety-related control system architecture (designated architectures, categories, channels, diagnostics, allocation of the safety functions) |
| Standard reference | Machinery: 10218-1 §5; SRP/CS: 13849-1 §6; Other: 60204-1 §9.4; ASPICE: SYS.3 |
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

The safety-related parts of the control system: a hardwired chain (dual-channel emergency stop and enabling inputs into a safety relay that removes the 24 V motor supply through a contactor, with monitored reset) and the controller safety layer (joint limits, torque and speed caps, the watchdog, the heartbeat) as the second checker. The chain is the checker of last resort: no input of the safety chain is reachable from the network, and nothing the host, the SDK or a policy sends can hold the contactor closed.

## 2. Designated architectures

Per safety function: category, channels, diagnostic coverage target, the parts that implement it (relay, contactor, drives, controller).

## 3. Allocation

Which function sits on the chain, which on the controller layer, which needs both (SF-08 safe stop: controller-initiated, chain-enforced).

## 4. Diagnostics

Contactor mirror contact, relay feedback loop, drive fault read-back, encoder plausibility.

## 5. Open items

Where the controller safety layer runs: on the host PC or on a dedicated controller between the host and the bus (DQ-020).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
