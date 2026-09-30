# Attribution and provenance

## Ownership

Original PDK and standard cells:
[azadnaeemi/GT2N](https://github.com/azadnaeemi/GT2N).
This repository, [AffanIman01/GT2N](https://github.com/AffanIman01/GT2N), is a
fork. The upstream cell remains named `gt2_6t_inv_x1_w31_lvt` throughout this
study. No PDK, device model, standard-cell design or rule-deck authorship is
claimed by Affan Iman.

The root [LICENSE](../../LICENSE) is BSD-3-Clause, copyright 2025 azadnaeemi.
File-specific notices additionally name contributors, including Piyush Kumar,
Dongwon Jang, Da Eun Shim, Akshata Ashoka, Meghana Mallikarjuna, Nahid Shazon,
Azad Naeemi and/or Georgia Institute of Technology, depending on the file.
The exact notices in each original file govern that file and are preserved.
This learning package does not imply endorsement by those authors.

The new contribution is limited to the educational walkthrough, source-audit
and workspace-preparation Python helper, pinned manifest and learning-log
structure. These were prepared for Affan Iman with AI assistance. The Python
helper uses only the standard library; no upstream geometry is redrawn or
rebranded. Copies generated in ignored `work/` retain upstream notices. The
repository's existing license is unchanged.

## Requested upstream citation

As stated in the pinned upstream README:

D. Jang, P. Kumar, M. N. H. Shazon, S. J. Ram, A. Svizhenko, V. Moroz,
A. Ceyhan, N. A. Radhakrishn, and A. Naeemi,
“GT2N: An Open-Source 2nm Nanosheet PDK Enabling Multi-Width/VT Benchmarking,”
IEEE International Symposium on Circuits and Systems (ISCAS), 2026.
[Publication link provided by upstream](https://ieeexplore.ieee.org/document/11562058).

This citation is transcribed from the README; this exercise does not claim to
have independently reviewed the paper's full text or reproduced its benchmarks.

## Pinned technical sources

Baseline: `699e2c10b2b494a120745515f59df8815f4f0175`, the fork's `main` when
this exercise was prepared on 2026-09-30 (Asia/Kuala_Lumpur). Newer upstream
changes are deliberately outside this baseline. [sources.json](sources.json)
records SHA-256 hashes for every source file directly used by this package,
including device/OA files and DRC includes.

| Claims or procedure | Pinned primary source |
|---|---|
| 2 nm, three-sheet devices, 72 cells, setup and citation | [README](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/README.md) |
| Device connectivity, W/L/M and terminal order | [CDL](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/cdl/gt2_6t_w31_lvt.cdl) |
| Body-terminal variant | [Four-node CDL](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/cdl/with4nodes/gt2_6t_w31_lvt.cdl) |
| Site/footprint, pin rectangles and obstructions | [LEF](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/lef/tt/gt2_6t_w31_lvt.lef) |
| Boolean function, area, nominal 0.7 V / 25 °C | [Liberty](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/lib/tt/gt2_6t_w31_lvt_tt_0p7v25c.lib) |
| GDS cell inventory and labels | [Flavored GDS](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/gds/gt2_6t_std_cells_w31_lvt.gds) |
| Drawing/pin/label mapping | [Layer map](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/techlib/gt2_techfile.layermap) |
| M0 pitch and routing layers | [Tech LEF](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/techlib/gt2_tech.lef) |
| DRC scope/includes | [DRC deck](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/icv_runset/gt2_main.drc.rs) |
| Connectivity, device recognition and comparison policy | [LVS deck](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/icv_runset/gt2_main.lvs.rs) |
| Model names and compact-model settings | [Model card](https://github.com/azadnaeemi/GT2N/blob/699e2c10b2b494a120745515f59df8815f4f0175/device/tt/gt2_w31_lvt_tt.sp) |

Geometry interpretations and suggested exercises are educational inferences,
identified as such in the walkthrough, rather than upstream validation claims.
