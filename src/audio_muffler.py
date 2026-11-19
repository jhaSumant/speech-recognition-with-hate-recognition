import subprocess
from pathlib import Path


def muffle_audio(input_file, output_file, start_time, duration):
    """
    Reduce the volume of a selected section of an audio recording.

    start_time: seconds where muffling begins
    duration: length of the section to muffle
    """

    input_file = str(Path(input_file))
    output_file = str(Path(output_file))

    start = max(0, float(start_time))
    duration = max(0.1, float(duration))
    end = start + duration

    audio_filter = (
        f"volume=enable='between(t,{start},{end})':volume=0.08"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-af", audio_filter,
        "-c:a", "pcm_s16le",
        output_file
    ]

    subprocess.run(command, check=True)

    print(f"Original audio: {input_file}")
    print(f"Muffled audio:  {output_file}")
    print(f"Muffled section: {start:.2f}s to {end:.2f}s")


if __name__ == "__main__":
    recording = Path("audio/recordings/test_recording.wav")

    if not recording.exists():
        print(f"Recording not found: {recording}")
        print("Record a sample first, then run this test again.")
    else:
        muffle_audio(
            input_file=recording,
            output_file="audio/recordings/muffled_test.wav",
            start_time=2.0,
            duration=1.0
        )
