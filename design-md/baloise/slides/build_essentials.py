#!/usr/bin/env python3
"""Build the 35-slide Prompting Essentials deck (Session 1).

Usage:  python3 build_essentials.py <corporate.potx> <out.pptx>

Same layout system as the Session 2 deck: slidekit carries every visual
decision, the modules under essentials/ carry only content.
"""
import importlib
import sys

from slidekit import drop_existing_slides, load_template, settle, snap_labels

MODULES = ["ess_00", "ess_01", "ess_02", "ess_03", "ess_04", "ess_05"]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    template, out = sys.argv[1], sys.argv[2]

    prs = load_template(template)
    drop_existing_slides(prs)
    for name in MODULES:
        module = importlib.import_module(f"essentials.{name}")
        for builder in module.SLIDES:
            builder(prs)
            settle(prs.slides[-1])
            snap_labels(prs.slides[-1])
    prs.save(out)
    print(f"wrote {out} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
