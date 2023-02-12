import argparse
import sys
import requests
from pathlib import Path
import zipfile
from glob import glob
import subprocess


def createParser():
    parser = argparse.ArgumentParser(
        description='Extracts the sound from a video file')

    parser.add_argument('inputFile',
                        help='file to be processed')

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


def main(args):
    def checkFileValid(filePath):
        fileExists = Path.exists(filePath)
        return fileExists

    filePath = Path(args.inputFile).resolve().absolute()

    if not checkFileValid(filePath):
        print("File does not exist")
        print(filePath)
        sys.exit(1)

    if not checkFileValid(Path("ffmpeg.zip")):
        downloadffmpeg()
        unzipffmpeg()

    exePath = glob("ffmpeg/**/ffmpeg.exe", recursive=True)[0]

    outputFilePath = filePath.with_suffix(".wav")
    subprocess.run([exePath, "-i", filePath, outputFilePath], shell=True, check=True)
    return 0


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    print(main(args))
