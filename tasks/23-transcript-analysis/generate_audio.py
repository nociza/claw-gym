#!/usr/bin/env python3
"""Generate a simple WAV file for the transcript-analysis task.

Creates a 5-second, 44100Hz mono WAV with a sine wave tone.
The agent needs to extract duration and sample rate from the WAV headers.
"""
import math
import struct
import wave
from pathlib import Path


def main():
    out_path = Path(__file__).parent / "seed" / "meeting.wav"
    out_path.parent.mkdir(exist_ok=True)

    sample_rate = 44100
    duration = 5.0  # seconds
    frequency = 440.0  # A4 note
    amplitude = 16000

    n_samples = int(sample_rate * duration)

    with wave.open(str(out_path), "w") as wf:
        wf.setnchannels(1)       # mono
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            value = int(amplitude * math.sin(2 * math.pi * frequency * t))
            frames.extend(struct.pack("<h", value))

        wf.writeframes(bytes(frames))

    print(f"Generated {out_path}")
    print(f"  Duration: {duration}s, Sample rate: {sample_rate}Hz, Channels: 1, Bits: 16")


if __name__ == "__main__":
    main()
