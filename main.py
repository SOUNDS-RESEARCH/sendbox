import numpy as np
import os


def call_opus_encoder(name):
    input = 'opusenc --bitrate 160 ' + name + ' ' + 'output.opus'
    print(input)
    enocoding_check = os.system(input)

    if enocoding_check == 1:
        raise Exception("Encoding did not go correct !!")


if __name__ == '__main__':
    name = 'test.flac'
    call_opus_encoder(name)