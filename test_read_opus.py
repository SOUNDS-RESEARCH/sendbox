# Purpose of script:
# Test the read_opus function.
#
# (c) Paul Didier, SOUNDS ETN, KU Leuven ESAT STADIUS

import sys
import numpy as np
from bitstring import BitArray
import commpy_trial_digital as ctd
import commpy_trial_analog as cta
import numpy as np
import os

# Global variables
from sys import platform as PLATFORM
OPUS_DIR = 'opus'

FILENAME = 'test.flac'
SEED = 0

def main():
    """Main function (called by default when running script)."""

    np.random.seed(SEED)

    # call_opus_encoder(
    #     wav_filename='test.flac',
    #     opus_out_name=opus_out_name,
    # )
    
    print('Calling OPUS decoder...')
    call_opus_decoder(
        opus_filename='output.opus',
        wav_out_name='output2.wav'
    )



    data = read_opus(FILENAME)

    # Convert to BitArray object
    bitArray = BitArray(bytes=data)
    # Extract actual bits as np.ndarray
    bitsList = np.array([int(b) for b in bitArray.bin])

    bitsList = bitsList[:8**5]

    # Modify bits as you want
    decodedBits = cta.analog_modeller(bitsList, noiseStd=0.0, plot=False)
    # Go back to bytes via BitArray object
    backToBytes = BitArray(decodedBits).bytes

    # Write OPUS file
    print('Writing OPUS file...')
    write_opus('output2.opus', backToBytes)

    # Call OPUS decoder
    print('Calling OPUS decoder...')
    call_opus_decoder(
        opus_filename='output.opus',
        wav_out_name='output2.wav'
    )


def read_opus(fileName):
    """Read an opus file and return the data."""
    f = open(fileName, 'rb')
    data = f.read()
    f.close()
    return data


def write_opus(fileName, data):
    """Writes an opus file."""
    f = open(fileName, 'wb')
    f.write(data)
    f.close()


def call_opus_encoder(
        wav_filename,
        opus_out_name,
        encoder_name='opusenc',
        bitrate=160
    ):
    """Call the opus encoder with the given parameters."""

    fullPathOpus = build_opus_path(encoder_name)

    encoding_check = os.system(
        f'{fullPathOpus} --bitrate {bitrate} {wav_filename} {opus_out_name}'
    )

    if encoding_check == 1:
        raise Exception("Encoding failed !!")
    

def call_opus_decoder(
        opus_filename,
        wav_out_name,
        decoder_name='opusdec'
    ):
    """Call the opus decoder with the given parameters."""

    fullPathOpus = build_opus_path(decoder_name)

    decoding_check = os.system(
        f'{fullPathOpus} {opus_filename} {wav_out_name}'
    )

    if decoding_check == 1:
        raise Exception("Decoding failed !!")


def build_opus_path(encoder_name):
    """Build the path to the opus encoder/decoder, 
    depending on the platform."""

    fullPathOpus = f'{OPUS_DIR}'
    if not 'darwin' in PLATFORM:
        sep = '\\'
        fullPathOpus += f'{sep}win'
        encoder_name += '_win'
    else:
        sep = '/'
    fullPathOpus += f'{sep}{encoder_name}'
    return fullPathOpus

if __name__ == '__main__':
    sys.exit(main())