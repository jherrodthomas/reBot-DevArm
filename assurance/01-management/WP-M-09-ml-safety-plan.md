# WP-M-09 Machine-learning safety plan

| Field | Value |
|---|---|
| Work product | WP-M-09 Machine-learning safety plan |
| Standard reference | Other: TR 5469 (AI technology classes, usage levels); AI Act Art. 9; ASPICE: MLE.1–4 |
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

How learned components (LeRobot imitation and reinforcement policies, the YOLO grasping demo, any vision-language-action model) are managed so that none carries a safety function, and what evidence the fork keeps about them under ISO/IEC TR 5469 and, if the threshold of WP-M-13 §5 is ever crossed, the AI Act.

## 2. Position

No safety function is allocated to a learned component (WP-M-01 T-03; decision DQ-008). Every learned output passes the same checker as any other command: joint limits, torque and speed caps, the watchdog. This plan keeps that true and documents it.

## 3. Classification under ISO/IEC TR 5469

Each learned component gets an AI technology class and a usage level; the target is usage outside the safety function, with the controller safety layer as the independent safeguard. Recorded in WP-C-09.

## 4. Activities by gate

G1 classification and requirements (WP-C-09) and the insufficiency analysis (WP-C-10); G3 ML engineering evidence (WP-W-10); G5 the AI Act record (WP-K-07).

## 5. Roles

| Role | Holder (today) | Duty |
|---|---|---|
| ML safety lead | Jherrod Thomas (acting); permanent holder TBD | Owns this plan and WP-C-09 |
| External ML reviewer | TBD (may be the FS assessor) | ML-R1…ML-R3 (WP-M-06 §7) |

## 6. Upstream

The LeRobot integration, the grasping demo and the policy checkpoints are upstream and community material; their quality varies per dataset (package open issue OI-06). The fork records which checkpoint ran in which test.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
