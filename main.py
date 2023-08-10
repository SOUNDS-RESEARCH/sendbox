import numpy as np
import os
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
        raise Exception("Encoding did not go correct !!")
    

def call_opus_decoder(
        opus_filename,
        wav_out_name,
        decoder_name='opusdec_win'
    ):
    """Call the opus decoder with the given parameters."""

    fullPathOpus = build_opus_path(decoder_name)

    decoding_check = os.system(
        f'{fullPathOpus} {opus_filename} {wav_out_name}'
    )

    if decoding_check == 1:
        raise Exception("Decoding did not go correct !!")


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
    name = 'test.flac'
    # name_decoded = 'test.opus'

    call_opus_encoder(
        wav_filename=name,
        opus_out_name='output.opus',
        encoder_name='opusenc_win'
    )
    call_opus_decoder(
        opus_filename='output.opus',
        wav_out_name='output.wav',
        decoder_name='opusdec_win'
    )