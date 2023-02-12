import argparse
import sys
from sys import platform
import requests
from pathlib import Path
import zipfile
from glob import glob
import subprocess


def createParser():
    parser = argparse.ArgumentParser(
        description='Extracts the sound from a video file or all files in a directory')

    parser.add_argument('inputPath',
                        help='path to be processed. If the inputPath is a directory instead of a file all files inside the directory will be processed')

    parser.set_defaults(feature=False)
    return parser


def unzipffmpeg():
    with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
        zip_ref.extractall("ffmpeg")


def downloadffmpeg():
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    print("Downloading ffmpeg, this might take a while...")
    r = requests.get(url, allow_redirects=True, stream=True)

    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    dl = 0
    with open('ffmpeg.zip', 'wb') as f:
        for data in r.iter_content(block_size):
            f.write(data)
            dl += len(data)
            done = int(50 * dl / total_size)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
            sys.stdout.flush()

    print("Download finished")


def checkFileValid(filePath):
    fileExists = Path.exists(filePath)
    return fileExists


def main(args):

    path = Path(args.inputPath).resolve().absolute()

    if not checkFileValid(path):
        print("File does not exist")
        print(path)
        sys.exit(1)

    if platform == "linux" or platform == "linux2":
        exePath = "ffmpeg"
    else:
        if not checkFileValid(Path("ffmpeg.zip")):
            downloadffmpeg()
            unzipffmpeg()

        exePath = glob("ffmpeg/**/ffmpeg.exe", recursive=True)[0]

    # File case
    if path.is_file():
        outputFilePath = path.with_suffix(".wav")
        subprocess.run([exePath, "-i", path, outputFilePath], check=True)
        return 0
    else:
        files = [f for f in path.glob('*') if f.is_file()]
        for f in files:
            if f.suffix == '.wav':
                continue
            outputFilePath = f.with_suffix(".wav")
            subprocess.run([exePath, "-i", str(f), str(outputFilePath), '-loglevel', 'error', '-y'], check=False)
            print(f"Converted {f}")
        return 0


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    print(main(args))
