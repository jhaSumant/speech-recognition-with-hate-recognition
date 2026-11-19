import os
import re

from recorder import AudioRecorder
from speech_recognizer import SpeechRecognizer
from moderator import Moderator
from logger import ModerationLogger


RECORDINGS_DIR = "audio/recordings"
RECORDING_FILE = os.path.join(RECORDINGS_DIR, "test_recording.wav")

# Basic display censoring for common offensive words.
# This affects displayed text, not the original audio.
CENSOR_WORDS = {
    "bitch", "fuck", "fucking", "shit", "asshole",
    "bastard", "idiot", "moron", "dick"
}


def censor_text(text):
    def replace_word(match):
        word = match.group(0)
        if word.lower() in CENSOR_WORDS:
            return "*" * len(word)
        return word

    pattern = r"\b[A-Za-z]+\b"
    return re.sub(pattern, replace_word, text)


def main():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    print("\n" + "=" * 50)
    print("       SPEECH MODERATION SYSTEM")
    print("=" * 50)

    recorder = AudioRecorder()
    recognizer = SpeechRecognizer()
    moderator = Moderator()
    logger = ModerationLogger()

    audio_chunks = []
    recorder_started = False

    try:
        recorder.start()
        recorder_started = True

        print("\nSpeak now. Recording one short sample...")
        print("Recording for approximately 6 seconds.\n")

        # One recording only: approximately 6.4 seconds.
        for _ in range(100):
            audio_chunks.append(recorder.read_chunk())

        recorder.save_audio(audio_chunks, RECORDING_FILE)
        print("Recording saved.")

    except KeyboardInterrupt:
        print("\nRecording cancelled.")

    except Exception as error:
        print(f"\nRecording error: {error}")
        return

    finally:
        if recorder_started:
            recorder.stop()

    print("\n[1/3] Recognizing speech...")

    text = recognizer.recognize_audio(RECORDING_FILE)

    if (
        text == "Speech could not be understood."
        or text == "Speech recognition service is unavailable."
        or text.startswith("Audio processing error:")
    ):
        print(f"Recognition issue: {text}")
        return

    print("\n[2/3] Moderating speech...")
    result = moderator.moderate(text)

    print("\n" + "=" * 50)
    print("              MODERATION REPORT")
    print("=" * 50)
    print(f"Original transcript:  {text}")
    print(f"Censored transcript:  {censor_text(text)}")
    print("-" * 50)
    print(f"Category:             {result['category']}")
    print(f"Confidence:           {result['confidence']:.2%}")
    print(f"Toxicity score:       {result['toxicity_score']:.4f}")
    print(f"Recommended action:   {result['action']}")
    print("=" * 50)

    print("\n[3/3] Saving moderation event...")

    logger.log_event(
        result["text"],
        result["category"],
        result["confidence"],
        result["action"]
    )

    print("Event saved to the moderation log.")
    print("\nRecording and moderation complete.")


if __name__ == "__main__":
    main()
