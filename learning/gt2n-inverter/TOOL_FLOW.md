# Import and verification exercise

These steps adapt the pinned upstream [README](../../README.md),
[technology files](../../techlib) and [ICV runsets](../../icv_runset).
They are a prepared procedure, not evidence of completed GUI or ICV runs.
Commercial tools require a separately available installation and license.

## 1. Prepare and import in Custom Compiler

Run `python3 learning/gt2n-inverter/study.py prepare` from the repository root.
The generated `work/cc/lib.defs` maps:

| Library | Generated content |
|---|---|
| `gt2_official` | Copies of upstream `nmos_lvt` and `pmos_lvt` |
| `gt2_std_cells` | Copy of upstream `gt2_6t_inv_x1`, including its views |

Launch Custom Compiler from `learning/gt2n-inverter/work/cc/` so it reads that
`lib.defs`. The file uses OA `DEFINE` entries. Preserve any site-required
library definitions in this isolated workspace. Keep the name `gt2_official`
because the upstream schematics reference it.

In Technology Manager, import `techlib/gt2_techfile.tf` from the repository and
apply it to `gt2_official`; attach that technology to `gt2_std_cells` as described
upstream. In Display Resource Manager, load `techlib/gt2_layer_colors.tcl`.
Open `gt2_6t_inv_x1` schematic/layout/abstract. Check unresolved device masters,
technology attachment, visible layers, pin names and device properties. This
exercise copies only one standard cell; if a tool reports additional required
masters, identify them and their upstream paths before adding them.

For GDS import, create a **separate scratch library**, attach the same technology,
and import `gds/gt2_6t_std_cells_w31_lvt.gds` using
`techlib/gt2_techfile.layermap`. Select `gt2_6t_inv_x1_w31_lvt`.
Keep drawing, pin and label purposes: the mapping includes drawing datatype 0,
label 20 and pin 251 for many layers. Record the tool build and import settings.
Compare OA and GDS only after checking naming, flavor and parameters; no
equivalence between their database contents was established during preparation.

## 2. DRC baseline

`work/icv/drc/` contains the original flavored GDS, a copy of the complete
upstream DRC deck, and its `Include/` directory. The only main-deck adaptation
is a `library(...)` input declaration for the chosen top and `input.gds`.
Copyright notices and rule bodies are retained.

In a shell configured for your installed ICV version, start from that directory.
The conventional runset invocation to check against your local ICV help is:

```bash
cd learning/gt2n-inverter/work/icv/drc
icv gt2_main.drc.rs
```

This command has **not** been executed here. Add installation-required options
according to the licensed tool's local documentation, or select the generated
deck in the Custom Compiler ICV interface. Record the exact command/settings.
Do not confuse a deck compile/input error with a physical DRC violation.

Inspect the full run summary, top-cell selection and executed rule scope.
Record counts by rule and open representative markers. Relevant include files
cover ACT, GATE, GCUT, DUMMY, BPR/VBPR, SDCON/VSD and M0/M1/vias. Do not assume
that the existence of layer definitions means all chip-level reliability or
backside-network checks are implemented. Investigate boundary-context markers
before adding waivers or altering geometry.

## 3. LVS baseline

`work/icv/lvs/` contains the same flavored GDS and a single-cell `source.cdl`
extracted verbatim with its full upstream license header. A copied LVS deck
substitutes exactly three input placeholders: top `cell`, GDS `inlib`, and
schematic `sch`. Device extraction/comparison rules are unchanged.

```bash
cd learning/gt2n-inverter/work/icv/lvs
icv gt2_main.lvs.rs
```

As with DRC, verify invocation/options against the installed version. The
upstream three-terminal CDL is the starting input for this prepared flow; its
acceptance by a specific ICV SPICE reader has **not** been tested here. If the
reader needs the supplied `cdl/with4nodes/gt2_6t_w31_lvt.cdl` variant, select the
same cell, retain its notice and record the input change. Do not rewrite devices
or disable comparison checks just to obtain a pass.

Inspect recognized PMOS/NMOS counts, model/flavor names, W/L, four top ports,
shorts and opens. The reference has one PMOS and one NMOS; the deck can merge
parallel devices, so read the comparison report as well as raw extraction counts.
It checks W/L and treats some port-name differences as warnings. Review warnings
even when connectivity matches. Bulk pins are explicitly ignored by these
recognition declarations, limiting what an LVS match establishes.

The model card is for circuit simulation; do not blindly include it as an LVS
reference. Its `.MODEL` names are `nmos`/`pmos`, whereas the CDL uses
`nmos_lvt`/`pmos_lvt`. Simulation needs deliberate model mapping and compatible
compact-model support; it is outside this executed exercise.

## 4. Record a defensible result

Keep all generated tool databases/reports in ignored `work/`. For a personal
reproduction, add only a reviewed summary to the learning log with:

- Date, source commit and input SHA-256 values; tool name/build and command.
- Import outcome and actual layout top; DRC rule/count summary and completion status.
- LVS match/mismatch, compared device/property/port summary, and warning disposition.
- An attributable screenshot or report excerpt from this **public GT2N exercise**.

If a run is blocked, record the exact stage and diagnostic. Leave its result
“not run” or “failed”; the supplied Python report cannot substitute for ICV.
Only after baseline closure consider a separate scratch variant, such as a pin
access change, and repeat the same checks before discussing its effect.
