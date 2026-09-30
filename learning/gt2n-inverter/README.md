# GT2N inverter: an attributed layout learning exercise

**Learner: Affan Iman. Scope: study and reproduce checks on an existing public
GT2N standard cell.** The PDK, device models, standard-cell design and physical
verification rules are the work of the upstream GT2N authors, not mine.
This learning package was prepared with AI assistance. See
[attribution and pinned sources](ATTRIBUTION.md) and the
[learning log](LEARNING_LOG.md), which separates assistant-run evidence from
personal work still to be completed.

No employer schematics, layouts, screenshots, rule decks, scripts or measurements
are inputs to this exercise. Everything studied comes from this public repository.

## Goal and current evidence

Trace one inverter through transistor connectivity, physical layout, abstract
pins, and timing-library metadata; then prepare a repeatable Custom Compiler and
IC Validator (ICV) exercise. This supports skills in pin/layer mapping, device
recognition, connectivity debugging and verification evidence.

| Item | Status |
|---|---|
| Source hashes, two-device topology and ideal static truth table | Reproduced by the assistant; [machine-readable result](evidence/source-check.json) |
| LEF/LIB cell area, pins and Boolean function | Cross-checked by the assistant |
| GDS structure name, layer inventory and four text labels | Read directly from the supplied GDS; no geometry extraction |
| Isolated OA and ICV workspace generation | Exercised; upstream source files remain unchanged |
| Custom Compiler import, ICV DRC/LVS, simulation, OpenROAD | **Not run**; tools/licenses unavailable in the preparation environment |
| Affan's personal hands-on reproduction | Pending; record evidence in the learning log |

Passing the Python checks means collateral consistency for this pinned example.
It does **not** mean DRC clean, LVS matched, timing validated or silicon proven.

## Start in under five minutes

Prerequisites for the reproducible checks: Git and Python 3.9 or newer. No Python
packages or commercial EDA license are required.

```bash
git clone --branch learning/gt2n-inverter-study https://github.com/AffanIman01/GT2N.git
cd GT2N
python3 learning/gt2n-inverter/study.py check
python3 learning/gt2n-inverter/study.py prepare
```

`check` exits nonzero on missing/changed source inputs or inconsistent expected
collateral. It verifies SHA-256 hashes rather than requiring HEAD to remain at
the baseline commit, so the learning branch can contain this new documentation.
The source baseline is `699e2c10b2b494a120745515f59df8815f4f0175`.

`prepare` creates ignored `learning/gt2n-inverter/work/` with a single-cell OA
library, device library, and separate DRC/LVS directories. It refuses to overwrite
an existing workspace: rename the old `work/` to keep previous results before
repeating. No EDA command is automatically executed.

To compare a fresh check with the committed evidence:

```bash
python3 learning/gt2n-inverter/study.py check > /tmp/gt2n-inverter-check.json
diff -u learning/gt2n-inverter/evidence/source-check.json /tmp/gt2n-inverter-check.json
```

## One cell, several names and views

| View | Exact path/name in the pinned source |
|---|---|
| OA cell | `std_cells/gt2_6t_inv_x1/{schematic,layout,abstract}` |
| GDS file | `gds/gt2_6t_std_cells_w31_lvt.gds` |
| GDS/CDL/LEF/LIB cell | `gt2_6t_inv_x1_w31_lvt` |
| Three-terminal device CDL | `cdl/gt2_6t_w31_lvt.cdl` |
| Four-terminal variant | `cdl/with4nodes/gt2_6t_w31_lvt.cdl` |
| Cell abstract | `lef/tt/gt2_6t_w31_lvt.lef` |
| Timing library | `lib/tt/gt2_6t_w31_lvt_tt_0p7v25c.lib` |
| Device model | `device/tt/gt2_w31_lvt_tt.sp` |

The README's generic `gds/gt2_6t_std_cells.gds` is absent at this revision; use
the existing flavored filename above. OA names omit the width/VT suffix: do not
silently assume an OA export and a flavored CDL have the same top-cell name.
The generated ICV exercise deliberately pairs the flavored upstream GDS and CDL.
An OA-export comparison is a separate follow-up requiring explicit name and
device-parameter reconciliation.

## Device and layout structure

