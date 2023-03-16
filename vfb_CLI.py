#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
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
check = True
exaud = False

init()

def main():
    global vid_name, exaud
    parser = argparse.ArgumentParser(prog="videoFilter_CLI",description="Bilateral video filter on CLI")
    parser.add_argument('-src','--source',required=True,type=str,help='Source video')
    parser.add_argument('-dest','--destination',default="NewFilteredVid.mp4",type=str,help='Destination video')
    parser.add_argument('-d','--demo',action='store_true',help='test video')
    parser.add_argument('-ea','--exclude_audio',action='store_true',help='Exclude audio from processing')
    parser.add_argument('-pd','--pixel_diameter',type=int,default=9,help='Pixel diameter')
    parser.add_argument('-sgc','--sigma_color',type=float,default=75,help='Sigma color value')
    parser.add_argument('-sgs','--sigma_space',type=float,default=75,help='Sigma space value')
    '''parser.add_argument('-bt','--border_type',type=str,default='BORDER_DEFAULT',help='Border type',choices=['MORPH_ERODE','MORPH_DILATE','MORPH_OPEN','MORPH_CLOSE',
                                                                                                            'MORPH_GRADIENT','MORPH_TOPHAT','MORPH_BLACKHAT','MORPH_HITMISS'])'''
    args=parser.parse_args()
    vid_name = args.destination
    if args.exclude_audio:
        exaud = True
    app(args)

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
            #time.sleep(0.00001)

        Pname, ex = os.path.splitext(vid_name)
        Pfile = Pname+"_.mp4"
        out = cv.VideoWriter(Pfile,cv.VideoWriter_fourcc(*'XVID'), eval(frame_rate), size)
        for i in range(len(frame_array)):
            out.write(frame_array[i])
        out.release()
        vid = ffmpeg.input(Pfile)

        try:
            ffmpeg.output(audio,vid,vid_name).run()
            print(Fore.YELLOW+Style.DIM+f"\nSuccessfully created video '{vid_name}'"+Fore.RESET+Style.RESET_ALL)
            if args.demo:
                make_comp(args)
        except:
            try:
                ffmpeg.output(vid,vid_name).run()
                print(Fore.YELLOW+Style.DIM+f"\nSuccessfully created video '{vid_name}'"+Fore.RESET+Style.RESET_ALL)
                if args.demo:
                    make_comp(args)
            except Exception as e:
                print(Fore.RED+Style.DIM+"\n"+str(e)+Fore.RESET+Style.RESET_ALL)
                
        if Pfile in os.listdir():
            os.remove(Pfile)
            print("REMOVED {}".format(Pfile))
            
    except Exception as e:
        print(Fore.RED+Style.DIM+"\n"+str(e)+Fore.RESET+Style.RESET_ALL)

def frames_editor(args):
    global frame_list, audio, check
    try:
        cam = cv.VideoCapture(args.source)
        ffmp_input = ffmpeg.input(args.source)
        if exaud == False:
            audio = ffmp_input.audio
        
        print(f"PROCESSING FRAMES: [PixDiam:{args.pixel_diameter}|SigCol:{args.sigma_color}|SigSpc:{args.sigma_space}]")
        pbar = tqdm(total=int(n_frames))
        ret = True
        while ret:
            ret,frame = cam.read()
            if ret:
                edited_frame = cv.bilateralFilter(frame,args.pixel_diameter,args.sigma_color,args.sigma_space)
                frame_list.append(edited_frame)
                pbar.update(ret)
        cam.release()
        pbar.close()
        
    except Exception as e:
        check = False
        print(Fore.RED+Style.DIM+"\n"+str(e)+Fore.RESET+Style.RESET_ALL)
    
def app(args):
    global n_frames, frame_rate
    name, ex = os.path.splitext(args.source)
    name2, ex2 = os.path.splitext(args.destination)
    if ex == ".mp4" and ex2 == ".mp4":
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
            frames_editor(args)
            if check == True:
                create_video(args)
        else:
            print(Fore.RED+Style.DIM+f"\nERROR: File '{args.source}' not found."+Fore.RESET+Style.RESET_ALL)
    else:
         print(Fore.RED+Style.DIM+"\nBAD FILE FORMAT: Source file and destination file must have 'mp4' extension."+Fore.RESET+Style.RESET_ALL)

if __name__=="__main__":
    main()