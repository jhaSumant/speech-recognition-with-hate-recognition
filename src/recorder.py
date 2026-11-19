import pyaudio
import wave


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024

        self.stream = None

    def start(self):
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )

            print("Microphone started.")

        except Exception as error:
            print("Microphone error:", error)
            self.audio.terminate()
            raise

    def read_chunk(self):
        if self.stream is None:
            raise RuntimeError("Microphone is not started.")

        return self.stream.read(
            self.chunk,
            exception_on_overflow=False
        )
    def save_audio(self, audio_chunks, filename):
        with wave.open(filename, "wb") as audio_file:
            audio_file.setnchannels(self.channels)
            audio_file.setsampwidth(self.audio.get_sample_size(self.format))
            audio_file.setframerate(self.rate)
            audio_file.writeframes(b"".join(audio_chunks))

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.audio.terminate()

        print("Microphone stopped.")