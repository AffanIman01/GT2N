# Open-source EDA route for this learning project

Recommendation: **start with KLayout for this GT2N cell**, then use
OpenROAD/OpenSTA to study the implementation/timing interface. For a separate
end-to-end custom-layout exercise with an established open tool setup, consider
Xschem + ngspice + Magic + Netgen using SKY130 or GF180MCU.

These are tool recommendations, not claims that a complete GT2N open-source
verification or simulation flow has been demonstrated here.

| Tool | Learning use | GT2N boundary in this exercise |
|---|---|---|
| [KLayout](https://www.klayout.de/doc/manual/index.html) | GDS inspection/editing, layer visibility and dimensions; also has programmable DRC/LVS engines | Open the supplied flavored GDS. The ICV `.rs` decks are not KLayout decks; a separately implemented, validated port would be required for equivalent verification. |
| [Xschem](https://xschem.sourceforge.io/) | Draw schematics and generate SPICE netlists | A way to redraw the two-device topology for study, with attribution. No ready GT2N Xschem symbols/device setup were verified; it is not an OA schematic importer for this exercise. |
| [ngspice](https://ngspice.sourceforge.io/docs.html) | DC/AC/transient circuit simulation | GT2N model compatibility must be established before using timing/current results. The supplied model card is not a tested drop-in here. |
| [Magic](https://github.com/RTimothyEdwards/magic) | Custom layout, DRC and extraction with a suitable technology setup | Useful for a separate SKY130/GF180MCU learning flow. This package supplies no GT2N Magic technology or extraction port. |
| [Netgen](https://github.com/RTimothyEdwards/netgen) | Compare extracted and schematic netlists for LVS | Requires compatible extracted devices and a PDK-specific setup; it does not execute ICV rules or extract GT2N GDS by itself. |
| [OpenROAD](https://openroad.readthedocs.io/en/latest/main/src/README.html) / [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA) | Digital placement/routing and static timing; connect LEF geometry with Liberty behavior | A collateral-import experiment is feasible to attempt. Complete routing, BSPDN and signoff compatibility remain untested here. |

## KLayout: the first practical session

1. Install KLayout from its official distribution for your OS. Record the version.
2. Open `gds/gt2_6t_std_cells_w31_lvt.gds` from this repository and select
   `gt2_6t_inv_x1_w31_lvt` in the cell hierarchy.
3. Use `techlib/gt2_techfile.layermap` as a reference for numeric layer/datatype
   pairs; it is a Synopsys map, not a ready KLayout `.lyp` display file.
4. Inspect ACT 2, GATE 3, DUMMY 4, GCUT 5, NSEL 6, PSEL 7, BPR 8, VBPR 9,
   SDCON 10, VSD 11, VG 12, M0 20, V0 22, M1 25 and prBoundary 235.
   Check drawing/pin/text purposes rather than combining all datatypes blindly.
5. Locate A, Y, vdd and vss; compare the LEF pin rectangles and the 0.084 ×
   0.144 µm boundary. Measure the boundary layer, not the extent of all shapes:
   power rails extend outside that footprint.
6. Capture your own annotated view and write three observations in the learning
   log. Credit the underlying layout to GT2N. Record this as **inspection**,
   not a DRC or LVS pass.

KLayout's [DRC](https://www.klayout.de/doc/manual/drc.html) and
[LVS](https://www.klayout.de/doc/manual/lvs_overview.html) manuals explain its
own rule language and device extraction. Reimplementing a few width/spacing
checks would be a separate educational experiment, not equivalent to the whole
ICV deck. It is intentionally outside this small example.

## LEF/LIB to OpenROAD: optional import experiment

The three views serve different purposes:

- `techlib/gt2_tech.lef`: routing layers, vias and technology constraints.
- `lef/tt/gt2_6t_w31_lvt.lef`: placement site, cell footprints, pins and obstacles.
- `lib/tt/gt2_6t_w31_lvt_tt_0p7v25c.lib`: Boolean function, timing/power tables
  and nominal TT, 0.7 V, 25 °C characterization context.

From the repository root, these are the documented OpenROAD read commands to
try interactively (not executed during package preparation):

```tcl
read_lef techlib/gt2_tech.lef
read_lef lef/tt/gt2_6t_w31_lvt.lef
read_liberty lib/tt/gt2_6t_w31_lvt_tt_0p7v25c.lib
```

Record parser warnings and the build before proceeding. Successful reads mean
only that the data loaded. A PnR flow additionally needs a linked design,
constraints, floorplan/rows, legal pin access, power connectivity, routing setup
and parasitic assumptions. Match the exact flavored cell names across views.
The upstream `Openroad_example/` archive is a further reference, but its contents
and execution have not been audited in this exercise.

BPR rails and backside connectivity deserve explicit validation; do not replace
them with arbitrary frontside rails and call the result equivalent. LEF/LIB
import is neither transistor-level LVS nor a complete BSPDN implementation.

## Simulation and a complete open learning stack

The supplied GT2N card uses `level=72`, `VERSION=111` and model names
`nmos`/`pmos`, while the CDL uses `nmos_lvt`/`pmos_lvt` and includes a
three-terminal variant. ngspice documents an
[OSDI/OpenVAF route for modern compact models](https://ngspice.sourceforge.io/extras.html),
including BSIM-CMG. That capability alone does not establish compatibility with
this particular model-card syntax, parameter version or terminal convention.
Model translation/mapping would need reference DC curves and regression checks;
do not merely rename the model or change the `level` and trust the result.

For practice completing schematic → simulation → custom layout → DRC → LVS,
use a separate SKY130 or GF180MCU project with the corresponding tool setup.
[Open PDKs](https://github.com/fossi-foundation/open-pdks) documents support for
these PDK families and tool-specific layouts such as `libs.tech/magic` and
`libs.tech/netgen`. Keep that project's rules/models separate from GT2N: useful
workflow skills transfer, but process dimensions and rules do not.

Official tool documentation linked here was consulted on 2026-09-30. Tool
versions were not pinned or installed for these optional GUI/EDA steps.
