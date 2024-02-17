import ffmpeg
import argparse
from colorama import init, Back, Fore


def video_compression(source, output, quality, codec):
    params = {
        'c:v': codec,
        'crf': quality,
        'preset': 'medium'
    }

    (
        ffmpeg
        .imput(source)
        .output(output, **params)
        .run()
    )

def main():
