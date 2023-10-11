# Purpose of script:
# Test the read_opus function.
#
# (c) Paul Didier, Mohammad Bokaei, José Miguel Cadavid Tobón, SOUNDS ETN

import os
import sys
import pydub  # requires ffmpeg
import numpy as np
from pathlib import Path
from bitstring import BitArray
import commpy_trial_analog as cta

from sys import platform as PLATFORM
OPUS_DIRECTORY = 'opus'
INPUT_WAV_FILENAME = 'test_short.wav'
SEED = 0
SNR = 10  # AWGN channel SNR [dB]
SIZE_OF_QAM_CONSTELLATION = 64
FRAME_SIZE = '2.5' #ms
BITRATE = '32K' # kb

AUDIO_CODEC = 'opus'  # 'opus' or something else

def main(inWavFilename=INPUT_WAV_FILENAME):
    """Main function (called by default when running script)."""

    # Set seed for reproducibility
    np.random.seed(SEED)

    # # Call OPUS encoder
    # if AUDIO_CODEC == 'opus':
    #     raise Exception('OPUS codec not working yet.') 
    #     print('Calling OPUS encoder...')
    #     opusOutFilename = Path(inWavFilename).stem + '_to_opus.opus'
    #     call_opus_encoder(
    #         wav_filename=inWavFilename,
    #         opus_out_name=opusOutFilename,
    #     )
    #     # Read OPUS file
    #     print('Reading OPUS file...')
    #     data = read_opus(opusOutFilename)
    # else:

   

    audio: pydub.AudioSegment = pydub.AudioSegment.from_file(
        inWavFilename,
        format="wav"
    )
    print(f'Calling {AUDIO_CODEC.capitalize()} encoder...')
    encOutFilename = Path(inWavFilename).stem + f'_to_{AUDIO_CODEC}.{AUDIO_CODEC}'

    if (Path(encOutFilename).exists()):
        os.remove(encOutFilename)

    os.system(f'ffmpeg -i {inWavFilename} -frame_duration {FRAME_SIZE} -b:a {BITRATE} -vbr off {encOutFilename}')
    print(f'Reading {AUDIO_CODEC.capitalize()} file...')
    audioEncoded: pydub.AudioSegment = pydub.AudioSegment.from_file(
        encOutFilename,
        # format=AUDIO_CODEC,
        codec = 'opus'
    )
    data = audioEncoded.raw_data

    # Convert to BitArray object
    print('Converting to BitArray object...')
    bitArray = BitArray(bytes=data)
    # Extract actual bits as np.ndarray
    bitsList = np.array([int(b) for b in bitArray.bin])

    # Modify bits as you want
    print('----- Modifying bits (channel effect) -----')
    decodedBits = cta.analog_modeller(
        bitsList,
        snr=SNR,
        plot=False,
        sizeOfQamConstellation=SIZE_OF_QAM_CONSTELLATION
    )
    backToBytes = BitArray(decodedBits).bytes
    print('----- Done modifying bits -----')

    backToWavFilename = f'{Path(inWavFilename).stem}_{AUDIO_CODEC}_codec_{SNR}dB_noise_QAM{SIZE_OF_QAM_CONSTELLATION}.wav'
    # if AUDIO_CODEC == 'opus':
    #     # Write OPUS file
    #     print('Writing OPUS file...')
    #     modifiedOpusFilename = f'{Path(inWavFilename).stem}_to_opus_modified.opus'
    #     write_opus(modifiedOpusFilename, backToBytes)

    #     # Call OPUS decoder
    #     print('Calling OPUS decoder...')
    #     call_opus_decoder(
    #         opus_filename=modifiedOpusFilename,
    #         wav_out_name=backToWavFilename
    #     )
    # else:
    # Write WAV file
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
        # encoder_name += '_win'
    else:
        sep = '/'
    fullPathOpus += f'{sep}{encoder_name}'
    return fullPathOpus

if __name__ == '__main__':
    sys.exit(main())