# wheremypeepsat

[![GitHub](https://github.com/tobyndax/wheremypeepsat/workflows/Python%20application/badge.svg?branch=master)](https://github.com/tobyndax/wheremypeepsat)
## What does it do?
Given a sound input, it segments the sound-input into segments separated by
silence.
Then counts the segments and outputs the amount of segments.

![Feedback image](docs/outputExample.png)

## Okay, but why does it do that?
In behavioral research with fowl one sometimes do what's called a peep-test.
Where you need to count the number of times a bird peeps during a time-period.
Manual counting is not particularly reliable or repeatable.
For instance like in [this paper](https://liu.diva-portal.org/smash/record.jsf?dswid=-8294).

## Settings
The tool can be run from the commandline using the following command:
`python WhereMyPeepsAt.py soundFile.wav --start 1500 --end 61500 --feedback`
This will parse one minute of the soundfile.wav, starting at 1500 ms and at the
end of the sound-file it will present a feedback image of the sound splitting.

### Navigating the feedback image
One can use the arrow-keyes to navigate the feedback image and jump 10 seconds
of signal at a time. This is useful for manual inspection of the results.

### Additional settings

#### Silence Level
`--sil 86` overrides the silence level
Normally the tool calculates a suitable silence level. This is set to 10 dB
below the sound files [dBFS](https://en.wikipedia.org/wiki/DBFS).

If for some reason this is not suitable, this can be set manually using the
above setting. In the feedback image a horizontal line is rendered,
representing the silence level being used. The interpretation of this line is
not always immediately straightforward as the audio split is checking the RMS
in a window is above of below this level. In other words it's not enough that
the signal momentarily rises above this threshold. It needs to be above it for
a while. For details see
[pydub](https://github.com/jiaaro/pydub/blob/master/pydub/silence.py).

#### Statistical splitting
The tool uses a statistical splitting model for detecting sounds that are
distinctly different, but occur so rapidly that the sound level never drops
below the silence threshold for long enough. This is done by assuming that
each sound detected should have roughly the same length. Then statistical
outliers are found and by checking their length compared to the average length
if they are 2,3,4, etc extra sound splits.

