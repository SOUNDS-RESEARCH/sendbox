# sendbox
The Sendbox toolbox is part of the WP(1-)2(-3) workload.

Audio → Opus Encoder → Binary data (bits)

→ CommPy (modulation, introducing redundancy) → Binary data (bits)

→ CommPy (additive white Gaussian noise) → Binary data (bits) with errors

→ CommPy (demodulation, getting rid of the redundancy) → Binary data (bits) with errors

→ Opus Decoder → Audio (with channel effects)


Producing OPUS file from audio file
Reading OPUS file in Python, as bits
Process bits in CommPy
Make OPUS read the produced bits and decode to an audio file
