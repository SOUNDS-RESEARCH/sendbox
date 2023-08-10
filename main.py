import numpy as np
import os

# Global variables
from sys import platform as PLATFORM
OPUS_DIR = 'opus'

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
    if 'win' in PLATFORM:
        sep = '\\'
        fullPathOpus += f'{sep}win'
    else:
        sep = '/'
    fullPathOpus += f'{sep}{encoder_name}'
    return fullPathOpus


if __name__ == '__main__':

    opus_out_name = 'output.opus'

    # Encode audio file into OPUS
    call_opus_encoder(
        wav_filename='test.flac',
        opus_out_name=opus_out_name,
    )

    # Decode OPUS file into audio
    call_opus_decoder(
        opus_filename=opus_out_name,
        wav_out_name='output.wav',
    )