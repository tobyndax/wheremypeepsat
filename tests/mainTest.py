import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WhereMyPeepsAt import *

parser = createParser()
args = parser.parse_args("""
        testData/0015.wav
        --start 45500
        --end 48950
    """.split())

assert(main(args) == 6)
print(main(args))

args = parser.parse_args("""
testData/0015.wav
--start 8700
--end 28700
""".split())
numPeeps = main(args)
print(numPeeps)
assert(numPeeps == 38)


args = parser.parse_args("""
testData/0024.wav
--start 6000
--end 186000
""".split())
numPeeps = main(args)

print(numPeeps)
assert(numPeeps == 277)

args = parser.parse_args("""
testData/0015.wav
--start 8000
--end 188000
""".split())
numPeeps = main(args)
print(numPeeps)
assert(numPeeps == 270)
