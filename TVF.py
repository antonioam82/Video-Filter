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
from pynput import keyboard


def main():
    parser = argparse.ArgumentParser(prog="bvf 0.1", description="Terminal video filter")
    parser.add_argument('-src', '--source', required=True, help='Source video')
    parser.add_argument('-dest','--destination',default='output_video.mp4',help='Output video name')
    parser.add_argument('-ea', '--exclude_audio', action='store_true', help='Exclude audio from processing')
    parser.add_argument('-cont','--contrast', default=0.0, help='Gamma value for contrast effect')
    parser.add_argument('-bf','--bilateral_filter',type=str,help='...')
    parser.add_argument('-sharp','--sharp_filter',type=str,help='...')

    args = parser.parse_args()

if __name__ == '__main__':
    main()
