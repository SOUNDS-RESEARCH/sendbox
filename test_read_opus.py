# Purpose of script:
# Test the read_opus function.
#
# (c) Paul Didier, SOUNDS ETN, KU Leuven ESAT STADIUS

import sys
import librosa
import matplotlib.pyplot as plt

FILENAME = 'output.opus'

def main():
    """Main function (called by default when running script)."""
    read_opus(FILENAME)

def read_opus(fileName):
    """Read an opus file and return the data."""
    X, sr = librosa.load(
        fileName,
        res_type='kaiser_fast'
    )
    plt.plot(X)

if __name__ == '__main__':
    sys.exit(main())