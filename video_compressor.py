#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ffmpeg
import argparse
from colorama import init, Back, Fore, Style
import pathlib
import os

init()

def check_source(file):
    file_extension = pathlib.Path(file).suffix
    if file in os.listdir():
        if file_extension != '.mp4':
            raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Enter a 'mp4' video format ('{file_extension}' is not valid)."+Fore.RESET+Style.RESET_ALL)
        else:
            return file
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"FILE NOT FOUND: File '{file}' not found."+Fore.RESET+Style.RESET_ALL)

def check_val_range(n):
    if int(n) in range(0,52):
        return n
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"VALUE OUT OF RANGE: Quality value must be in range 0 to 51."+Fore.RESET+Style.RESET_ALL)
    

def video_compression(source, output, quality, codec, preset):
    params = {
        'c:v': codec,
        'crf': quality,
        'preset': preset
    }

    (
        ffmpeg
        .input(source)
        .output(output, **params)
        .run()
    )

def main():
    parser = argparse.ArgumentParser(prog="VIDEO COMPRESSOR",conflict_handler='resolve',
                                     description = "Compress video files in command line",
                                     epilog = "REPO: https://github.com/antonioam82/Video-Filter/blob/main/video_compressor.py")
    parser.add_argument('-src','--source',required=True,type=check_source,help='Source file name')
    parser.add_argument('-dest','--destination',default='compessed_video.mp4',type=str,help="Output video name")
    parser.add_argument('-qlt','--quality',type=check_val_range,default=23,help="...")
    parser.add_argument('-cdc','--codec',type=str,default='libx264',help="Video codec")
    parser.add_argument('-prs','--preset',type=str,default='medium',choices=['fast','ultrafast','medium','slow','veryslow'],help="...")

    try:
        args=parser.parse_args()
        video_compression(args.source,args.destination,args.quality,args.codec,args.preset)
        print("VIDEO GENERADO CORRECTAMENTE")
    except Exception as e:
        print(str(e))


if __name__=='__main__':
    main()
