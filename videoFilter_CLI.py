#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
import threading
import os
import argparse

def main():

    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',type=str,help='Destination video')
    parser.add_argument('-flt','--filter',type=str,default='bilateral',choices=['bilateral','blur','median','denoisingCol','2d','pyrdown','sketched','mean'],help='Filter method')
    

