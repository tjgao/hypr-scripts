#!/usr/bin/env python3
import os
import time
import argparse
import random


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


def main(parser):
    args = parser.parse_args()
    if args.image_list:
        args.image_list = ['"' + a + '"' for a in args.image_list]

    swww_path = args.swww_path or "swww"

    if args.period and args.image_list:
        ready()
        random.shuffle(args.image_list)
        lenth, idx = len(args.image_list), 0
        while True:
            os.system(
                f"{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} {args.image_list[idx]}"
            )
            idx = (idx + 1) % lenth
            time.sleep(args.period)
        return 0
    if args.image:
        return os.system(
            f'{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} "{args.image}"'
        )
    elif args.image_list:
        return os.system(
            f"{swww_path} img --transition-type {random.choice(transition_type)} --transition-angle {random.randint(0, 359)} --transition-pos {random.choice(transition_pos)} {random.choice(args.image_list)}"
        )
    parser.print_help()
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
        "--swww-path",
        dest="swww_path",
        type=str,
        default=None,
        help="The swww binary path",
    )
    main(parser)
