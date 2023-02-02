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
    r = requests.get(url, allow_redirects=True)
    open('ffmpeg.zip', 'wb').write(r.content)
    print("Download finished")


def main(args):
    def checkFileValid(filePath):
        print(filePath)
        fileExists = Path.exists(filePath)
        return fileExists

    print(args.inputFile)
    filePath = Path(args.inputFile).resolve().absolute()

    if not checkFileValid(filePath):
        print("File does not exist")
        sys.exit(1)

    print(filePath)
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
