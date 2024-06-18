# llama-password-gen

A small* Python utility for generating a password based on a user-provided input using a Large Language Model (LLM). This project is inspired by Randall Munroe's XKCD comic that suggests using four random words (no space), with a mix of nouns, verbs, adjectives, and adverbs.

## Features

- Generates a password based on a user-provided input using an LLM.
- Uses a salt for additional security.
- Supports benchmarking mode for generating passwords for a list of sites.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/llama-password-gen.git
cd llama-password-gen
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Make sure you have Ollama installed and running locally. You can download it from [here](https://ollama.com).
4. Pull the Llama3:8b model using
```
ollama pull llama3:8b
```


## Usage
To generate a password based on a user-provided input, run the following command:
```
python main.py --input "your-input-here"
```

To run the benchmark mode and generate passwords for a list of sites, create a sites.txt file with one site per line and run the following command:

```
python main.py --benchmark
```


<i>* not including the LLM</i>