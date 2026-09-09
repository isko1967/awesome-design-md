#!/usr/bin/env python3
"""Build one block of the prompting-workshop deck.

Usage:  python3 build.py <corporate.potx> <block-number> <out.pptx>
"""
import importlib
import sys

from slidekit import drop_existing_slides, load_template, settle


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    template, number, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    module = importlib.import_module(f"blocks.block_{number:02d}")
    prs = load_template(template)
    drop_existing_slides(prs)
    for builder in module.SLIDES:
        builder(prs)
        settle(prs.slides[-1])
    prs.save(out)
    print(f"wrote {out} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
