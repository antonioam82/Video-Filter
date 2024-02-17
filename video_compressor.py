import ffmpeg
import argparse
from colorama import init, Back, Fore


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
    parser.add_argument('-src','--source',required=True,type=str,help='Source file name')
    parser.add_argument('-dest','--destination',default='compessed_video.mp4',type=str,help="Output video name")
    parser.add_argument('-qlt','--quality',type=int,default=23,help="...")
    parser.add_argument('-cdc','--codec',type=str,default='libx264',help="Video codec")
    parser.add_argument('-prs','--preset',type=str,default='medium',help="...")

    try:
        args=parser.parse_args()
        video_compression(args.source,args.destination,args.quality,args.codec,args.preset)
        print("VIDEO GENERADO CORRECTAMENTE")
    except Exception as e:
        print(str(e))


if __name__=='__main__':
    main()  
