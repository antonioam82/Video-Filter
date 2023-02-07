#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
import threading
import os
from tqdm import tqdm
import argparse

n_frames = 0

def main():

    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',type=str,help='Destination video')
    parser.add_argument('-flt','--filter',type=str,default='bilateral',choices=['bilateral','blur','median','denoisingCol','2d','pyrdown','sketched','mean'],help='Filter method')
    
    args=parser.parse_args()
    app(args)

def aply_method(filterm,fr): #'bilateral','blur','median','denoisingCol','2d','pyrdown','sketched','mean'
    if filterm == 'bilateral':
        edit = cv.bilateralFilter(fr,9,75,75)
    elif filterm == 'blur':
        edit = cv.blur(fr, (5,5))
    elif filterm == 'median':
        edit = cv.medianBlur(fr,5)
    elif filterm == 'denoisingCol':
        edit = cv.fastNlMeansDenoisingColored(fr,None,20,10,7,21)
    elif filterm == 'pyrdown':
        cv.pyrDown(fr)
        
    return edit

def frames_editor(filterm,source):
    frame_list = []
    try:
        #ffmp_input = ffmpeg.input(source)
        cam = cv.VideoCapture(source)
        #audio = ffmp_input.audio
        pbar = tqdm(desc="PROCESSING FRAMES: ",total=int(n_frames))
        ret = True
        while ret:
            ret,frame = cam.read()
            if ret:
                frame_list.append(aply_method(filterm,frame))
                pbar.update(ret)
        pbar.close()
        print("END")
        
    except Exception as e:
        print(str(e))
    
def app(args):
    global n_frames
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
        frames_editor(args.filter,args.source)
    else:
        print(f"ERROR: File '{args.source}' not found.")

    
if __name__=="__main__":
    main()
