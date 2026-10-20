# WP-C-07 Cybersecurity threat and risk assessment

| Field | Value |
|---|---|
| Work product | WP-C-07 Cybersecurity threat and risk assessment |
| Standard reference | IEC 62443: 62443-4-1 SR-2; 62443-3-2 §5; ASPICE: SEC.1 |
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

Threat and risk assessment of the arm as one component: assets (the motion command path, the safety parameters, the camera stream, the policy checkpoints), threat scenarios TS-nn, their likelihood and their safety impact. Safety impact is anchored to the hazard list of WP-C-03: a threat that can cause a hazard is rated with that hazard's severity.

## 2. Assets and zones

The host, the CAN-USB adapter and motor bus, the optional web UI and tele-operation path, the wrist camera, the update path.

## 3. Threat scenarios

TS-nn: unauthenticated motion commands over the bus or the network (GAP-22, GAP-23), parameter tampering, replay, denial of service on the heartbeat, a malicious policy checkpoint, camera exfiltration.

## 4. Risk rating

Likelihood × safety impact; the rows that reach a hazard become cyber-induced hazards in WP-C-03 §4.

## 5. Outputs

Security level target and requirements in WP-C-08.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
