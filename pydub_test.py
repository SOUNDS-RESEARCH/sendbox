import pydub

# Load audio file
audio: pydub.AudioSegment = pydub.AudioSegment.from_file("test_short.wav", format="wav")

# Convert to mp3
audio.export(
    "test_short_mp3.mp3",
    format="mp3",
)
# Convert back to wav
audioMp3: pydub.AudioSegment = pydub.AudioSegment.from_file("test_short_mp3.mp3", format="mp3")
audioMp3.export(
    "test_short_mp3_to_wav.wav",
    format="wav",
)