#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

import commpy.channelcoding.convcode as cc
import commpy.channels as chan
import commpy.modulation as mod


SIZE_OF_QAM_CONSTELLATION = 64
SNR = 0


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


def analog_modeller(
        bits,
        snr=SNR,  # [dB]
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

    # From SNR to STD
    powerModulatedBits = np.mean(np.abs(modulatedBits) ** 2)
    snrNormal = 10 ** (snr / 10)
    noiseStd = np.sqrt(powerModulatedBits / snrNormal)

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