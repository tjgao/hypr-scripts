#!/usr/bin/env python3

import os, sys
import json
import subprocess
import argparse


def sp_exists(name):
    cmd = f'hyprctl clients -j | jq ".[] | select(.workspace.name == \\"special:{name}\\")"'
    try:
        out = subprocess.check_output(cmd, shell=True).decode().strip()
        return out
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        return False


def main(args):
    if not args.jfile:
        args.jfile = os.path.expanduser("~/.config/hypr/scratchpads.json")
    try:
        ret = 0
        with open(args.jfile, "r") as f:
            data = json.load(f)
            if args.name not in data:
                print(
                    f"Name {args.name} was not found in json file:{args.jfile}",
                    file=sys.stderr,
                )
                return 1
            if not sp_exists(args.name):
                cmd = data[args.name]["cmd"]
                ret = os.system(
                    f'hyprctl dispatch "exec [workspace special:{args.name}] {cmd}"'
                )
            else:
                cmd = f'hyprctl dispatch togglespecialworkspace "{args.name}"'
                ret = os.system(cmd)
        return ret
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        dest="jfile",
        type=str,
        default=None,
        help="Use the specified json file otherwise use the default one",
    )
    parser.add_argument(
        "--name",
        type=str,
        dest="name",
        default=None,
        help="name of the special workspace",
    )

    args = parser.parse_args()
    if args.name is None:
        print("Please specify the name of the special workspace", file=sys.stderr)
        sys.exit(1)
    if main(args):
        print("Workspace not found", file=sys.stderr)
        sys.exit(1)
