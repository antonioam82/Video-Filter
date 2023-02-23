#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
#import threading
import time
import os
from colorama import init, Fore, Style
from pydub import AudioSegment
from tqdm import tqdm
import argparse

n_frames = 0
frame_list = []
frame_rate = ""
vid_name = ""
audio = ""

init()

def main():
    global vid_name
    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',default="NewFilteredVid.mp4",type=str,help='Destination video')
    parser.add_argument('-d','--demo',action='store_true',help='test video')
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

def make_comp(args):
    print("\nCREATING SPLIT SCREEN VIDEO...")
    from moviepy.editor import VideoFileClip, clips_array
    
    vid1 = VideoFileClip(args.source).subclip(0, 3)
    vid2 = VideoFileClip(args.destination).subclip(0, 3)

    comb = clips_array([[vid1],
                        [vid2]])
    comb.write_videofile("test_video.mp4")
    vid1.close()
    vid2.close()
    

def create_video(args):
    frame_array = []
    print("\nCREATING VIDEO...")
    try:
        for i in tqdm(frame_list):
            height = i.shape[0] 
            width = i.shape[1]       
            size = (width,height)

            for k in range(1):
                frame_array.append(i)
            time.sleep(0.00001)
        
        out = cv.VideoWriter("provVid.mp4",cv.VideoWriter_fourcc(*'XVID'), eval(frame_rate), size)
        for i in range(len(frame_array)):
            out.write(frame_array[i])
        out.release()
        vid = ffmpeg.input("provVid.mp4")

        try:
            ffmpeg.output(audio,vid,vid_name).run()#vid
        except:
            ffmpeg.output(vid,vid_name).run()#vid'''

        if args.demo:
            make_comp(args)
            
        if 'provVid.mp4' in os.listdir():
            os.remove('provVid.mp4')
        
        print(f"\nSuccessfully created video '{vid_name}'")
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+"\n"+str(e)+Fore.RESET+Style.RESET_ALL)

def frames_editor(filterm,source):
    global frame_list, audio
    try:
        cam = cv.VideoCapture(source)
        ffmp_input = ffmpeg.input(source)
        audio = ffmp_input.audio
        
        print("PROCESSING FRAMES...")
        pbar = tqdm(total=int(n_frames))
        ret = True
        while ret:
            ret,frame = cam.read()
            if ret:
                frame_list.append(aply_method(filterm,frame))
                pbar.update(ret)
        cam.release()
        pbar.close()
        
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
        create_video(args)
    else:
        print(f"ERROR: File '{args.source}' not found.")

if __name__=="__main__":
    main()
