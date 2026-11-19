import numpy as np


def preprocess_audio(audio_chunk):
    audio_data = np.frombuffer(audio_chunk, dtype=np.int16)

    audio_data = audio_data.astype(np.float32)

    audio_data = audio_data / 32768.0

    return audio_data