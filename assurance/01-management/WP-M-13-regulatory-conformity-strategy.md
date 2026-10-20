# WP-M-13 Regulatory Conformity Strategy

| Field | Value |
|---|---|
| Work product | WP-M-13 Regulatory conformity strategy (Machinery Regulation, AI Act) |
| Standard reference | Regulation (EU) 2023/1230 (Machinery Regulation): Art. 3 (definitions, partly completed machinery, substantial modification), Art. 10 (obligations of manufacturers), Art. 20 (presumption of conformity), Art. 21 (EU declaration of conformity), Art. 25 (conformity assessment procedures), Annex I (high-risk categories), Annex III (essential health and safety requirements), Annex IV (technical documentation), Annex V (declaration), Annexes VI–X (modules A, B, C, H, G); Regulation (EU) 2024/1689 (AI Act): Art. 6 (classification), Art. 43 (conformity assessment), Annex I (Union harmonisation legislation), Annex IV (technical documentation); ANSI/A3 R15.06 (deferred, see §6) |
| Version | 0.1 (initial strategy; 2026-10-20) |
| Status | Draft |
| PL / scope | Regulatory (all) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); legal review TBD |
| Approver | Project maintainer (acting safety manager). Self-approval at I0 is proposed as a recorded interim limitation; it is decision DQ-010 (open, recommended A) |
| Baseline | `206ebda` |

> [!NOTE]
> This document is engineering planning, not legal advice. Article and annex numbers are quoted from the Official
> Journal texts as understood by the authors and must be checked by someone qualified before any declaration is
> drafted (OI-1).

## 1. Purpose

reBot-DevArm is machinery, and in the EU machinery is placed on the market under Regulation (EU) 2023/1230, which
applies from 20 January 2027 and replaces Directive 2006/42/EC. This document records which regulations apply to
the fork, which route to conformity is recommended, what the technical documentation must contain, and how the
assurance work products of [WP-M-00](WP-M-00-work-product-register.md) map onto it. The frame itself is decision
DQ-002 (EU recommended, open); the route is decision DQ-012 (queued, Module A recommended).

## 2. What the fork is, in regulatory terms

| Question | Position | Consequence |
|---|---|---|
| Is the fork a manufacturer? | Only if a fork build is placed on the market or put into service by the project. Today the fork is an assurance record for a kit arm operated on its own bench, which is "putting into service for own use" at most | The obligations of Art. 10 are planned for, not yet incurred; the hold point WP-V-07 governs own use |
| Is a bare arm "machinery" or "partly completed machinery"? | Arguably partly completed machinery (Art. 3): the kit as sold has no supply, no host and no safety function and cannot perform a specific application on its own. A fixtured arm with its supply, its host, its safety chain and a defined task put into service on a bench is machinery, and whoever puts it into service is its manufacturer | The fork plans the whole technical file for the arm as put into service, not a declaration of incorporation for the kit; the kit's own status is upstream's question |
| Is adding a safety chain a substantial modification? | The inherited arm was never CE-marked, so there is no conforming machine to modify; the resulting arm is new machinery | The fork plans the whole technical file, not a delta |
| Is any safety component a product in its own right? | The safety relay, the contactor, the E-stop devices and the enabling device are bought safety components with their own declarations; the fork integrates them. The actuators are not safety components (WP-M-01 T-05) | Their certificates are evidence in WP-H-07, not something the fork issues |
| Does Annex I Part A apply (mandatory third-party assessment)? | Part A lists safety components and machinery with "fully or partially self-evolving behaviour using machine learning approaches ensuring safety functions". The fork's strategy (WP-M-01 T-03; DQ-008 recommended A) allocates no safety function to a learned component, so Part A is **not triggered**. Part B lists other high-risk categories; none applies to a desktop arm as such | The fork may choose Module A if harmonised standards are applied in full (§3); the threshold is monitored in §5 |
| Does the licence allow the use? | Upstream's CC BY-NC-SA 4.0 forbids commercial use and upstream states that selling a rebranded arm is prohibited. A safety-assured arm put into service in a workplace (the package's OE-3) may be commercial use (GAP-35); use on a research bench (OE-1) is not | The first case covers OE-1 only (DQ-003); any later envelope records the licence question before the regulatory one |

## 3. Route to conformity

Art. 25 offers internal production control (Module A, Annex VI) where the machinery is not in Annex I and the
harmonised standards covering all the essential requirements are applied; otherwise EU type-examination plus
conformity to type (Modules B and C, Annexes VII and VIII), full quality assurance (Module H, Annex IX) or unit
verification (Module G, Annex X).

| Option | What it means for the fork | Cost | Recommendation |
|---|---|---|---|
| A: Module A, harmonised standards in full (ISO 10218-1, ISO 10218-2, ISO 13849-1, EN 60204-1, ISO 13850, ISO 13854, ISO 13857) | The fork self-declares against Annex III using the presumption of conformity of Art. 20. The technical documentation must still be complete and available for ten years | No notified body fee. The standards must be bought and applied in full; any deviation voids the presumption for that requirement | **Recommended**, conditional on DQ-004 option A (PL d stop functions) and on no collaborative claim beyond what ISO 10218-2 covers without measurement (DQ-005) |
| B: Module B + C, voluntary EU type-examination | A notified body examines the technical documentation and the type; gives an independent view the project otherwise lacks | Fee (indicative four to five figures); scheduling | Worth it only if a build is ever to leave the bench; the assessor engagement DQ-009 could be the same body |
| C: Module H | A certified quality system covering design and production | Out of proportion for a one-person open-source record of a kit | Not recommended |