The upstream README describes three stacked nanosheets and a 2 nm GAAFET/BSPDN
PDK. Here `w31` selects the 31 nm sheet-width flavor and `lvt` the low-threshold
flavor. The CDL records `W=0.031u`, `L=0.014u`, `M=1` for both devices.
**The node label “2 nm” is not the drawn gate length:** this cell's CDL length
is 14 nm. Likewise, CDL W is not a claim about a planar MOS effective width;
interpret it with the PDK's stacked-sheet model convention.

| Device | Model | Drain | Gate | Source | Function |
|---|---|---|---|---|---|
| MM0 | `pmos_lvt` | Y | A | vdd | Pull Y high when A is low |
| MM1 | `nmos_lvt` | Y | A | vss | Pull Y low when A is high |

These connections give `Y = NOT A`. The script evaluates an ideal two-state
switch model from the CDL and checks the Liberty function `(!A)`; it does not
evaluate analog voltage transfer, leakage, rise/fall time or parasitics.
The four-terminal CDL additionally ties PMOS bulk to vdd and NMOS bulk to vss.
The supplied LVS recognition declarations ignore bulk in the comparison; this
does not establish body-bias or substrate reliability correctness.

The LEF footprint is **0.084 × 0.144 µm**, giving **0.012096 µm²**, equal to
the Liberty area number. It occupies two 0.042 µm-wide `gt2_6t` placement sites.
The 0.144 µm height is six times the tech LEF's 0.024 µm M0 pitch, consistent
with the `6t` library naming. Track count is not transistor count: this inverter
has two CDL devices.

| Geometry to inspect | Evidence / interpretation |
|---|---|
| `ACT`, `GATE`, `NSEL`, `PSEL`, `NWELL` | The LVS deck derives PMOS/NMOS recognition regions from these layers. A GDS polygon is a 2D process representation, not a literal 3D sheet cross-section. |
| `DUMMY`, `GCUT` | Excluded/cut in the LVS gate derivation; inspect termination at the cell edges before reasoning about active devices. |
| `VG`, `M0`, `V0`, `M1` | Gate-to-local-metal and local-to-signal-metal connections in the LVS deck; A and Y access pins are on M1 in LEF. |
| `SDCON`, `VSD`, `VBPR`, `BPR` | Source/drain contact connects toward M0 through VSD and toward buried power rails through VBPR. LEF vdd/vss ports are on BPR. |
| Backside metal network | The LVS deck includes BM/BV layers. Presence in the deck does not mean a single isolated inverter contains a complete chip power network. |

The direct GDS inventory finds layers 1–12, 20, 22, 25 and 235, and the labels
A, Y, vdd, vss for this cell. Consult `techlib/gt2_techfile.layermap` to interpret
layer/purpose pairs; a numeric layer inventory alone proves no electrical path.

![Original GT2N inverter layout thumbnail](../../std_cells/gt2_6t_inv_x1/layout/snapshot.png)

*Original upstream GT2N thumbnail, not a screenshot of Affan's reproduction.
Its resolution is limited; inspect the actual GDS/OA for measurements.*

## Layout observations to practice

1. Trace A to both gates and Y to both drains. Inspect labels, contact/via paths
   and pin purposes, then compare the extracted netlist when ICV is available.
2. Inspect the LEF power rails: vdd spans y = 0.128…0.160 µm and vss spans
   y = −0.016…0.016 µm. They extend beyond the nominal 0…0.144 µm footprint.
   This suggests rail sharing/abutment intent; do not “fix” the overhang merely
   because it exceeds the bounding box. Verify row orientation and neighbor
   compatibility in a separate abutment test.
3. Examine the three M0 obstruction rectangles in LEF. An abstract protects
   internal routing from the placer/router; it does not expose the complete
   transistor geometry.
4. The PMOS and NMOS are complementary devices, not an analog matched pair.
   Equal W/L does not establish equal current or equal rise/fall delay.
   Common-centroid/interdigitation is not a justified requirement for this
   two-device cell. Practice consistent device environment, edge treatment,
   access resistance and parasitic awareness instead.
5. Separate what is observed from what is inferred. Connectivity extraction,
   timing and EM/IR require their own runs; no improvement is claimed here.

Continue with [Custom Compiler and ICV](TOOL_FLOW.md), or use the
[open-source EDA route](OPEN_SOURCE_EDA.md) for license-free exploration.
