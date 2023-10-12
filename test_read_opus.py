# Purpose of script:
# Encodes a WAV file to OPUS, apply some channel-related disturbances
# on the bytes via a channel model, then decodes it back to WAV.
#
# (c) Paul Didier, Mohammad Bokaei, José Miguel Cadavid Tobón (SOUNDS ETN 2023)

import os
import sys
import pydub  # requires `ffmpeg`
import numpy as np
from pathlib import Path
from bitstring import BitArray
import commpy_trial_analog as cta
from sys import platform as PLATFORM

# Global variables (change as you want)
OPUS_DIRECTORY = 'opus'  # directory where opus encoder/decoder is located
INPUT_WAV_FILENAME = 'test_short.wav'  # input WAV file
SEED = 0  # seed for reproducibility
SNR = 10  # AWGN channel SNR [dB]
SIZE_OF_QAM_CONSTELLATION = 64  # 4, 16, 64, 256, 1024, 4096, 16384 (cf. `cta.analog_modeller`)
FRAME_SIZE = 2.5  # OPUS encoding frame size [ms]
BITRATE = 32  # OPUS encoding bitrate [kbits/s]

# Probably don't change these
AUDIO_CODEC = 'opus'  # 'opus' or something else (e.g., 'mp3')

def main(inWavFilename=INPUT_WAV_FILENAME):
    """Main function (called by default when running script)."""

    # Set seed for reproducibility
    np.random.seed(SEED)

    # Encode WAV file to OPUS
    print(f'Calling {AUDIO_CODEC.capitalize()} encoder...')
    encOutFilename = Path(inWavFilename).stem + f'_to_{AUDIO_CODEC}.{AUDIO_CODEC}'
    if (Path(encOutFilename).exists()):
        os.remove(encOutFilename)
    os.system(f'ffmpeg -i {inWavFilename} -frame_duration {FRAME_SIZE} -b:a {BITRATE}K -vbr off {encOutFilename}')
    
    # Read OPUS file
    print(f'Reading {AUDIO_CODEC.capitalize()} file...')
    audioEncoded: pydub.AudioSegment = pydub.AudioSegment.from_file(
        encOutFilename,
        codec = 'opus'
    )
    data = audioEncoded.raw_data
    # Convert to `BitArray` object
    print('Converting to BitArray object...')
    bitArray = BitArray(bytes=data)
    # Extract actual bits as `np.ndarray`
    bitsList = np.array([int(b) for b in bitArray.bin])

    # Modify bits as we want
    print('----- Modifying bits (channel effect) -----')
    decodedBits = cta.analog_modeller(
        bitsList,
        snr=SNR,
        plot=False,
        sizeOfQamConstellation=SIZE_OF_QAM_CONSTELLATION
    )
    backToBytes = BitArray(decodedBits).bytes
    print('----- Done modifying bits -----')

    # Write modified bits to WAV file
    backToWavFilename = f'{Path(inWavFilename).stem}_{AUDIO_CODEC}_codec_{SNR}dB_noise_QAM{SIZE_OF_QAM_CONSTELLATION}.wav'
    print('Writing WAV file...')
    audioForOutput = pydub.AudioSegment(
        data=backToBytes,
        sample_width=audioEncoded.sample_width,
        frame_rate=audioEncoded.frame_rate,
        channels=audioEncoded.channels
    )
    audioForOutput.export(
        backToWavFilename,
        format="wav",
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


def build_opus_path(encoder_name, opus_dir=OPUS_DIRECTORY):
    """Build the path to the opus encoder/decoder, 
    depending on the platform."""
    fullPathOpus = opus_dir
    if not 'darwin' in PLATFORM:
        sep = '\\'
        fullPathOpus += f'{sep}win'
    else:
        sep = '/'
    fullPathOpus += f'{sep}{encoder_name}'
    return fullPathOpus


if __name__ == '__main__':
    sys.exit(main())