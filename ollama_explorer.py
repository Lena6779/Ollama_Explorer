import time
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

def generate(prompt, system=None, temperature=None):
    """Send a chat request to ollama. Returns(response_text, seconds_taken)"""
    messages = []
    if system:
        messages.append({"role":"system", "content":system})
    messages.append({"role":"user", "content":prompt})
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    } 
    
    if temperature is not None:
        payload["options"] = {"temperature": temperature}  
    
    start = time.time()
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    elapsed_time = time.time() - start
    
    return response.json()["message"]["content"], elapsed_time

# Helper function to display the results
def show(label, text, elapsed_time):     
    print(f"--- {label} ---")
    print(text)
    print(f"Time taken: {elapsed_time:.2f} seconds\n")
    
question = "What is an API?"

def experiment_1():
    """Same question, different system prompts"""
    print("\nExperiment 1: Same question, different system prompts\n")
    question = "What is an API?"
    system_prompts = {
        "(a) no system prompt":None,
        "(b) Explain like I am 5": "Explain like I am 5 years old",
        "(c) Senior architect": "You are a senior software architect. Be technical and precise."
    }
    for label, system_prompt in system_prompts.items():
        text, elapsed_time = generate(question, system=system_prompt)
        show(label, text, elapsed_time)
        
def experiment_2():
    """RAG-style context grounding"""
    print("\nExperiment 2: RAG-style context grounding\n")
    context = """An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information. APIs are essential for enabling integration between different systems, allowing developers to build applications that can leverage existing services and data."""
    system = ("Answer the user's question based on the provided context. If the answer is not in the context, say 'I don't know.' and do not make up an answer.")

    questions = {
        "(a) Direct question": question,
        "(b) Cannot be answered from context": "What is the capital of the United States?"
    }
    
    for label, q in questions.items():
        prompt = f"Context: {context}\n\nQuestion: {q}"
        text, elapsed_time = generate(prompt, system=system)
        show(f"{label}: {q}", text, elapsed_time)
        
def experiment_3():
    """Response Timing"""
    print("\nExperiment 3: Response Timing\n")
    questions = {
        "(a) Short question": "What is an API, exactly?",
        "(b) Medium question": "Can you explain what an API is, including its purpose, "
                               "how it works, and provide examples of APIs used today?",
        "(c) Long question": "Can you provide an overview of what an API (Application "
                             "Programming Interface) is, including its definition, purpose, "
                             "how it functions in software development, the different types "
                             "of APIs available (such as REST, SOAP, and GraphQL), and examples "
                             "of how APIs are used in real-world applications to connect "
                             "different software systems?",
    }
    results = []
    for label, q in questions.items():
        text, elapsed_time = generate(q)
        results.append((label, len(q.split()), elapsed_time, len(text.split())))
        show(f"{label}: ({len(q.split())} words)", text, elapsed_time)

    print("\nSummary of response times:")
    print(f"{'Length':<22}{'Q words':>9}{'Seconds':>10}{'Answer words':>14}")
    for label, q_words, elapsed, a_words in results:
        print(f"{label:<22}{q_words:>9}{elapsed:>10.2f}{a_words:>14}")
     
def experiment_4():
    """Temperature variation 0.1 and 1.0"""
    print("\nExperiment 4: Temperature variation\n")
    temperatures = {
        "(a) Low temperature (0.1)": 0.1,
        "(b) High temperature (1.0)": 1.0
    }
    for label, temp in temperatures.items():
        for run in (1, 2):
            text, elapsed_time = generate(question, temperature=temp)
            show(f"{label}: (temperature={temp}), run {run}", text, elapsed_time)
            
def main():
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
    
if __name__ == "__main__":
    main()