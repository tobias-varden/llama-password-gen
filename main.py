# ```
# $ llama-password-gen --help

# usage: llama-password-gen [-h] [--input STRING]

# Generate a strong password using LLaMA and Randall Munroe's algorithm

# optional arguments:
#   -h, --help            show this help message and exit
#   --input STRING        input string to use as inspiration for the password generation (default: None)

# $ llama-password-gen --input "mysecretphrase"
# Generated password: catstovepianoelephant
# ```
# Blocking issue  https://github.com/ollama/ollama/pull/5045
# Blocking issue https://github.com/ggerganov/llama.cpp/issues/2838 The output is not deterministic on CUDA
# These two blocking issues, are related. Ollama have a direct dependency on llama.cpp

import argparse
import os
import struct
import hashlib
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)


def generate_seed(user_input, salt):
    # Combine user input and salt
    combined = user_input + salt

    # Generate SHA-256 hash of the combined string
    hash_object = hashlib.sha256(combined.encode())
    hash_bytes = hash_object.digest()

    # Convert the first 4 bytes of the hash to an int32
    seed, = struct.unpack('>i', hash_bytes[:4])

    # Ensure the seed is within the range of int32
    seed = abs(seed)

    return seed


def generate_password(input_string, salt):
    # Convert the input string to a seed from first converting it to a hash
    seed = generate_seed(input_string, salt)
    #print(seed)
    prompt = 'Generate a password that follows the rules outlined by Randall Munroe in his XKCD comic. Randall Munroes XKCD comic suggests'
    prompt += ' using four random words (no space), with a mix of nouns, verbs, adjectives, and adverbs. Output only the password, no explanation or nothing.'
    prompt += """\n\nExamples:\ncatstovepianoelephant\nmoonriverlaptopzebra\norangeskycastlepenguin\nlighthousecoffeejungle\nbutterflydeskthunderocean"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model='llama3:8b',
        seed=seed,
        temperature=1
    )
    
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate strong passwords using LLaMA and Randall Munroe's algorithm")
    parser.add_argument("--input", type=str, help="Address or site name that will be used as a seed for the password generation", default=None)
    parser.add_argument("--benchmark", type=bool, help="Run benchmark", default=None)

    args = parser.parse_args()

    input_string = args.input

    # Read the salt from the file, if the file does not exist, create it
    if not os.path.exists('./salt'):
        with open('./salt', 'wb') as fp:
            print('File not found, generating a new salt')
            # Generate a salt
            salt = os.urandom(16)
            fp.write(salt)
    else:
        with open('./salt', 'rb') as fp:
            salt = fp.read()

    if args.benchmark:
        # Read a list of sites to generate passwords for, then iterate through them:
        with open('./sites.txt', 'r') as fp:
            for line in fp.readlines():
                input_string = line.strip()
                generated_password = generate_password(input_string, str(salt))
                print(f"Generated password for {input_string}: {generated_password}")
    else:
        generated_password = generate_password(input_string, str(salt))
        print(f"Generated password: {generated_password}")