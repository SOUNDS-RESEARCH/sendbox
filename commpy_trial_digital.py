#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:57:17 2023

@author: NH28KQ
"""

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
    
    # =============================================================================
    # Basic example using homemade counting and hard decoding
    # =============================================================================
    
    # Traceback depth of the decoder
    tb_depth = None  # Default value is 5 times the number or memories
    
    for i in range(10):
        # Generate random message bits to be encoded
            #message_bits = np.random.randint(0, 2, 1000)
        message_size = np.size(message_bits)
    
        # Encode message bits
        coded_bits = cc.conv_encode(message_bits, trellis)
    
        # Introduce bit errors (channel)
        coded_bits[np.random.randint(0,message_size)] = 0
        coded_bits[np.random.randint(0, message_size)] = 0
        coded_bits[np.random.randint(0, message_size)] = 1
        coded_bits[np.random.randint(0, message_size)] = 1
    
        # Decode the received bits
        decoded_bits = cc.viterbi_decode(coded_bits.astype(float), trellis, tb_depth)
    
        num_bit_errors = util.hamming_dist(message_bits, decoded_bits[:len(message_bits)])
    
        if num_bit_errors != 0:
            print(num_bit_errors, "Bit Errors found!")
        elif i == 9:
            print("No Bit Errors :)")
            