import asyncio
import edge_tts
import subprocess
import tempfile
import os

VOICE = "en-GB-RyanNeural"


async def async_speak(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        fname = f.name
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

    subprocess.run(
        ["mpv", "--no-terminal", "--quiet", fname],
        check=True
    )
    os.unlink(fname)


def speak(text):
    asyncio.run(
        async_speak(text)
    )