The route is DQ-012 (queued behind DQ-002 and DQ-008). Until it is answered, NB-1 stays planned in WP-M-06 §8 and
the fork plans for self-declaration with the harmonised standards applied in full. The standards themselves are not
bought (DQ-011, queued) and no assessor is engaged (DQ-009, open), so "applied in full" rests on references marked
to be checked until that changes.

Whichever module is chosen, the harmonised standards are listed in the Official Journal under the Regulation only
once the Commission cites them; until then the standards give state of the art, not presumption. OI-2 tracks the
citation status of ISO 10218-1:2025, ISO 10218-2:2025 and ISO 13849-1:2023 under the new Regulation.

## 4. Technical documentation (Annex IV)

Annex IV requires, in summary: a general description; the complete drawings and the calculations, test results and
certificates needed to check conformity; the risk assessment documentation (the hazards identified, the essential
requirements that apply, the measures taken and the residual risks); the standards applied; technical reports with
test results; the instructions for use; the declaration of incorporation for any partly completed machinery; the
declaration of conformity; and, for machinery with self-evolving behaviour, the data and logs that describe it.

[WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) is the index. The mapping from Annex IV items to
work products:

| Annex IV item (summary) | Work products |
|---|---|
| General description, intended use, limits | WP-C-01, WP-C-02 |
| Drawings, circuit diagrams, calculations | WP-H-02, WP-H-04, WP-H-05, WP-H-08, WP-S-03, WP-S-04; upstream's STEP assembly and BOM under `hardware/` by reference |
| Risk assessment documentation | WP-C-03, WP-C-04, WP-C-05, WP-C-06, WP-C-10 |
| Standards and specifications applied | WP-M-00 (clause columns), WP-M-01 §4 |
| Technical reports and test results | WP-V-01…WP-V-05, WP-V-08, WP-S-09, WP-H-06, WP-W-06…W-08 |
| Certificates of safety components | WP-H-07 |
| Instructions for use | WP-O-01, WP-O-02, WP-O-03 |
| Software description, configuration, parameters | WP-W-03, WP-W-09, WP-P-01 (baselines) |
| Cybersecurity (Annex III §1.1.9 protection against corruption, §1.2.1 safety and reliability of control systems) | WP-C-07, WP-C-08, WP-S-07, WP-W-11, WP-V-06, WP-K-03 |
| Declaration of incorporation (if the kit is treated as partly completed machinery) | Upstream's, if any; recorded in WP-K-02, not issued by the fork |
| Declaration of conformity | WP-K-06 |
| Safety case (not required by the Regulation; the project's own argument) | WP-K-01 |

## 5. The AI Act threshold

Regulation (EU) 2024/1689 Art. 6(1) makes an AI system high-risk when it is a safety component of a product covered
by the Union harmonisation legislation listed in Annex I and that product must undergo third-party conformity
assessment. The Machinery Regulation is in Annex I Section A. The fork keeps learned components (the LeRobot
policies, the grasping demo, any vision-language-action model) outside every safety function (WP-M-01 T-03;
DQ-008 recommended A; [WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md)), so no AI
system is a safety component and the AI Act's high-risk obligations do not apply.
[WP-K-07](../10-safety-case/WP-K-07-ai-act-conformity-record.md) records that position with its evidence, and is
rewritten as a full Annex IV technical documentation if the position changes (for example, if a learned collision
predictor is ever used to trigger the protective stop, which DQ-008 option C would allow and this strategy does
not recommend). ML-R3 in [WP-M-06 §7](WP-M-06-confirmation-measures-plan.md#7-cybersecurity-and-ml-reviews) reviews
the record at G5.

## 6. Other markets

ANSI/A3 R15.06 (industrial robots and robot systems, US) and ANSI/A3 R15.806 (task-based risk assessment) are
deferred (DQ-002). R15.06 adopts the ISO 10218 text, so if a US deployment is added the plan is a cross-reference
table from the ISO 10218 and ISO 13849-1 requirements to R15.06 added to this document, with any additional tests
appended to WP-V-01, not a second technical file.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Have the article and annex references of this document checked against the Official Journal text by someone qualified | PM | G1 |
| OI-2 | Track the citation of ISO 10218-1:2025, ISO 10218-2:2025, ISO 13849-1:2023 and EN 60204-1:2018 as harmonised standards under Regulation (EU) 2023/1230; until cited, state "state of the art" rather than "presumption of conformity" everywhere | SM | G1 |
| OI-3 | Apply the lead's answers on the frame (DQ-002) and the module (DQ-012) to §1, §3 and WP-M-06 §8 | SM | G1 |
| OI-4 | Settle whether the kit as sold is partly completed machinery with upstream or a qualified adviser; record the answer in §2 | PM | G1 |
| OI-5 | Confirm with the lead that no fork build will be made available to anyone outside the project before G5, and that no envelope beyond OE-1 is used until the licence question of §2 is settled | PM | G0 |
