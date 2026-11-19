
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Ignore very quiet background noise.
        self.recognizer.dynamic_energy_threshold = True

        # Allow a little more time for speech to be processed.
        self.recognizer.pause_threshold = 0.8

    def recognize_audio(self, filename):
        try:
            with sr.AudioFile(filename) as source:
                # Estimate background noise before processing.
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.3
                )

                audio = self.recognizer.record(source)

            # Specify English for speech recognition.
            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            return text

        except sr.UnknownValueError:
            return "Speech could not be understood."

        except sr.RequestError:
            return "Speech recognition service is unavailable."

        except (OSError, ValueError) as error:
            return f"Audio processing error: {error}"
 