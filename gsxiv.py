#!/usr/bin/env python3

import os, sys
import json
import subprocess


def geometry():
    j = (
        subprocess.Popen(["hyprctl", "activewindow", "-j"], stdout=subprocess.PIPE)
        .communicate()[0]
        .decode()
        .strip()
    )
    out = json.loads(j)
    [x, y] = out["at"]
    [w, h] = out["size"]
    return f"{w}x{h}+{x}+{y}"


if __name__ == "__main__":
    args = [
        '"' + a + '"' for a in sys.argv[1:]
    ]  # in case there are spaces in file names
    os.system(f"sxiv -g {geometry()}" + " " + " ".join(args))
