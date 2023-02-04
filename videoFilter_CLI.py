#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
import threading
import os
import tqdm
import argparse

def main():

    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',type=str,help='Destination video')
    parser.add_argument('-flt','--filter',type=str,default='bilateral',choices=['bilateral','blur','median','denoisingCol','2d','pyrdown','sketched','mean'],help='Filter method')
    
    args=parser.parse_args()
    app(args)

def frames_editor(source):
    
    try:
        #ffmp_input = ffmpeg.input(source)
        cam = cv.VideoCapture(source)
        #audio = ffmp_input.audio
        ret = True
        while ret:
            ret,frame = cam.read()
            if ret:
                print("OK")
        print("END")
        
    except Exception as e:
        print(str(e))
    
def app(args):
    if args.source in os.listdir():
        probe = ffmpeg.probe(args.source)
        video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        n_frames = (video_streams[0]['nb_frames'])
        height = (video_streams[0]['height'])
        frame_rate = (video_streams[0]['avg_frame_rate'])
        print("\n******************INFO******************")
        print(f'SOURCE FILE: {args.source}')
        print(f'Number of frames: {n_frames}')
        print(f'Frame Rate: {frame_rate}')
        print(f'Height: {height}')
        print("****************************************")
        frames_editor(args.source)
    else:
        print(f"ERROR: File '{args.source}' not found.")

    
if __name__=="__main__":
    main()
