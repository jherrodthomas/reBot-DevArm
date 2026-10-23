# WP-W-01 SW development environment, languages and coding guidelines

| Field | Value |
|---|---|
| Work product | WP-W-01 SW development environment, languages and coding guidelines |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.4.4; IEC 62443: 62443-4-1 SI-1, SI-2; ASPICE: SWE.3 |
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

Languages, toolchains, coding rules and the test environment for the fork's safety-relevant software: the controller safety layer (C or C++ on a microcontroller, or Python on the host, per DQ-020), the SDK and ROS 2 hardening, pinned dependencies, reproducible builds.

## 2. Environment

Toolchain versions, pinned, reproducible.

## 3. Guidelines

Coding rules per language; what the static analysis checks.

## 4. Test environment

Unit tests, the bench harness, hardware-in-the-loop.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
