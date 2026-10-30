# Ollama Explorer

A Python script that runs four experiments against a local LLM through Ollama's `/api/chat` endpoint. It looks at how system prompts, context grounding, prompt length, and temperature affect the model's responses.

> [!IMPORTANT]
> This project requires **Ollama** running on your computer. Ollama is a separate
> app, not a Python package, so `pip` will not install it.
> 1. Download and install Ollama from [ollama.com](https://ollama.com)
> 2. Download the model: `ollama pull llama3.2:1b`
> 3. Make sure Ollama is running (open the Ollama app or run `ollama serve`)
>
> If Ollama isn't running, the script will stop with the message
> "Could not connect to Ollama."

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running
- The `llama3.2:1b` model
- The `requests` library

## Setup

```bash
# Pull the model
ollama pull llama3.2:1b

# Install dependencies
python -m pip install requests
```

## Usage

Make sure Ollama is running (open the Ollama app or run `ollama serve`), then:

```bash
python ollama_explorer.py
```

The full run makes 11 model calls and takes a few minutes on a typical laptop.

## How It Works

The script is built around one helper function:

```python
generate(prompt, system=None, temperature=None) -> (response_text, seconds_taken)
```

- Sends a request to `http://localhost:11434/api/chat` with `"stream": False`
- Adds a system message only when one is given
- Passes temperature inside `"options"` (Ollama ignores a top-level `temperature` key)
- Times the request with `time.time()` and returns both the text and the elapsed seconds

A second helper, `show()`, prints each result with a label and its response time.

## Experiments

### 1. Same question, different system prompts
Asks "What is an API?" three times:
- (a) no system prompt
- (b) "Explain like I am 5 years old"
- (c) "You are a senior software architect. Be technical and precise."

### 2. RAG-style context grounding
Gives the model a short paragraph defining an API, with a system prompt telling it to answer only from the context and say "I don't know" otherwise. It then asks:
- (a) a question the context answers: "What is an API?"
- (b) a question it doesn't: "What is the capital of the United States?"

### 3. Response timing
Asks questions of 5, 20, and 50 words. The script prints a summary table of question length, response time, and answer length.

### 4. Temperature
Asks "What is an API?" twice at temperature 0.1 and twice at temperature 1.0 to compare how consistent the answers are.

## Findings

### Experiment 1
The system prompt clearly changed the tone and depth of the answers:
- **No system prompt:** a general explanation with an analogy, bullet lists, and API types (~42s).
- **Explain like I'm 5:** simpler language and a lemonade-stand story. It was the fastest (~31s) because the answer was shorter.
- **Senior architect:** more technical, covering abstraction, decoupling, endpoints, HTTP methods, and headers (~42s).

Both the default and architect answers expanded REST as "Representational State of Resource." The correct expansion is **Representational State Transfer**. A "technical and precise" persona does not make a small model more accurate. It only changes the style.

### Experiment 2
The model answered "I don't know" to **both** questions.
- (b) The capital question was correctly refused, even though the model knows the answer from training. That is good grounding.
- (a) "What is an API?" was **wrongly refused**, even though the context defines an API directly.

The strict refusal instruction caused the 1B model to over-refuse. This shows a real tradeoff in RAG systems: loose instructions lead to made-up answers, and strict instructions can make the model refuse answers that are right in the context.

### Experiment 3
| Question | Words | Seconds | Answer words |
|----------|------:|--------:|-------------:|
| Short    | 5     | 38.11   |              |
| Medium   | 20    |         |              |
| Long     | 50    |         |              |

*Fill in from the summary table the script prints.* Compare whether response time follows question length or answer length.

### Experiment 4
*Fill in after running:* Were the two 0.1 runs nearly identical? How different were the two 1.0 runs?

## Takeaways
- System prompts are an effective way to control tone and audience, but not accuracy.
- Response time on a local model depends mostly on how much text the model generates.
- Grounding instructions need careful wording. Small models tend to follow them too literally.