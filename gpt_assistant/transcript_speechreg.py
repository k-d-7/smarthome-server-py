import pyaudio
import wave
import openai
import os
import audioop
from dotenv import load_dotenv

load_dotenv()
# config = dotenv_values(".env")
# gpt_key = "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"
gpt_key = os.getenv("GPT-API-KEY")

openai.api_key = gpt_key


def recordToTranscipt():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 8

    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print(
        "=========================================START RECORDING======================================="
    )
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
        input_device_index=1,
    )

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print(
        "========================================STOP RECORDING========================================="
    )

    wf = wave.open("command.wav", "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()


def checkVolume(filename, threshold=600):
    with wave.open(filename, "rb") as wf:
        data = wf.readframes(wf.getnframes())
        rms = audioop.rms(
            data, wf.getsampwidth()
        )  # Calculate root mean square (RMS) volume level
        if rms >= threshold:
            print(f"Volume level: {rms}")
            return True
        else:
            print(f"Volume level is too low: {rms}")
            return False


def transciptOpenAI():
    audio_file = open("command.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"].encode("utf-8").decode("utf-8")


# record2transcipt()
# print(transcipt_openai())
def evaluateTranscipt():
    i = 0
    while True:
        recordToTranscipt()
        # is_valid_volume =check_volume('voice_check/command.wav')
        is_valid_volume = True
        if is_valid_volume == True:
            result = transciptOpenAI()
            print(result)
            i += 1
            if i == 3:
                break


evaluateTranscipt()
