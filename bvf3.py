#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import ffmpeg
import numpy as np
import os
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import argparse

frame_list = []
check = True
exaud = False

init()

def main():
    global vid_name, exaud
    parser = argparse.ArgumentParser(prog="bvf 1.1",description="Bilateral video filter on CLI",epilog='REPO: https://github.com/antonioam82/Video-Filter')
    parser.add_argument('-src','--source',required=True,type=check_file,help='Source video')
    parser.add_argument('-dest','--destination',default="NewFilteredVid.mp4",type=check_extension,help='Destination video')
    parser.add_argument('-ea','--exclude_audio',action='store_true',help='Exclude audio from processing')
    parser.add_argument('-pd','--pixel_diameter',type=int,default=9,help='Pixel diameter [Default: 9]')
    parser.add_argument('-sgc','--sigma_color',type=float,default=75,help='Sigma color value [Default: 75]')
    parser.add_argument('-sgs','--sigma_space',type=float,default=75,help='Sigma space value [Default: 75]')
    
    args=parser.parse_args()
    vid_name = args.destination
    if args.exclude_audio:
        exaud = True
    app(args)

def check_file(file):
    if file in os.listdir():
        name, ex = os.path.splitext(file)
        if ex == ".mp4":
            return file
        else:
            raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"source file must be '.mp4' extension."+Fore.RESET+Style.RESET_ALL)
    else:
        raise argparse.ArgumentTypeError (Fore.RED+Style.BRIGHT+f"file '{file}' not found."+Fore.RESET+Style.RESET_ALL)

def check_extension(file):
    name, ex = os.path.splitext(file)
    if ex == ".mp4":
        return file
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"result file must be '.mp4' extension."+Fore.RESET+Style.RESET_ALL)

def create_video(args):
    print("\nCREATING VIDEO...")
    try:
     
        Pname, ex = os.path.splitext(vid_name)
        Pfile = Pname+"_.mp4"
        out = cv.VideoWriter(Pfile,cv.VideoWriter_fourcc(*'XVID'), eval(frame_rate), (width, height))
        for frame in tqdm(frame_list):
            out.write(frame)
        
        out.release()
        vid = ffmpeg.input(Pfile)

        if vid_name in os.listdir():
            os.remove(vid_name)

        try:
            if mute == False and exaud == False:
                ffmpeg.output(audio,vid,vid_name).run()
                print(Fore.YELLOW+Style.DIM+f"\nSuccessfully created video '{vid_name}'"+Fore.RESET+Style.RESET_ALL)
            else:
                ffmpeg.output(vid,vid_name).run()
                print(Fore.YELLOW+Style.DIM+f"\nSuccessfully created video '{vid_name}'"+Fore.RESET+Style.RESET_ALL)
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
        ffmp_input = ffmpeg.input(args.source) ###############################
        if mute == False and exaud == False: 
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

def check_audio(file):
    global mute
    audio_probe = ffmpeg.probe(file, select_streams='a')
    if audio_probe['streams']:
        mute = False
        return "Yes"
    else:
        mute = True
        return "No"
    
def app(args):
    global n_frames, frame_rate, height, width

    probe = ffmpeg.probe(args.source)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
    n_frames = (video_streams[0]['nb_frames'])
    height = (video_streams[0]['height'])
    width = (video_streams[0]['width'])
    frame_rate = (video_streams[0]['avg_frame_rate'])
    audio_c = check_audio(args.source)

    print(Fore.BLACK+Back.GREEN+"\n B I L A T E R A L  V I D E O   F I L T E R   1.1 \n"+Fore.RESET+Back.RESET)
            
    print(Fore.YELLOW+"\n********************VIDEO INFO********************")
    print(f'SOURCE FILE: {args.source}')
    print(f'Number of frames: {n_frames}')
    print(f'Frame Rate: {frame_rate}')
    print(f'Width: {width}')
    print(f'Height: {height}')
    print(f'Audio: {audio_c}')
    print("**************************************************\n"+Fore.RESET)
            
    frames_editor(args)
    if check == True:
        create_video(args)

if __name__=="__main__":
    main()
