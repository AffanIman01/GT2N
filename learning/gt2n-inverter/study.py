#!/usr/bin/env python3
"""Small, pinned GT2N inverter collateral study; Python 3.9+, stdlib only.

This is a source audit and workspace preparer, NOT a DRC/LVS or SPICE engine.
Learning helper prepared for Affan Iman with AI assistance; upstream cells,
models and rules remain the work of the GT2N authors. See ATTRIBUTION.md.
"""
import argparse
import hashlib
import json
import re
import shutil
import struct
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = json.loads((HERE / "sources.json").read_text())
CELL = MANIFEST["cell"]
CDL = "cdl/gt2_6t_w31_lvt.cdl"
LEF = "lef/tt/gt2_6t_w31_lvt.lef"
LIB = "lib/tt/gt2_6t_w31_lvt_tt_0p7v25c.lib"
GDS = "gds/gt2_6t_std_cells_w31_lvt.gds"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source(path):
    return (ROOT / path).read_text()


def section(text, start, end):
    match = re.search(start + r"(.*?)" + end, text, re.S | re.M)
    require(match is not None, "Missing section: " + start)
    return match.group(0)


def liberty_group(text, kind, name):
    # Scoped brace matching for this pinned Liberty file, not a general parser.
    match = re.search(r"\b" + kind + r"\s*\(\s*" + re.escape(name) + r"\s*\)\s*\{", text)
    require(match is not None, f"Missing {kind}({name})")
    depth = 1
    for i in range(match.end(), len(text)):
        depth += (text[i] == "{") - (text[i] == "}")
        if depth == 0:
            return text[match.end():i]
    raise ValueError("Unbalanced Liberty group")


def cdl_cell(path=CDL):
    return section(source(path), r"^\.subckt " + CELL + r"\s", r"^\.ends " + CELL + r"\s*$")


def gds_inventory(data):
    """Read cell names, layer IDs and text only; no geometry extraction/LVS.

    Stop at ENDLIB so legal zero padding is not interpreted as records.
    """
    offset, current = 0, None
    names, layers, labels, references = [], set(), [], []
    while offset + 4 <= len(data):
        size, kind, _ = struct.unpack(">HBB", data[offset:offset + 4])
        require(size >= 4 and size % 2 == 0 and offset + size <= len(data), "Malformed GDS record")
        value = data[offset + 4:offset + size]
        offset += size
        if kind == 4:  # ENDLIB
            return names, sorted(layers), sorted(labels), sorted(references)
        if kind == 6:  # STRNAME
            current = value.rstrip(b"\0").decode("ascii")
            names.append(current)
        elif kind == 7:  # ENDSTR
            current = None
        elif current == CELL:
            if kind == 13:  # LAYER
                layers.add(struct.unpack(">h", value)[0])
            elif kind == 25:  # STRING
                labels.append(value.rstrip(b"\0").decode("ascii"))
            elif kind == 18:  # SNAME
                references.append(value.rstrip(b"\0").decode("ascii"))
    raise ValueError("GDS ENDLIB missing")


