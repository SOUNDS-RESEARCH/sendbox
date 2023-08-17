#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

import matplotlib.pyplot as plt
import numpy as np

import commpy.channelcoding.convcode as cc
import commpy.channels as chan
import commpy.links as lk
import commpy.modulation as mod


def encoding(bits):

    memory = np.array(2, ndmin=1)
    g_matrix = np.array((0o5, 0o7), ndmin=2)
    # Create trellis data structure
    trellis = cc.Trellis(memory, g_matrix)

    encodedBits = cc.conv_encode(bits, trellis, 'cont')

    return encodedBits, trellis

    
# Decoder function
def decoder_hard(msg, trellis):
    return cc.viterbi_decode(msg, trellis)


# Decoder function
def decoder_soft(msg, trellis):
    return cc.viterbi_decode(msg, trellis, decoding_type='soft')


SIZE_OF_QAM_CONSTELLATION = 16
NOISE_STD = 1.6  # TODO: the SNR depends on SIZE_OF_QAM_CONSTELLATION - fix that

def analog_modeller(
        bits,
        noiseStd=NOISE_STD,
        sizeOfQamConstellation=SIZE_OF_QAM_CONSTELLATION,
        plot=False
    ):
    """Modulate and demodulate bits using analog modulation."""

    # Encoding
    print('Encoding bits (channel)...')
    encodedBits, trellis = encoding(bits)

    # Modulation
    print('Modulating bits...')
    modem = mod.QAMModem(sizeOfQamConstellation)
    modulatedBits = modem.modulate(encodedBits)

    # AWGN channel
    print('Propagating bits through AWGN channel...')
    channels = chan.SISOFlatChannel(
        noise_std=noiseStd,
        fading_param=(1 + 0j, 0j)
    )
    receivedSignal = channels.propagate(modulatedBits)

    # Demodulation
    print('Demodulating bits...')
    demodulatedBits = modem.demodulate(receivedSignal, 'hard')
    # demodulatedBits = modem.demodulate(out, 'soft')   # THROWS ERROR FOR SOME REASON

    # Decoding
    print('Decoding bits (channel) [BE PATIENT!]...')
    decodedBits = decoder_hard(demodulatedBits, trellis)
    # decodedBits = decoder_soft(encodedBits)   # LESS ACCURATE
    
    if plot:
        fig, axes = plt.subplots(2, 1)
        fig.set_size_inches(8.5, 3.5)
        #
        axes[0].plot(bits, '.-', label='Original bits')
        axes[0].plot(demodulatedBits, '.--', label='Demodulated bits')
        axes[0].set_ylabel('Bit value')
        axes[0].set_title(f'DEMODULATION OUTPUT - Noise level {noiseStd} - {sizeOfQamConstellation}-QAM')
        axes[0].legend()
        #
        axes[1].plot(bits, '.-', label='Original bits')
        axes[1].plot(decodedBits, '.--', label='Decoded bits')
        axes[1].set_ylabel('Bit value')
        axes[1].set_title(f'DECODER OUTPUT - Noise level {noiseStd} - {sizeOfQamConstellation}-QAM')
        axes[1].legend()
        #
        fig.tight_layout()
        plt.show(block=False)

    return decodedBits

    # ==================================================================================================
    # # Complete example using Commpy features and compare hard and soft demodulation. Example with code 1
    # # ==================================================================================================
    
    # # Modem : QPSK
    # modem = mod.QAMModem(4)
    
    # # AWGN channel
    # channels = chan.SISOFlatChannel(None, (1 + 0j, 0j))
    
    # # SNR range to test
    # SNRs = np.arange(0, 6) + 10 * math.log10(modem.num_bits_symbol)
    
    # # Modulation function
    # def modulate(bits):
    #     return modem.modulate(cc.conv_encode(bits, trellis, 'cont'))
    
    
    # # Receiver function (no process required as there are no fading)
    # def receiver_hard(y, h, constellation, noise_var):
    #     return modem.demodulate(y, 'hard')
    
    
    # # Receiver function (no process required as there are no fading)
    # def receiver_soft(y, h, constellation, noise_var):
    #     return modem.demodulate(y, 'soft', noise_var)
    
    
    # # Decoder function
    # # def decoder_hard(msg):
    # #     return cc.viterbi_decode(msg, trellis)
    
    
    # # # Decoder function
    # # def decoder_soft(msg):
    # #     return cc.viterbi_decode(msg, trellis, decoding_type='soft')
    
    # # Build model from parameters
    # code_rate = trellis.k / trellis.n
    # model_hard = lk.LinkModel(modulate, channels, receiver_hard,
    #                           modem.num_bits_symbol, modem.constellation, modem.Es,
    #                           decoder_hard, code_rate)
    # model_soft = lk.LinkModel(modulate, channels, receiver_soft,
    #                           modem.num_bits_symbol, modem.constellation, modem.Es,
    #                           decoder_soft, code_rate)
    
    # # Test
    # BERs_hard = model_hard.link_performance(SNRs, 10000, 600, 5000, code_rate)
    # BERs_soft = model_soft.link_performance(SNRs, 10000, 600, 5000, code_rate)
    # plt.semilogy(SNRs, BERs_hard, 'o-', SNRs, BERs_soft, 'o-')
    # plt.grid()
    # plt.xlabel('Signal to Noise Ration (dB)')
    # plt.ylabel('Bit Error Rate')
    # plt.legend(('Hard demodulation', 'Soft demodulation'))
    # plt.show()
    
    
            