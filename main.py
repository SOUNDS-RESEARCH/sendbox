import numpy as np
import os


def call_opus_encoder(name):

    enocoding_check = os.system('opusenc --bitrate 160 ' + name + ' ' + 'output.opus')

    if enocoding_check == 1:
        raise Exception("Encoding did not go correct !!")
    

def call_opus_decoder(name): 

    enocoding_check = os.system('opusdec output.opus test_opus.wav')
 


if __name__ == '__main__':
    name = 'test.flac'
    name_decoded = 'test.opus'

    call_opus_encoder(name)
    call_opus_decoder(name_decoded)