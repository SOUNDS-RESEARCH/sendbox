#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def digital_modeller(message_bits)

    from __future__ import division, print_function  # Python 2 compatibility
    
    import math
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    import commpy.channelcoding.convcode as cc
    import commpy.channels as chan
    import commpy.links as lk
    import commpy.modulation as mod
    import commpy.utilities as util
    
    # =============================================================================
    # Convolutional Code 1: G(D) = [1+D^2, 1+D+D^2]
    # Standard code with rate 1/2
    # =============================================================================
    # Number of delay elements in the convolutional encoder
    memory = np.array(2, ndmin=1)
    
    # Generator matrix
    g_matrix = np.array((0o5, 0o7), ndmin=2)
    
    # Create trellis data structure
    trellis = cc.Trellis(memory, g_matrix)
    
            
    # ==================================================================================================
    # Complete example using Commpy features and compare hard and soft demodulation. Example with code 1
    # ==================================================================================================
    
    # Modem : QPSK
    modem = mod.QAMModem(4)
    
    # AWGN channel
    channels = chan.SISOFlatChannel(None, (1 + 0j, 0j))
    
    # SNR range to test
    SNRs = np.arange(0, 6) + 10 * math.log10(modem.num_bits_symbol)
    
    
    # Modulation function
    def modulate(bits):
        return modem.modulate(cc.conv_encode(bits, trellis, 'cont'))
    
    
    # Receiver function (no process required as there are no fading)
    def receiver_hard(y, h, constellation, noise_var):
        return modem.demodulate(y, 'hard')
    
    
    # Receiver function (no process required as there are no fading)
    def receiver_soft(y, h, constellation, noise_var):
        return modem.demodulate(y, 'soft', noise_var)
    
    
    # Decoder function
    def decoder_hard(msg):
        return cc.viterbi_decode(msg, trellis)
    
    
    # Decoder function
    def decoder_soft(msg):
        return cc.viterbi_decode(msg, trellis, decoding_type='soft')
    
    # Build model from parameters
    code_rate = trellis.k / trellis.n
    model_hard = lk.LinkModel(modulate, channels, receiver_hard,
                              modem.num_bits_symbol, modem.constellation, modem.Es,
                              decoder_hard, code_rate)
    model_soft = lk.LinkModel(modulate, channels, receiver_soft,
                              modem.num_bits_symbol, modem.constellation, modem.Es,
                              decoder_soft, code_rate)
    
    # Test
    BERs_hard = model_hard.link_performance(SNRs, 10000, 600, 5000, code_rate)
    BERs_soft = model_soft.link_performance(SNRs, 10000, 600, 5000, code_rate)
    plt.semilogy(SNRs, BERs_hard, 'o-', SNRs, BERs_soft, 'o-')
    plt.grid()
    plt.xlabel('Signal to Noise Ration (dB)')
    plt.ylabel('Bit Error Rate')
    plt.legend(('Hard demodulation', 'Soft demodulation'))
    plt.show()
    
    
            