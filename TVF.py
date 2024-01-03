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
from pydub import AudioSegment
#import concurrent_futures
from pynput import keyboard

init()

frame_list = []

video_formats = [".mp4",".mov",".avi"]
exaud = False
stop = False
check = True

def check_extension(file):
    global ex
    name, ex = os.path.splitext(file)
    if ex in video_formats:
        return file
    else:
        raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"result file must be a supported video format ('.mp4', '.mov' and '.avi')." + Fore.RESET + Style.RESET_ALL)

def check_file(file):
    if file in os.listdir():
        name, ex = os.path.splitext(file)
        
        if ex in video_formats:
            return file
        else:
            raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"source file must be a supported video format ('.mp4', '.mov' and '.avi')." + Fore.RESET + Style.RESET_ALL)
    else:
        raise argparse.ArgumentTypeError(Fore.RED + Style.BRIGHT + f"file '{file}' not found." + Fore.RESET + Style.RESET_ALL)

def negative_filter(negative,frame):
    width, height, deep = frame.shape
    for y in range(width):
        for x in range(height):
            for c in range(deep):
                negative[y,x,c] = 255 - frame[y,x,c]
    return negative

def apply_sketch_effect(fr):
    gray_image = cv.cvtColor(fr,cv.COLOR_BGR2GRAY)
    inver = 255 - gray_image
    blurred = cv.GaussianBlur(inver, (21,21),0)
    inver_blur = 255 - blurred
    sketched = cv.divide(gray_image,inver_blur,scale = 256.0)
    return sketched

# APLICACION DE FILTROS
def apply_filter(args,fr):
    if args.negative:
        negative = np.zeros(fr.shape, fr.dtype)
        edited_frame = negative_filter(negative,fr)
    elif args.bilateral_filter:
        edited_frame = cv.bilateralFilter(fr,args.bilateral_filter[0],args.bilateral_filter[1],args.bilateral_filter[2])
    elif args.cathode_ray_tube:
        edited_frame = apply_crt_effect(fr)
    elif args.distorsed:
        edited_frame = apply_distorsed_effect(fr)
    elif args.canny:
        edited_frame = apply_border_detection(fr)
    elif args.sketch:
        edited_frame = apply_sketch_effect(fr)
        
    # TO DO: sketct method, sharp method and blur mathod
         
    frame_list.append(edited_frame)

def apply_distorsed_effect(fr):
    rows, cols = fr.shape[:2]
    map_x = np.zeros(fr.shape[:2], np.float32)
    map_y = np.zeros(fr.shape[:2], np.float32)
    for i in range(rows):
        for j in range(cols):
            map_x[i, j] = j + 10 * np.sin(i / 10)
            map_y[i, j] = i + 10 * np.sin(j / 10)
    distorsed_img = cv.remap(fr, map_x, map_y, interpolation=cv.INTER_LINEAR)
    
    return distorsed_img

def on_press(key):##
    global stop
    if key == keyboard.Key.space:
        stop = True
        return False

def apply_crt_effect(fr):
    blur = cv.GaussianBlur(fr, (5,5), 0)
    for _ in range(5):
        for i in range(0, len(blur), 2):
            blur[i] = np.roll(blur[i], 1)
        for i in range(0, len(blur[0]), 2):
            blur[:, i] = np.roll(blur[:, i], 1)
        
    return blur

def apply_border_detection(fr):
    edges = cv.Canny(fr, 100, 200)
    return edges
   
def app(args):
    global n_frames, frame_rate, height, width, audio, frame_list, check
    
    cap = cv.VideoCapture(args.source)
    n_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv.CAP_PROP_FPS)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    audio = check_audio(args.source)

    print(Fore.BLACK + Back.GREEN + "\n T E R M I N A L   V I D E O   F I L T E R   v: 1.0 \n" + Fore.RESET + Back.RESET)
    print(Fore.YELLOW + "\n*********************VIDEO DATA*********************")
    print(f'SOURCE FILE: {args.source}')
    print(f'Number of frames: {n_frames}')
    print(f'Frame Rate: {frame_rate}')
    print(f'Frames Width: {width}')
    print(f'Frames Height: {height}')
    print(f'Audio Stream: {audio}')
    print("****************************************************\n" + Fore.RESET)

    print(args.source)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    cap = cv.VideoCapture(args.source)
    ret = True

    print(f"PROCESSING FRAMES -PRESS SPACE BAR TO CANCEL-")
    pbar = tqdm(total=int(n_frames), unit='frames')
    try:
        while ret:
            ret, frame = cap.read()
            if ret:
                apply_filter(args,frame)
                pbar.update(ret)

            if stop == True:
                frame_list = []##
                check = False
                print(Fore.YELLOW + Style.DIM + "\nFrame processing interrupted by user." + Fore.RESET + Style.RESET_ALL)
                pbar.disable = True
                break
    except Exception as e:
        check = False
        print(Fore.RED + Style.BRIGHT +'\nUnexpected error: ',str(e)+ Fore.RESET + Style.RESET_ALL)
        
    cap.release()
    pbar.close()

    if check == True:
        print("TO BE CONTINUED...")
    else:
        print("END")

    # ___________________________________________________________
    '''if len(frame_list) > 0:
        print("saving...")
        counter = 1
        for i in frame_list:
            print(type(i))
            cv.imwrite("frame"+str(counter)+".png",i)
            counter += 1'''
    #_____________________________________________________________
    
def check_audio(file):
    global mute
    try:
        audio = AudioSegment.from_file(file)
        print(audio)
        mute = False
        return True
    except Exception as e:
        mute = True
        return False

def main():
    global vid_name, exaud
    parser = argparse.ArgumentParser(prog="Terminal Video Filter 0.1", description="Terminal video filter")
    parser.add_argument('-src', '--source', required=True, type=check_file, help='Source video')
    parser.add_argument('-dest', '--destination', type=check_extension, default='output_video.mp4', help='Output video name')
    parser.add_argument('-ea', '--exclude_audio', action='store_true', help='Exclude audio from processing')

    mutually_exclusive_group = parser.add_mutually_exclusive_group()

    mutually_exclusive_group.add_argument('-cont', '--contrast', default=0.0, help='Gamma value for contrast effect')
    mutually_exclusive_group.add_argument('-bf', '--bilateral_filter', nargs=3, type=int, help='...')
    mutually_exclusive_group.add_argument('-sharp', '--sharp_filter', type=str, help='...')
    mutually_exclusive_group.add_argument('-blr', '--blur', type=str, help='...')
    mutually_exclusive_group.add_argument('-skt', '--sketch', action='store_true', help='...')
    mutually_exclusive_group.add_argument('-crt', '--cathode_ray_tube', action='store_true',help='...')
    mutually_exclusive_group.add_argument('-neg', '--negative', action='store_true', help='...')
    mutually_exclusive_group.add_argument('-dist','--distorsed',action='store_true', help='Apply distorsed effect on video.')
    mutually_exclusive_group.add_argument('-can','--canny',action='store_true', help='Get borders.')
    
    args = parser.parse_args()

    filters = [args.bilateral_filter, args.sharp_filter, args.blur, args.sketch, args.negative, args.cathode_ray_tube, args.distorsed, args.canny]
    if not any(filters):
        parser.error(Fore.RED + Style.BRIGHT + "You must specify a filter function: -bf, -sharp, -blr, -skt, -neg, -crt, -dist, -can" + Fore.RESET + Style.RESET_ALL)
    else:
        vid_name = args.destination
        if args.exclude_audio:
            exaud = True
        app(args)        

if __name__ == '__main__':
    main()

