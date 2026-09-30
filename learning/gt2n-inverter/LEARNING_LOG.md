# Affan Iman — GT2N inverter learning log

Focus: understanding an existing public advanced-node cell and reproducing
verifiable results. Original design credit remains with the GT2N authors.

## 2026-09-30 — exercise prepared with AI assistance

| Activity | Evidence and honest status |
|---|---|
| Selected one public inverter and pinned the sources | Complete — assistant prepared `sources.json` and attribution |
| Traced CDL pull-up/pull-down connectivity; related W/L to nanosheet/node naming | Study notes prepared by assistant; Affan's review pending |
| Compared LEF pins/area with Liberty and GDS labels | Assistant reproduced `study.py check`; see `evidence/source-check.json` |
| Prepared isolated OA and ICV inputs | Assistant exercised `study.py prepare`; generated files remain ignored |
| Personally imported the cell in Custom Compiler or opened it in KLayout | Not yet confirmed by Affan |
| Personally ran ICV DRC/LVS, simulation or OpenROAD | Not yet confirmed; no EDA result claimed |

The assistant's execution is not evidence that I personally performed the GUI
or verification steps. Replace pending entries only after doing the work and
adding the actual evidence.

## My next reproduction entry

- Date and tool/build: **pending**
- Source baseline/hash check: **pending**
- What I personally did: **pending**
- What I observed (layers, pins, device dimensions, rail access): **pending**
- What I can explain in my own words: **pending**
- Result and evidence path (include failed/blocked runs): **pending**
- Remaining question / next experiment: **pending**

Useful review questions: Why is a “2 nm” model used with a 14 nm CDL L? Why
does this `6t` inverter have two devices? What is missing from a LEF abstract?
Why is passing a source check different from passing LVS? What does ignoring
bulk comparison prevent me from claiming?

## Portfolio wording after personal reproduction

Use only once supported by my own evidence:

> Studied and reproduced a single-cell layout exercise using the open-source
> GT2N PDK by the GT2N authors, tracing inverter connectivity and comparing
> GDS/CDL/LEF/Liberty views. My contribution was the documented learning
> exercise and reproducibility checks, prepared with AI assistance.

Add specific DRC/LVS or simulation outcomes only after running and recording
them. Do not describe this work as designing a 2 nm PDK, an original GT2N
standard cell, a tapeout, or employer project experience.
