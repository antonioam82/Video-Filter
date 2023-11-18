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
    print("EDITING...")
    width, height, deep = frame.shape
    for y in range(width):
        for x in range(height):
            for c in range(deep):
                negative[y,x,c] = 255 - frame[y,x,c]
    return negative

# APLICACION DE FILTROS
def apply_filter(args,fr):
    if args.negative:
        negative = np.zeros(fr.shape, fr.dtype)
        edited_frame = negative_filter(negative,fr)
    if args.bilateral_filter:
        edited_frame = cv.bilateralFilter(fr,args.bilateral_filter[0],args.bilateral_filter[1],args.bilateral_filter[2])
    if args.cathode_ray_tube:
        edited_frame = apply_crt_effect(fr)
         
    frame_list.append(edited_frame)
    
        

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
    
        
def app(args):
    global n_frames, frame_rate, height, width, audio, frame_list
    
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
    
    while ret:
        ret, frame = cap.read()
        if ret:
            apply_filter(args,frame)

        if stop == True:
            print("stopped")##
            frame_list = []##
            print(Fore.YELLOW + Style.DIM + "\nFrame processing interrupted by user." + Fore.RESET + Style.RESET_ALL)
            break
    print(len(frame_list))
    cap.release()
    
    '''if len(frame_list) > 0:
        print("saving...")
        counter = 1
        for i in frame_list:
            print(type(i))
            cv.imwrite("frame"+str(counter)+".png",i)
            counter += 1'''
    
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
    
    args = parser.parse_args()

    if not (args.bilateral_filter or args.sharp_filter or args.blur or args.sketch or args.negative):
        parser.error(Fore.RED + Style.BRIGHT + "You must specify a filter function: -bf, -sharp, -blr, -skt, -neg" + Fore.RESET + Style.RESET_ALL)
    else:
        vid_name = args.destination
        if args.exclude_audio:
            exaud = True
        app(args)        

if __name__ == '__main__':
    main()

