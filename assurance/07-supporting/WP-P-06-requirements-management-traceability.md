# WP-P-06 Requirements management and traceability procedure

| Field | Value |
|---|---|
| Work product | WP-P-06 Requirements management and traceability procedure |
| Standard reference | SRP/CS: 13849-1 §5; 61508-3 §7.2; IEC 62443: 62443-4-1 SR-5; ASPICE: SYS.2, SWE.1. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: identifier families and attributes, the trace chain, what CI checks today and what it will check; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How requirements are written, identified, linked to hazards, safety functions and tests, and kept consistent. The
data lives in [`trace/`](../trace/README.md) (WP-T-01) as machine-readable items; the work products that specify the
requirements quote them and own their wording.

The seed is the concept-phase package: `reBot_DevArm_Requirements.xlsx` holds 104 requirements (35 `SYRS-nnn`,
38 `SRS-nnn`, 31 `HWRS-nnn`) and `reBot_DevArm_TestPlan.xlsx` 127 test cases (49 `TC-U-nn`, 23 `TC-I-nn`, 22
`TC-S-nn`, 33 `TC-Q-nn`), with trace and verification matrices. They are an input: they are re-identified on the
record's conventions as the owning work products are written, each new item keeps the package identifier it came
from, and the workbooks are not edited.

## 2. Identifiers and attributes

| Family | Prefix | Owned by | Seed from the package | In `trace/items/` |
|---|---|---|---|---|
| Hazard | `HZ-<cat><nn>` | [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) | Same identifiers | Yes: 34 in `hazards.yaml` |
| Safety function | `SF-<nn>` | [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md) | Same identifiers; reclassified numbers stay reserved | Yes: 20 in `hazards.yaml` |
| Design measure, information for use | `DM-<nn>`, `IFU-<nn>` | WP-C-03, WP-C-05 | Package SFs reclassified | Not yet |
| Assumption of use | `AOU-<nn>` | [WP-C-01](../02-concept/WP-C-01-item-definition.md) | `ASS-A-01…08` | Yes: 8 in `aou.yaml` |
| System requirement (functional) | Not yet defined; `SYS-<nnn>` proposed | [WP-S-01](../03-system/WP-S-01-system-requirements.md) | `SYRS-nnn` | Not yet |
| Safety requirement of the SRP/CS | `SR-<nn>` | [WP-S-02](../03-system/WP-S-02-safety-requirements.md) | `SRS-nnn` | Not yet |
| Hardware safety requirement | `HWSR-<nn>` | [WP-H-01](../04-hardware/WP-H-01-hardware-safety-requirements.md) | `HWRS-nnn` | Not yet |
| Software safety requirement | `SWSR-<nn>` | [WP-W-02](../05-software/WP-W-02-software-safety-requirements.md) | Parts of `SRS-nnn` | Not yet |
| Cybersecurity requirement | `CSR-<nn>` | [WP-C-08](../02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md) | — (the package's `GAP-CYB` findings are inputs) | Not yet |
| Requirement on a learned component | `AIR-<nn>` | [WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md) | — | Not yet |
| Safety-related parameter | `PAR-<nn>` | [WP-W-09](../05-software/WP-W-09-safety-parameters-and-configuration-data.md) | Values inside `SRS`/`HWRS` rows | Not yet |
| Test case | `VS-<area>-<nn>` | WP-V-01 and the test work products | `TC-U`, `TC-I`, `TC-S`, `TC-Q` | Not yet |

The package's `TC-x-nn` test identifiers clash with the record's `TC-<nn>` (triggering condition, WP-C-10), so they
are kept only as the source reference of a `VS-` item, never used as an identifier in the record.

**Attributes.** Every item is a flat mapping in the restricted YAML subset the case records use
([case README](../case/README.md#record-format-and-rules)): `id`, `kind`, `title` (the statement), `status`
(`proposed`, `approved`, `withdrawn`), `source` (owning work product). Requirements add `derived_from` (parent
identifiers), `allocated_to` (chain, controller safety layer, host, actuator, information for use), `plr` where it
serves a safety function, `verification` (test, analysis, inspection, review), `verified_by` (`VS-` identifiers),
`package_ref` and `rationale`.

**Writing rules.** One requirement per item, with "shall"; measurable values with units and tolerance; allocated to
one element; no "should", "as fast as possible" or "where possible". A requirement on a learned component never
allocates a safety function to it (WP-M-01 T-03). An identifier is never reused; a withdrawn item keeps its
identifier with status `withdrawn`.

## 3. Traceability

```
hazard (HZ) ──> safety function (SF) or design measure (DM) or information for use (IFU)
  SF ──> safety requirement (SR) ──> hardware (HWSR), software (SWSR), parameter (PAR)
  SR, HWSR, SWSR, PAR ──> test case (VS) ──> result ──> evidence (Sn-nn) ──> claim (G…)
threat scenario (TS) ──> cybersecurity requirement (CSR) ──> VS
insufficiency (FI) / triggering condition (TC) ──> requirement on a learned component (AIR) ──> VS
```

Each lower item names its parents in `derived_from`; the reverse direction is computed, never typed twice. The
Living Safety Case links claims to hazards, assumptions and requirements through its `related_*` fields. WP-T-01 will
generate the matrices (hazard to safety function, safety function to requirement, requirement to test) into
`trace/maps/`; none exists yet. A change to an item follows [WP-P-02](WP-P-02-change-management.md), and its impact
analysis follows the links in both directions.

## 4. Consistency checks

**What CI checks today.** `assurance/case/tools/validate.py` (rule V3) resolves every hazard, assumption and
requirement reference in the case records against the items in `trace/items/`, and checks the prefix allowed for
each: `H`, `HE`, `HZ`, `SF` for the hazard log; `AOU` for assumptions; `SR`, `SF`, `TSR`, `SWSR`, `HWSR`, `CSR` for
requirements ([`case-schema.json`](../case/schema/case-schema.json)). Identifiers are checked for uniqueness among
the case records (V2), but not among the trace items: a duplicate trace identifier would silently replace the first.

**What is still to be built (WP-T-01 §3).** Every hazard has a safety function, a design measure or an instruction;
every safety function has SR rows; every SR, HWSR, SWSR, CSR and AIR has at least one `VS-` test; no item has a parent
that does not exist; no identifier is reused or deleted; generated matrices match the items.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Import the package's requirements and test cases as items once WP-S-02 fixes the scheme (WP-T-01 OI-1) | Safety manager | G2 |
| OI-2 | Write the trace checker for the §4 rules, including uniqueness across `trace/items/`, and run it in CI | Safety manager | G1 |
| OI-3 | Align the schema's requirement prefixes with the README identifiers (`AIR`, `PAR` missing; `TSR` not in the README) | Safety manager | G1 |
| OI-4 | Add a prefix for system requirements of WP-S-01 to the README identifier table (`SYS-<nnn>` proposed) | Safety manager | G2 |
| OI-5 | Add the item kinds for `DM`, `IFU`, `TS`, `FI` and `TC` so the safety case can reference them | Safety manager | G1 |
