import sys
import argparse
import os

parser = argparse.ArgumentParser(
    description='Count the number of distinct sound segments of the .wav file')

parser.add_argument('wavFile',
                    help='wav file to be processed')

parser.add_argument('--sil',
                    type=float,
                    help='''Override the silent level. Silent level is given in
                     dB typical values -96 to -16''')

parser.add_argument('--start',
                    type=float,
                    help='Start time in audio signal to start the processing')

parser.add_argument('--end',
                    type=float,
                    help='End time in the audio signal to end the processing')
args = parser.parse_args()

def checkFileValid(filePath):
    fileExists  = os.path.isfile(filePath)
    fileIsWav = filePath.lower().endswith(".wav")
    return fileExists and fileIsWav


if not checkFileValid(args.wavFile):
    print("File does not exist, or is not a wav-fil")
    sys.exit(1)

