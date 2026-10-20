# Documentation

This repository holds upstream Seeed Studio's hardware record for the reBot Arm B601-DM, the fork's concept-phase
engineering package, and the engineering assurance record the fork adds around them. The software that moves the
arm lives in upstream repositories until the lead decides to fork it (DQ-007); upstream's documentation stays
where upstream keeps it.

| If you want to | Read |
|---|---|
| Understand the safety architecture argument | [Architecture](architecture.md) |
| Browse every work product, with its gate and status | [Assurance record](../assurance/README.md) |
| See what the inherited arm and the package lack, finding by finding | [Gap assessment](../assurance/00-assessment/gap-assessment.md) |
| Read upstream's hardware record (BOM, STEP, the thermal test) | [`hardware/reBot_B601_DM/`](../hardware/reBot_B601_DM/readme.md), never edited here |
| Get oriented: processes, process maps, standards, glossary | [Wiki](https://github.com/jherrodthomas/reBot-DevArm/wiki), kept in [`wiki/`](../wiki/README.md) and mirrored on merge |
| Contribute | [Contributing](../CONTRIBUTING.md) |
| Report a vulnerability | [Security policy](../SECURITY.md) |

Every figure is generated and checked by CI; nothing in them is drawn by hand:

| Figures | Generator |
|---|---|
| README and wiki figures under [`assets/rebot/`](assets/rebot/): hero, standards, architecture, roadmap, lifecycle, status card, standards map, repository map | [`make_assets.py`](assets/rebot/make_assets.py) |
| Process swimlanes, lifecycle grid and interface figure under [`assets/rebot/process/`](assets/rebot/process/) | [`process_figures.py`](../assurance/process/tools/process_figures.py), from the process model |
| Living Safety Case dashboard and lifecycle areas under [`assets/assurance/`](assets/assurance/) | [`generate_dashboard.py`](../assurance/case/tools/generate_dashboard.py), from the case records |
