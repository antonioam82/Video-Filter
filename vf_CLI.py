#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
#import threading
import time
import os
from colorama import init, Fore
from pydub import AudioSegment
from tqdm import tqdm
import argparse

n_frames = 0
frame_list = []
frame_rate = ""
vid_name = ""
init()


def main():
    global vid_name
    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',default="NewFilteredVid.mp4",type=str,help='Destination video')
    parser.add_argument('-flt','--filter',type=str,default='bilateral',choices=['bilateral','blur','median','denoisingCol','2d','pyrdown','sketched','mean'],help='Filter method')

    args=parser.parse_args()
    vid_name = args.destination
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
        edit = cv.pyrDown(fr)
        
    return edit

def create_video():
    frame_array = []
    print("\nCREATING VIDEO...")
    for i in tqdm(frame_list):
        height = i.shape[0] 
        width = i.shape[1]       
        size = (width,height)

        for k in range(1):
            frame_array.append(i)
        time.sleep(0.00001)
    print("CREATING...")
    out = cv.VideoWriter(vid_name,cv.VideoWriter_fourcc(*'XVID'), eval(frame_rate), size)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()
    print("END: ",len(frame_array))   

def frames_editor(filterm,source):
    global frame_list
    try:
        cam = cv.VideoCapture(source)
        #ffmp_input = ffmpeg.input(source)
        #audio = ffmp_input.audio
        #audio.export("video_audio.mp3",format="mp3")
        #audio = AudioSegment.from_file(source)
        #audio.export("VidAudioInfo.mp3",format="mp3")
        #pbar = tqdm(desc="PROCESSING FRAMES: ",total=int(n_frames))
        print("PROCESSING FRAMES...")
        pbar = tqdm(total=int(n_frames))
        ret = True
        while ret:
            ret,frame = cam.read()
            if ret:
                frame_list.append(aply_method(filterm,frame))
                pbar.update(ret)
        pbar.close()
        #print("END")
        
    except Exception as e:
        print(str(e))
    
def app(args):
    global n_frames, frame_rate
    if args.source in os.listdir():
        probe = ffmpeg.probe(args.source)
        video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        n_frames = (video_streams[0]['nb_frames'])
        height = (video_streams[0]['height'])
        width = (video_streams[0]['width'])
        frame_rate = (video_streams[0]['avg_frame_rate'])
        codec_type = (video_streams[0]['avg_frame_rate'])
        print(Fore.YELLOW+"\n******************VIDEO INFO******************")
        print(f'SOURCE FILE: {args.source}')
        print(f'Number of frames: {n_frames}')
        print(f'Frame Rate: {frame_rate}')
        print(f'Width: {width}')
        print(f'Height: {height}')
        print("**********************************************\n"+Fore.RESET)
        frames_editor(args.filter,args.source)
        create_video()
    else:
        print(f"ERROR: File '{args.source}' not found.")

    
if __name__=="__main__":
    main()
