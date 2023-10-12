# Sendbox
The Sendbox toolbox is part of the WP(1-)2(-3) workload.

Requirements:
- `pydub` (`pip install pydub`) -- itself requiring `ffmpeg` library; see https://ffmpeg.org/.
- NumPy
- `commpy` (`pip install scikit-commpy`)
- `bitstring` (`pip install bitstring`)

Run the test script `test_read_opus.py` to:
1) Read a test WAV file (default available in repo: "test_short.wav")
2) Encode it to an OPUS file
3) Read the OPUS file as bytes.
4) Modify bytes to model the wireless channel.
5) Decode modified bytes with OPUS decoder to a WAV file.
