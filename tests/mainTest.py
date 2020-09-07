import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WhereMyPeepsAt import *

parser = createParser()
args = parser.parse_args("""
        testData/output.wav
        --feedback
        --start 45500
        --end 48950
    """.split())

assert(main(args) == 6)
print(main(args))

args = parser.parse_args("""
testData/output.wav
--feedback
--start 8700
--end 28700
""".split())
numPeeps = main(args)
print(numPeeps)
assert(numPeeps == 38)