def audit():
    for path, expected in MANIFEST["sha256"].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
                "Source changed or wrong checkout: " + path)
    cdl = cdl_cell()
    require(cdl.splitlines()[0].split()[2:] == ["A", "Y", "vdd", "vss"], "CDL port order")
    devices = [line.split() for line in cdl.splitlines() if line.startswith("MM")]
    require(devices == [
        ["MM0", "Y", "A", "vdd", "pmos_lvt", "W=0.031u", "L=0.014u", "M=1"],
        ["MM1", "Y", "A", "vss", "nmos_lvt", "W=0.031u", "L=0.014u", "M=1"],
    ], "Unexpected inverter connectivity or sizing")
    # Ideal static switch interpretation of the actual CDL connectivity.
    truth = []
    for a in (0, 1):
        rails = {d[3] for d in devices if (d[4].startswith("pmos") and a == 0)
                 or (d[4].startswith("nmos") and a == 1)}
        require(len(rails) == 1, "Output floating or rails shorted in ideal switch model")
        y = int(rails == {"vdd"})
        require(y == 1 - a, "Inversion failed")
        truth.append({"A": a, "Y": y})
    lef = section(source(LEF), r"^MACRO " + CELL + r"\s", r"^END " + CELL + r"\s*$")
    width, height = re.search(r"SIZE ([\d.]+) BY ([\d.]+)", lef).groups()
    lib = liberty_group(source(LIB), "cell", CELL)
    area = re.search(r"\barea\s*:\s*([\d.]+)", lib)[1]
    require(Decimal(width) * Decimal(height) == Decimal(area), "LEF / LIB area mismatch")
    pin_data = {}
    for pin, direction, use, layer in [("A", "INPUT", "SIGNAL", "M1"), ("Y", "OUTPUT", "SIGNAL", "M1"),
                                        ("vdd", "INOUT", "POWER", "BPR"), ("vss", "INOUT", "GROUND", "BPR")]:
        block = section(lef, r"^  PIN " + pin + r"\s", r"^  END " + pin + r"\s*$")
        for fragment in (f"DIRECTION {direction}", f"USE {use}", f"LAYER {layer}"):
            require(fragment in block, f"LEF {pin}: {fragment}")
        rect = re.search(r"RECT\s+([^;]+);", block)[1].split()
        pin_data[pin] = {"direction": direction, "use": use, "layer": layer, "rect_um": rect}
    output = liberty_group(lib, "pin", "Y")
    require(re.search(r'function\s*:\s*"\(!A\)"', output), "Liberty inverter function")
    for pin, direction in [("A", "input"), ("Y", "output")]:
        require(re.search(r"direction\s*:\s*" + direction, liberty_group(lib, "pin", pin)), "LIB direction")
    for pin, kind in [("vdd", "primary_power"), ("vss", "primary_ground")]:
        require(kind in liberty_group(lib, "pg_pin", pin), "LIB power pin")
    names, layers, labels, references = gds_inventory((ROOT / GDS).read_bytes())
    require(names.count(CELL) == 1, "GDS cell missing or duplicated")
    require(set(labels) == set(pin_data), "GDS text labels differ from LEF/CDL ports")
    return {
        "status": "PASS: pinned source and collateral checks only",
        "source_commit": MANIFEST["source_commit"], "cell": CELL,
        "source_files_sha256_verified": len(MANIFEST["sha256"]),
        "cdl_device_count": len(devices), "ideal_switch_truth_table": truth,
        "lef_size_um": [width, height], "lib_area": area,
        "pins": pin_data, "gds_structure_count": len(names),
        "gds_cell_layer_ids": layers, "gds_cell_text_labels": labels,
        "gds_cell_references": references,
        "not_run": ["Custom Compiler import", "ICV DRC", "ICV LVS", "SPICE", "OpenROAD/PnR"],
    }


def replace_once(text, old, new):
    require(text.count(old) == 1, "Runset template changed: " + old)
    return text.replace(old, new, 1)


def prepare():
    # Never clobber a previous GUI session or verification result.
    work = HERE / "work"
    require(not work.exists(), "work/ already exists; rename it before preparing a new workspace")
    cc = work / "cc"
    for cell in ("nmos_lvt", "pmos_lvt"):
        shutil.copytree(ROOT / "techlib" / cell, cc / "gt2_techlib" / cell)
    shutil.copytree(ROOT / "std_cells" / MANIFEST["oa_cell"], cc / "gt2_std_cells" / MANIFEST["oa_cell"])
    # OA lib.defs uses DEFINE; keep gt2_official to resolve upstream references.
    definitions = '\n'.join(f'DEFINE {name} "{cc / folder}"' for name, folder in
                            [("gt2_official", "gt2_techlib"), ("gt2_std_cells", "gt2_std_cells")])
    (cc / "lib.defs").write_text(definitions + "\n")
    # Preserve the full upstream CDL header/notice on the extracted single cell.
    header = source(CDL).split(".subckt", 1)[0]
    for mode in ("drc", "lvs"):
        target = work / "icv" / mode
        target.mkdir(parents=True)
        shutil.copy2(ROOT / GDS, target / "input.gds")
        shutil.copytree(ROOT / "icv_runset/Include", target / "Include")
        deck = source(f"icv_runset/gt2_main.{mode}.rs")
        if mode == "drc":
            anchor = '#include "string.rh"'
            deck = replace_once(deck, anchor, anchor + '\n\n// Learning workspace input binding only.\n'
                                + f'library(cell = "{CELL}", format = GDSII, library_name = "input.gds");')
        else:
            deck = replace_once(deck, 'cell         = "cell"', f'cell         = "{CELL}"')
            deck = replace_once(deck, 'library_name = "inlib"', 'library_name = "input.gds"')
            deck = replace_once(deck, '{{"sch", SPICE}}', '{{"source.cdl", SPICE}}')
            (target / "source.cdl").write_text(header + cdl_cell() + "\n")
        (target / f"gt2_main.{mode}.rs").write_text(deck)
    (work / "preflight.json").write_text(json.dumps(audit(), indent=2) + "\n")
    print("Prepared work/cc and work/icv/{drc,lvs}; no EDA tools were run.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "prepare"])
    args = parser.parse_args()
    report = audit()
    if args.action == "check":
        print(json.dumps(report, indent=2))
    else:
        prepare()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit("FAIL: " + str(error)) from error
