#!/usr/bin/env python3
import os
import time
import argparse
import random
import subprocess


transition_type = [
    "simple",
    "fade",
    "left",
    "right",
    "top",
    "bottom",
    "wipe",
    "wave",
    "grow",
    "center",
    "any",
    "outer",
]

transition_pos = [
    "center",
    "left",
    "top",
    "bottom",
    "right",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
]


def daemon(args):
    daemon_path = "swww-daemon"
    if args.bin_path:
        daemon_path = f"{args.bin_path}/swww-daemon"
    args.period = None
    while True:
        # in case swww-daemon crashes
        out = subprocess.Popen([f"{daemon_path}"], shell=True)
        time.sleep(0.1)
        main(args)
        out.communicate()


def ready():
    wait = 0.1
    while True:
        o = os.system("swww query")
        if o == 0:
            break
        time.sleep(wait)
        wait *= 2
        if wait > 6:
            wait = 6


def main(args):
    if args.image_list:
        args.image_list = ['"' + a + '"' for a in args.image_list]

    swww_path = "swww"
    if args.bin_path:
        swww_path = f"{args.bin_path}/swww"

    if args.period and args.image_list:
        ready()
        random.shuffle(args.image_list)
        lenth, idx = len(args.image_list), 0
        while True:
            time.sleep(args.period)
            os.system(
                f"{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} {args.image_list[idx]}"
            )
            idx = (idx + 1) % lenth

    if args.image:
        return os.system(
            f'{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} "{args.image}"'
        )
    elif args.image_list:
        return os.system(
            f"{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} {random.choice(args.image_list)}"
        )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--period",
        dest="period",
        type=float,
        default=None,
        help="The wallpaper swap period. Be used with --image-list, otherwise ignored. ",
    )
    parser.add_argument(
        "--image",
        dest="image",
        type=str,
        default=None,
        help="Use the image as wallpaper",
    )
    parser.add_argument(
        "--image-list",
        dest="image_list",
        nargs="+",
        type=str,
        default=None,
        help="The wallpaper image list. If not used with --period, a random image in the list will be set as wallpaper and exit",
    )
    parser.add_argument(
        "--bin-path",
        dest="bin_path",
        type=str,
        default=None,
        help="The swww/swww-daemon binary path",
    )
    parser.add_argument(
        "--daemon",
        dest="daemon",
        action="store_true",
        default=False,
        help="Run swww-daemon instead of swww",
    )
    args = parser.parse_args()
    if not args.daemon:
        main(args)
    else:
        daemon(args)
