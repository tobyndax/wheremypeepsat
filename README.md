# wheremypeepsat

## What does it do? 
Given a sound input, it segments the sound-input into segments separated by silence.
Then counts the segments and outputs the amount of segments. 

## Okay, but why does it do that? 
In behavioral research with fowl one sometimes do what's called a peep-test. 
Where you need to count the number of times a bird peeps during a time-period. 
Manual counting is not particularly reliable or repeatable. 

## Design idea 
Command line tool which takes a .wav file and a few settings and outputs a number. 

Settings: 
* Override quiet-level
* Length of time for silence-segments
* Boolean to generate feedback image?

## Todo
* Add tests for multiple dataset
* Write documentation for all options
* Add an image to the readme
