import argparse
import re
import subprocess
import sys

from providers.ollama import OllamaProvider
from providers.openrouter import OpenRouterProvider
from providers.groq import GroqProvider
from memory import create_memory
from voice.tts import speak
from voice.stt import listen

# Parser ahh shit
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--provider", default="ollama")
parser.add_argument("-m", "--model", default=None)
parser.add_argument("--max-tokens", type=int, default=None)
parser.add_argument("--memory", default="none", choices=["none", "mem0", "zep"])
parser.add_argument("--voice", action="store_true", help="Use microphone input")
args = parser.parse_args()

if args.provider == "ollama":
    provider = OllamaProvider(model=args.model or "llama3")
elif args.provider == "openrouter":
    kwargs = {"model": args.model or "meta-llama/llama-3.3-70b-instruct"}
    if args.max_tokens is not None:
        kwargs["max_tokens"] = args.max_tokens
    provider = OpenRouterProvider(**kwargs)
elif args.provider == "groq":
    provider = GroqProvider(model=args.model or "llama-3.3-70b-versatile")
else:
    print(f"Unknown provider: {args.provider}")
    sys.exit(1)


# Memory stuff, These ai's are just so dumb can't even remember anything, I gotta tell them bruh. 
memory = create_memory(args.memory)

messages = [
    {
        "role": "system",
        "content": "You are Arthur, a helpful voice assistant. Keep responses concise, short, and conversational. Use plain paragraphs, not bullet points. You can run system commands on the user's computer by wrapping them in <cmd> tags, for example: <cmd>firefox</cmd> or <cmd>echo hello</cmd>. When the user asks you to do something that requires a command, respond briefly and include the <cmd> tag. The user is more likely to be on linux."
    }
]

# Main loop
while True:
    if args.voice:
        msg = listen()
        if not msg:
            continue
    else:
        msg = input("Ask: ")

    if memory:
        context = memory.get_context_message(msg)
        if context:
            messages.append(context)

    messages.append({"role": "user", "content": msg})

    reply = provider.chat(messages)
    messages.append({"role": "assistant", "content": reply})

    commands = re.findall(r"<cmd>(.*?)</cmd>", reply, re.DOTALL)
    clean_reply = re.sub(r"\s*<cmd>.*?</cmd>\s*", "", reply, flags=re.DOTALL).strip()

    for cmd in commands:
        print(f"Running: {cmd}")
        subprocess.Popen(cmd, shell=True)

    if memory:
        memory.store_conversation(msg, reply)

    if clean_reply:
        print("Arthur:", clean_reply)
        speak(clean_reply)
