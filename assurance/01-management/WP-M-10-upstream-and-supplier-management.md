# WP-M-10 Upstream and Supplier Management

| Field | Value |
|---|---|
| Work product | WP-M-10 Upstream (Seeed Studio) and supplier (Damiao, RobStride) management |
| Standard reference | SRP/CS: 61508-1 §6.2 (subcontracted activities); IEC 62443: 62443-4-1 SM-9, SM-10; ASPICE: ACQ.4. Clause numbers are to be checked against licensed copies ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1) |
| Version | 0.1 (first draft: the hardware upstream and the three software upstreams with licence and pin, the fork's change policy per repository, what is asked of each supplier under DQ-019 B, evidence classes; 2026-11-01) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | BL-001 (`206ebda`) |

## 1. Purpose

How the fork takes changes from its upstreams (Seeed Studio for the hardware record, three repositories for the
software that moves the arm), what it asks of the component suppliers (Damiao and RobStride for the actuators,
MEAN WELL for the supply, the makers of the CAN-USB adapter and of the safety components), and how a supplier's data
enters the record. None of these parties is under contract with the fork and none has a development interface
agreement with it; the supplier-side activities fall to the fork (tailoring T-08,
[WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring)). The fork is not affiliated with or endorsed by Seeed Studio
or any supplier and never implies otherwise.

## 2. Upstream

### 2.1 The hardware record (Seeed Studio)

| Item | Rule |
|---|---|
| Source | `Seeed-Projects/reBot-DevArm`, CC BY-NC-SA 4.0 (non-commercial); hardware v1.1 of 2026-04-25 at BL-001 (`206ebda`) |
| `hardware/` | Upstream's record. Updated only by merging from upstream, never edited here; an SR-Q path in [`safety-relevant-paths.txt`](../07-supporting/safety-relevant-paths.txt) |
| `README.md` | The fork's own page; on an upstream merge the fork's README is kept and links to upstream for the arm's documentation. The translated READMEs are upstream's |
| Licence | Kept for the whole repository, including the record. Whether a safety-assured build in a workplace is commercial use is open (GAP-35; [WP-M-13 §2](WP-M-13-regulatory-conformity-strategy.md#2-what-the-fork-is-in-regulatory-terms)) |
| Merge procedure | Fetch upstream; diff `hardware/` and the upstream READMEs against the last merged commit; write an impact record ([WP-M-11 §5](WP-M-11-impact-analysis.md#5-change-impact-analysis-records)) naming the elements, hazards and work products touched; merge by pull request; update the baseline record |
| What triggers a merge | A new hardware version or BOM change for the B601-DM; the release of the B601-RS BOM, which also opens the CFG-002 impact analysis (DQ-017, answered A); a correction to the performance test |
| Upstream's statements | The README, wiki, assembly video and thermal test are inputs; the thermal test is supporting evidence only (T-06). The XIAO ESP32 wireless stop mentioned upstream is not accepted as a stop ([WP-V-07 §3](../06-validation/WP-V-07-test-operations.md#3-limits-during-development-testing)) |

### 2.2 The software that moves the arm

Research on 2026-11-01 found that the stack is three upstream repositories, not the two the fork question named. The
lead chose to fork all three into the `jherrodthomas` GitHub account and pin them in BL-001 (DQ-007, answered A).
The forks are being created by the lead and are not yet confirmed (OI-1).

| Repository | What it is | Licence as found | Upstream HEAD recorded 2026-11-01 | Fork policy |
|---|---|---|---|---|
| [`motorbridge/motorbridge`](https://github.com/motorbridge/motorbridge) | CAN motor-control stack: Rust core, C ABI, Python and C++ bindings; drivers for Damiao, RobStride and other actuators. Installed upstream as the PyPI package `motorbridge` (0.5.6) | MIT | `d5700bcd5b7f9355dd2012488d463c3bac982259` (`main`) | **Fork, pin and change.** MIT permits modification and redistribution with the notice kept. The host-side hardening (authenticated session, mirrored bounds) is made here |
| [`Seeed-Projects/reBotArm_control_py`](https://github.com/Seeed-Projects/reBotArm_control_py) | Arm control library: the `RebotArm` class, Pinocchio kinematics and dynamics, gravity compensation, on top of motorbridge | **None** (no licence file) | `d4f3591bc0183de03f3ae8651298db0269aadfdd` | **Fork and pin; do not modify.** Without a licence there is no right to modify or redistribute, only GitHub's fork right. An issue asks the authors to state a licence |
| [`Yang-Ci/ReBot_Arm_DigitalTwin_DM`](https://github.com/Yang-Ci/ReBot_Arm_DigitalTwin_DM) | Community ROS 2 driver and digital twin for the B601-DM: ROS 2, MoveIt 2, MuJoCo, web control, agents; referenced by Seeed's wiki | **Ambiguous:** the LICENSE file is CERN-OHL-W-2.0 (a hardware licence); the README says the software follows Apache-2.0 | `7456d8bc3cc6d9c470680988543f90bc8f3b03b0` | **Fork and pin; do not modify.** An issue asks the author which licence governs the software |

Not chosen: `EclipseaHime017/reBotArmController_ROS2`, a second community ROS 2 driver with no licence. The
upstream README translations at BL-001 link the control library at `vectorBH6/reBotArm_control_py`; which of the two
is canonical is recorded in OI-5.

Rules for all three:

1. **Pinned, never floating.** The fork release names each repository by fork URL and commit; nothing is installed
   from a branch or a package index at an unrecorded version ([WP-M-08 §3](WP-M-08-cybersecurity-plan.md#3-practices-of-iec-62443-4-1-and-where-each-lands)).
2. **Upstream changes by merge only**, each with an impact record; an upstream release is not taken automatically.
3. **The two unlicensed repositories are not modified** until their authors state a licence that permits it. Any
   safety measure that would need a change there is placed in motorbridge or on the controller safety layer instead,
   which runs on a dedicated controller between the host and the motor bus (DQ-020, answered A) and is the fork's
   own code. If a licence is refused or never stated, the fork records the repository as used as found, unmodified,
   and revisits DQ-007 with the lead if a change there becomes necessary.
4. **No safety function depends on any of the three** (T-04); they are hardened as defence in depth and qualified as
   components in [WP-P-08](../07-supporting/WP-P-08-software-component-qualification.md).
5. **Defects found upstream** are reported to the upstream owner; a security defect is routed privately, per
   [SECURITY.md](../../SECURITY.md).

The other software the arm uses (ROS 2 Humble, MoveIt 2, Pinocchio, LeRobot, the YOLO demo, the hosted web UI) is
not forked; it is pinned by version and listed in WP-P-08.

## 3. Suppliers

The lead decided not to request reliability data (MTTFD, B10D) from Damiao or RobStride (DQ-019, answered B): only
ISO 13849-1's generic values are used for the actuators where they appear at all, and the actuators are a channel of
no PL d function, because the chain of [WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md)
removes their power by contactor. Datasheets and fault-behaviour information are still wanted, from published
documentation first and by a technical question to the supplier where it is silent.

| Supplier and part | Configuration | What the record needs | Used in |
|---|---|---|---|
| Damiao DM4310 and DM4340P (V4), and the gripper actuator | CFG-001, the B601-DM v1.1 (DQ-001, answered A) | Datasheet: rated and peak torque, speed and current; whether logic and power share one 24 V input (WP-H-02 OI-2); firmware version and how to read it; behaviour on over-temperature, undervoltage, power return and loss of CAN traffic (does the drive hold its last command, GAP-18); holding and back-driving without power (GAP-07, SF-13); wake-up by back-EMF when moved by hand (WP-H-02 OI-6) | WP-C-01 OI-4, WP-H-02, WP-H-07, WP-W-09 |
| DM CAN-USB adapter | CFG-001 | Datasheet, firmware version, behaviour on USB loss | WP-S-05, WP-S-07 |
| RobStride actuators (models unknown) | CFG-002, tracked, every value unverified until its BOM is released (DQ-017, answered A) | The same list as for Damiao, requested only once the RS BOM names the models | WP-C-01 §1.2 |
| MEAN WELL LRS-350-24 | Both | Datasheet: output protections, inrush, hold-up time, approvals | WP-H-05 |
| Safety relay, contactors, E-stop devices, interlock relay, disconnect | The bench chain (DQ-006, answered A) | Certificates or declarations with PL, category, PFHD or B10D, conditions of use; bought with them (T-05) | WP-H-04, WP-H-07 |

## 4. Supplier evidence

A supplier's statement enters the record as an evidence item of one of these classes, stored or referenced under
[WP-H-07](../04-hardware/WP-H-07-safety-component-qualification.md):

| Class | What it is | What it may support |
|---|---|---|
| S-1 Certificate | A third-party certificate (type examination, functional-safety certificate) with its scope | A PL calculation and a qualification claim, within the certificate's conditions |
| S-2 Manufacturer declaration or datasheet | A dated, versioned document from the maker | A design value with its source; a reliability figure only for bought safety components |
| S-3 Informal statement | A wiki page, forum post, e-mail reply or video | An assumption to be confirmed; never a design value on its own |
| S-4 Fork measurement | A test the fork ran on its own parts, with a record under `06-validation/` | A design value for the configuration tested |

Each item records the supplier, document title and revision, date retrieved, URL and a checksum of the retrieved
copy. Where the document's licence does not allow redistribution, the record keeps the reference and checksum, not
the file. A value with no source of class S-1, S-2 or S-4 is marked unverified wherever it is used.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Confirm the three forks exist under `jherrodthomas`; record their URLs and the pinned commits in BL-001 (`assurance/case/baselines/baselines.yaml`, owned by WP-P-01) | Project maintainer | G0 |
| OI-2 | Raise an issue on `Seeed-Projects/reBotArm_control_py` asking the authors to state a licence; record the answer here | Project maintainer | G0 (raise); answer when given |
| OI-3 | Raise an issue on `Yang-Ci/ReBot_Arm_DigitalTwin_DM` asking which licence governs the software; record the answer here | Project maintainer | G0 (raise); answer when given |
| OI-4 | Request a change to `safety-relevant-paths.txt` (WP-P-01, WP-P-02) so its fork entries name the three forks instead of the two assumed ones | Configuration and change manager | G0 |
| OI-5 | Establish whether `Seeed-Projects/reBotArm_control_py` or `vectorBH6/reBotArm_control_py` (linked by the upstream README translations) is canonical, and pin the other's relation | Project maintainer | G0 |
| OI-6 | Collect the Damiao DM4310 and DM4340P datasheets and fault-behaviour information of §3 as S-2 items; ask Damiao where they are silent | Electrical and mechanical engineer | Before the chain purchase (WP-H-02 OI-2) |
| OI-7 | Choose the licence of the fork's own new code (the controller safety layer) | Project maintainer | G2 |
