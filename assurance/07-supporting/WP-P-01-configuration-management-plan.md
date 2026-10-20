# WP-P-01 Configuration management plan

| Field | Value |
|---|---|
| Work product | WP-P-01 Configuration management plan (safety-relevant file list, baselines across the fork repositories) |
| Standard reference | SRP/CS: 61508-1 §6.2.3; 13849-1 §12; IEC 62443: 62443-4-1 SM-6, SM-7; ASPICE: SUP.8 |
| Version | 0.0 (skeleton: structure and clause map; 2026-10-20) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `206ebda` |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Configuration management for the record and for the fork's code: the safety-relevant file list (`safety-relevant-paths.txt`), the baselines BL-nnn across this repository and the software repositories once forked (DQ-007), the pins of upstream and of every dependency.

## 2. Configuration items

This repository, the hardware record, the software forks, the parameter sets, the policy checkpoints.

## 3. Safety-relevant file list

The classes SR-A, SR-Q, SR-T and what each requires.

## 4. Baselines

How a baseline is cut, tagged and frozen; BL-001 is the inherited state.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
