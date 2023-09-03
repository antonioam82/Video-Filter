#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import os
import numpy as np
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import argparse
from tempfile import NamedTemporaryFile
import sys
from pynput import keyboard
import subprocess
from pydub import AudioSegment

frame_list = []
check = True
exaud = False
video_formats = [".mp4",".mov",".avi"]
stop = False

def check_value(v):
    try:
        if float(v) >= 0.0:
            return float(v)
        else:
            raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + "gamma value must be positive." + Fore.RESET + Style.RESET_ALL)
    except Exception as e:
        raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + str(e) + Fore.RESET + Style.RESET_ALL)

def check_extension(file):
    global ex
    name, ex = os.path.splitext(file)
    if ex in video_formats:
        return file
    else:
        raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"result file must be a supported video format ('.mp4', '.mov' and '.avi')." + Fore.RESET + Style.RESET_ALL)

def main():
    global vid_name, exaud
    parser = argparse.ArgumentParser(prog="bvf 1.2.1", description="Bilateral video filter on CLI", epilog='REPO: https://github.com/antonioam82/Video-Filter')
    parser.add_argument('-src', '--source', required=True, type=check_file, help='Source video')
    parser.add_argument('-dest', '--destination', default="NewFilteredVid.mp4", type=check_extension, help='Destination video')
    parser.add_argument('-ea', '--exclude_audio', action='store_true', help='Exclude audio from processing')
    parser.add_argument('-pd', '--pixel_diameter', type=int, default=9, help='Pixel diameter [Default: 9]')
    parser.add_argument('-sgc', '--sigma_color', type=float, default=75, help='Sigma color value [Default: 75]')
    parser.add_argument('-sgs', '--sigma_space', type=float, default=75, help='Sigma space value [Default: 75]')
    parser.add_argument('-cont','--contrast',type=check_value, default=0.0, help='Gamma value for contrast effect')

    args = parser.parse_args()
    vid_name = args.destination
    if args.exclude_audio:
        exaud = True
    app(args)

if __name__ == "__main__":
    main()


