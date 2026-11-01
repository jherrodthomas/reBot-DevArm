# WP-P-04 Documentation management

| Field | Value |
|---|---|
| Work product | WP-P-04 Documentation management |
| Standard reference | Machinery: 12100 §7; SRP/CS: 13849-1 §12; IEC 62443: 62443-4-1 SG-1; Other: Machinery Reg. Annex IV; ASPICE: SUP.7. Clause numbers are to be checked against licensed copies |
| Version | 0.1 (first draft: header rules, status and version scheme, generated files, checks, technical file; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

The rules every document of the record follows: the document-control header, what each status means, how versions are
numbered, which files are generated and by what, the checks CI runs on the Markdown, and how the technical file
([WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md)) is assembled. Documents are Markdown files in
this repository, changed only by pull request ([WP-P-02](WP-P-02-change-management.md)); the git history is their
revision history.

## 2. Document control

### 2.1 Header

Every work product starts with the table of the [assurance README](../README.md#document-control-header):

| Field | Rule |
|---|---|
| Work product | `WP-<area>-<nn>` and the name as in [WP-M-00 §3](../01-management/WP-M-00-work-product-register.md#3-register) |
| Standard reference | The clauses the work product answers. No standard is held, so every clause reference is marked as to be checked against a licensed copy |
| Version | `<number> (<one-line summary>; <YYYY-MM-DD>)`, see §2.3 |
| Status | One of the values in §2.2; the same value as the register's status column |
| PL / scope | Highest PLr addressed, or process, cybersecurity or ML |
| Author | The person or team who wrote it; an AI-assisted draft says so and carries I0 ([WP-M-02 §3.3](../01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)) |
| Reviewer(s) | Name and independence level I0–I3 of each verification reviewer; `TBD (I1)` until a review is recorded |
| Approver | The role in the safety plan; a self-approval under DQ-010 is written as such |
| Baseline | `BL-nnn (<short SHA>)`: the configuration the content refers to ([WP-P-01 §4](WP-P-01-configuration-management-plan.md#4-baselines)) |

### 2.2 Status transitions

| From | To | When | Who |
|---|---|---|---|
| Skeleton | Draft | The content is written, with an open items table of what is still missing | Author |
| Draft | In review | A pull request asks for verification review per [WP-P-05](WP-P-05-verification-review-procedure.md) | Author |
| In review | Approved | The review is `accepted` and the approver approves; under DQ-010 the safety manager may approve own work, recorded as self-approval at I0 | Approver |
| Approved | Baselined | The work product is part of a frozen baseline | Configuration and change manager |
| Approved or Baselined | Draft | Its content changes; the change carries an impact record (WP-P-02 §2) | Author |
| Any | N/A (tailored) | Tailored out, with a reference to [WP-M-01 §5](../01-management/WP-M-01-assurance-strategy.md#5-tailoring) | Safety manager |

The header and the register change in the same pull request. No tool checks that they agree yet (OI-1); the folder
README tables repeat the register's column, not the header.

### 2.3 Version numbers

`0.0` is a skeleton. `0.1`, `0.2` … are drafts, one step per substantive revision merged to `main`. `1.0` is the first
Approved version; `1.1` … are approved revisions; a version that is Baselined keeps its number and the baseline names
it. Editorial fixes that change no content do not change the number.

### 2.4 Content rules

Plain, concrete prose; tables where they help. Identifiers follow the [assurance README conventions](../README.md#identifiers)
and are never reused. No sentence says an activity was performed, reviewed or approved unless the record shows it,
and no work product claims compliance. The wiki explains and links; it never claims. The concept-phase package at the
root is an input, cited by its identifiers, never edited. `hardware/` is upstream's and is only merged.

## 3. Generated documents

Generated files are never edited by hand; the source is changed, the generator run, and its output committed in the
same pull request. Folder READMEs carry a line saying which generator wrote them.

| Generator | Outputs | Checked in CI by |
|---|---|---|
| `assurance/tools/folder_index.py` | `assurance/<numbered folder>/README.md` | `--check` (assurance workflow) |
| `assurance/process/tools/process_model.py` | `process/maps/*.md`, `10-safety-case/gates/skeletons/*.md` | `--check` and its tests |
| `assurance/process/tools/process_figures.py` | `docs/assets/rebot/process/` swimlane figures | `--check` and its tests |
| `assurance/case/tools/generate_dashboard.py` | `case/status.json`, `case/badge.json`, the dashboard SVGs, the README summary blocks | `--check`, after `validate.py` |
| `assurance/01-management/decisions/fig_lifecycle.py` | `decisions/figures/fig-dr-1-lifecycle.svg` | `--check` and its tests |
| `docs/assets/rebot/make_assets.py` | README and wiki figures | `--check` and its tests |
| `docs/assets/rebot/banner.py` | `banner.svg`, `banner-arm.jpg` | `--check` and its tests |
| `tools/wiki/tour_figures.py` | `docs/assets/rebot/tour/*.svg` | its test runs `--check` (wiki workflow) |
| `assurance/sim/figures/fig_sim_hero.py` | `sim/figures/sim-hero-dashboards.jpg` | `--check` |
| `assurance/sim/blender/gallery.py` | `sim/blender/dashboards/` | Not checked: it needs local Blender renders |
| `tools/wiki/build_wiki.py` | The GitHub wiki, built from `wiki/` and pushed on every merge to `main` | Built on every pull request |
| `assurance/01-management/decisions/build_inbox.py` | The decision inbox page (published, not committed) | Built on every pull request |

Two checkers cover every Markdown file outside `hardware/` and the upstream README translations:
`assurance/tools/check_links.py` (every relative link resolves to a file or folder; anchors are not checked; `wiki/`
has its own check in the build) and `assurance/tools/check_tables.py` (every table row has as many cells as its
header). The full list of local checks is in [CONTRIBUTING.md](../../CONTRIBUTING.md#checks-to-run-locally).

## 4. Technical file

[WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) is the index from the Annex IV items of the
Machinery Regulation to the work products of [WP-M-00](../01-management/WP-M-00-work-product-register.md). It is
assembled at G5 from a frozen baseline: for each Annex IV item, the work product, its version and the baseline tag.
Items the standards define but the register covers elsewhere (risk assessment documentation, review and confirmation
records, gate records, impact records) are found through [WP-M-00 §4](../01-management/WP-M-00-work-product-register.md#4-work-products-the-standards-define-that-are-covered-elsewhere).
The tagged repository is the technical file's master copy; the form in which it is handed to an authority, and its
retention for the period the Machinery Regulation sets, are open (OI-4). WP-K-02 is still a skeleton.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Add a check that the Status in each header equals the register's status column | Configuration and change manager | G1 |
| OI-2 | Extend `check_links.py` to check `#anchor` targets in this repository | Configuration and change manager | G1 |
| OI-3 | Export pull requests, reviews and issues (held by GitHub, outside git) into the record at each frozen baseline | Configuration and change manager | First frozen baseline |
| OI-4 | Decide the delivery form and retention of the technical file (check the Machinery Regulation's retention period against the text) | Safety manager | G5 |
| OI-5 | Bring existing headers in line with §2.1 and §2.3 as each work product is next revised (Baseline written as `BL-001`, Approver wording after DQ-010) | Safety manager | G1 |
