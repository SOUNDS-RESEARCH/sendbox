# Purpose of script:
# Test the read_opus function.
#
# (c) Paul Didier, SOUNDS ETN, KU Leuven ESAT STADIUS

import sys
import numpy as np
from bitstring import BitArray

FILENAME = 'output.opus'

def main():
    """Main function (called by default when running script)."""
    data = read_opus(FILENAME)

    # Convert to BitArray object
    bitArray = BitArray(bytes=data)
    # Extract actual bits as np.ndarray
    bitsList = np.array([int(b) for b in bitArray.bin])
    # Modify bits as you want
    bitsListModified = bitsList  # whatever CommPy does
    # Go back to bytes via BitArray object
    backToBytes = BitArray(bitsListModified).bytes

    # print(data == backToBytes)

    stop = 1 

def read_opus(fileName):
    """Read an opus file and return the data."""
    f = open(fileName, 'rb')
    data = f.read()
    f.close()
    return data

if __name__ == '__main__':
    sys.exit(main())