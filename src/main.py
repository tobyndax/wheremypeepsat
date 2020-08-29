import sys
import argparse
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import plotly.graph_objects as go
import numpy as np

if __name__ == '__main__':
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
                        help='Start time in ms where to start the processing')

    parser.add_argument('--end',
                        type=float,
                        help='End time in ms where to end the processing')
    args = parser.parse_args()

    def checkFileValid(filePath):
        fileExists  = os.path.isfile(filePath)
        fileIsWav = filePath.lower().endswith(".wav")
        return fileExists and fileIsWav


    if not checkFileValid(args.wavFile):
        print("File does not exist, or is not a wav-fil")
        sys.exit(1)

    sound_file = AudioSegment.from_wav(args.wavFile)

    start = 0
    end = len(sound_file)
    if args.start is not None:
        start = args.start
    if args.end is not None:
        end = args.end

    if start > end or start < 0 or end > len(sound_file):
        print("Incorrect start or end values")
        sys.exit(1)

    sound_file = sound_file[start:end]
    audio_segs = split_on_silence(
        sound_file,
        # must be silent for at least this long
        min_silence_len=125,
        # consider it silent if quiter than this
        silence_thresh=sound_file.dBFS - 16,
        keep_silence=True
    )
    offset = 0
    fig = go.Figure()
    for i, seg in enumerate(audio_segs):
        y = np.array(seg.get_array_of_samples())
        start = offset
        end = len(seg) + offset
        offset = end
        t = np.linspace(start, end ,len(y))
        fig.add_trace(
            go.Scatter(x=t, y=y,
                       mode='lines',
                       name='lines'))
    fig.update_layout(showlegend=False)
    fig.show()

    print(len(audio_segs))

