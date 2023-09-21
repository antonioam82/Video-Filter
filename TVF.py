#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import os
import numpy as np
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import argparse
from tempfile import NamedTemporaryFile
import sys
#import concurrent_futures
from pynput import keyboard

init()

video_formats = [".mp4",".mov",".avi"]

def check_file(file):
    if file in os.listdir():
        name, ex = os.path.splitext(file)
        
        if ex in video_formats:
            return file
        else:
            raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"source file must be a supported video format ('.mp4', '.mov' and '.avi')." + Fore.RESET + Style.RESET_ALL)
    else:
        raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"file '{file}' not found." + Fore.RESET + Style.RESET_ALL)

def app(args):
    print('ok')

def main():
    global vid_name, exaud
    parser = argparse.ArgumentParser(prog="bvf 0.1", description="Terminal video filter")
    parser.add_argument('-src', '--source', required=True, type=check_file, help='Source video')
    parser.add_argument('-dest', '--destination', default='output_video.mp4', help='Output video name')
    parser.add_argument('-ea', '--exclude_audio', action='store_true', help='Exclude audio from processing')

    mutually_exclusive_group = parser.add_mutually_exclusive_group()

    mutually_exclusive_group.add_argument('-cont', '--contrast', default=0.0, help='Gamma value for contrast effect')
    mutually_exclusive_group.add_argument('-bf', '--bilateral_filter', type=str, help='...')
    mutually_exclusive_group.add_argument('-sharp', '--sharp_filter', type=str, help='...')
    mutually_exclusive_group.add_argument('-blr', '--blur', type=str, help='...')
    mutually_exclusive_group.add_argument('-skt', '--sketch', action='store_true', help='...')
    mutually_exclusive_group.add_argument('-neg', '--negative', action='store_true', help='...')
    

    args = parser.parse_args()

    if not (args.bilateral_filter or args.sharp_filter or args.blur or args.sketch or args.negative):
        parser.error(Fore.RED + Style.BRIGHT + "You must specify a filter function: -bf, -sharp, -blr, -skt, -neg" + Fore.RESET + Style.RESET_ALL)
    else:
        vid_name = args.destination
        if args.exclude_audio:
            exaud = True
        app(args)        

if __name__ == '__main__':
    main()
