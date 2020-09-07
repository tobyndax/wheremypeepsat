import sys
import argparse
import os
from pydub import AudioSegment, utils
from pydub.silence import split_on_silence
import plotly.graph_objects as go
import numpy as np


def createParser():
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
    parser.add_argument('--feedback',
                        dest='feedback',
                        action='store_true',
                        help='Generates a feedback image')
    parser.set_defaults(feature=False)
    return parser

def main(args):
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
    if args.sil is not None:
        silenceLevel = args.sil
    else:
        silenceLevel = sound_file.dBFS - 10


    silenceScale = sound_file.max_possible_amplitude * utils.db_to_float(silenceLevel)
    sound_file = sound_file[start:end]
    audio_segs = split_on_silence(
        sound_file,
        # must be silent for at least this long
        min_silence_len=150,
        # consider it silent if quiter than this
        silence_thresh=silenceLevel,
        keep_silence=True
    )

    if args.feedback:
        offset = 0
        subSample = 32
        fig = go.Figure()
        for i, seg in enumerate(audio_segs):
            y = np.array(seg.get_array_of_samples())
            start = offset
            end = len(seg) + offset
            offset = end
            t = np.linspace(start, end ,len(y))
            fig.add_trace(
                go.Scatter(x=t[::subSample]/1000, y=y[::subSample],
                           mode='lines',
                           name='lines'))
        fig.add_trace(
            go.Scatter(x=np.array([0, end])/1000, y=np.array([silenceScale, silenceScale]),
                       mode='lines',
                       name='lines'))
        fig.update_layout(showlegend=False)
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                type="linear"
            )
        )
        initial_range = [0, 10]
        fig['layout']['xaxis'].update(range=initial_range)
        fig.show()

    return len(audio_segs)


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    print(main(args))

