#!/usr/bin/env python3

import os, sys
import traceback
import argparse
import datetime
import subprocess


def main(args):
    cmd = "grim"
    if args.full:
        cmd += " -o $(hyprctl activeworkspace | head -n1 | awk '{print $NF}' | cut -d':' -f1)"
    else:
        dimension = (
            subprocess.Popen("slurp", stdout=subprocess.PIPE)
            .communicate()[0]
            .decode()
            .strip()
        )
        if dimension == "":
            return 0
        cmd += f' -g "{dimension}"'
    if args.clipboard:
        cmd += " - | wl-copy"
        path = "clipboard"
    else:
        fname = datetime.datetime.now().strftime("%Y_%m%d-%H.%M.%S.png")
        path = os.path.expanduser(f"~/Pictures/{fname}")
        cmd += f" {path}"

    ret = os.system(cmd)

    if args.notify:
        if ret != 0:
            os.system(f"notify-send 'Screenshot failed'")
            return ret
        else:
            os.system(f"notify-send 'Screenshot saved to {path}'")
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        dest="full",
        action="store_true",
        default=False,
        help="Full desktop screenshot",
    )
    parser.add_argument(
        "--clipboard",
        dest="clipboard",
        action="store_true",
        default=False,
        help="Copy image to clipboard",
    )
    parser.add_argument(
        "--notify",
        dest="notify",
        action="store_true",
        default=False,
        help="Whether to notify",
    )
    args = parser.parse_args()
    try:
        ret = main(args)
    except Exception as e:
        print(
            f"Main event loop exception: {e},\n{traceback.format_exc()}",
            file=sys.stderr,
        )
        ret = 1
    sys.exit(ret)
