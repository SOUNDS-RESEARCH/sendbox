# Purpose of script:
# Test the read_opus function.
#
# (c) Paul Didier, SOUNDS ETN, KU Leuven ESAT STADIUS

import sys

FILENAME = 'output.opus'

def main():
    """Main function (called by default when running script)."""
    read_opus(FILENAME)

def read_opus(fileName):
    """Read an opus file and return the data."""
    f = open(fileName, 'rb')
    data = f.read()
    f.close()

if __name__ == '__main__':
    sys.exit(main())