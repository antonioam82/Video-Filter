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


