#!/usr/bin/env python3
"""Build the whole 54-slide prompting-workshop deck.

Usage:  python3 build_all.py <corporate.potx> <out.pptx>

Blocks run in slide order: 0 (opening) 1..5 (technique blocks, the break
rides at the end of block 3) 6 (clinic) 7 (transfer & close).
"""
import importlib
import sys

from slidekit import drop_existing_slides, load_template, settle

BLOCKS = [0, 1, 2, 3, 4, 5, 6, 7]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    template, out = sys.argv[1], sys.argv[2]

    prs = load_template(template)
    drop_existing_slides(prs)
    for number in BLOCKS:
        module = importlib.import_module(f"blocks.block_{number:02d}")
        for builder in module.SLIDES:
            builder(prs)
            settle(prs.slides[-1])
    prs.save(out)
    print(f"wrote {out} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
