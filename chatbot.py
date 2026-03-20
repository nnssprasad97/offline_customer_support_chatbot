import requests
import json
import os

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

def query_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False 
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        response.raise_for_status() 
        return json.loads(response.text).get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "Error: Could not get a response from the model."

def main():
    # Ensure required directories exist
    os.makedirs("eval", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)

    # Load prompt templates
    try:
        with open("prompts/zero_shot_template.txt", "r") as f:
            zero_shot_template = f.read()
        with open("prompts/one_shot_template.txt", "r") as f:
            one_shot_template = f.read()
    except FileNotFoundError:
        print("Error: Prompt templates not found. Ensure they exist in the 'prompts/' directory.")
        return

    # 20 Adapted E-commerce Queries
    queries = [
        "How do I track my order?",
        "My discount code isn't working at checkout.",
        "Do you ship internationally?",
        "Can I change my shipping address after placing an order?",
        "I received the wrong item in my package.",
        "How do I reset my account password?",
        "What payment methods do you accept?",
        "The item I want is out of stock. When will it be back?",
        "Can I cancel my order?",
        "Where can I find the sizing guide for dresses?",
        "My package arrived damaged, what should I do?",
        "Do you offer gift wrapping services?",
        "How long does standard shipping take?",
        "Can I apply two promo codes to one order?",
        "I didn't receive an order confirmation email.",
        "How do I delete my account?",
        "Do you have a physical retail store I can visit?",
        "What is the warranty policy on your electronics?",
        "How do I contact a human customer service agent?",
        "Are your products ethically sourced?"
    ]

    print("Starting inference. This may take a few minutes depending on your hardware...\n")

    with open("eval/results.md", "w") as f:
        # Write the Markdown table header and rubric
        f.write("# Evaluation Results\n\n")
        f.write("### Scoring Rubric:\n")
        f.write("* **Relevance (1-5):** How well does the response address the customer's query?\n")
        f.write("* **Coherence (1-5):** Is the response grammatically correct and easy to understand?\n")
        f.write("* **Helpfulness (1-5):** Does the response provide a useful, actionable answer?\n\n")
        f.write("| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n")
        f.write("|---|---|---|---|---|---|---|\n")

        for i, query in enumerate(queries, 1):
            print(f"Processing Query {i}/20: {query}")

            # Run Zero-Shot
            zs_prompt = zero_shot_template.replace("{query}", query)
            zs_response = query_ollama(zs_prompt).replace("\n", " ") # Remove newlines to avoid breaking the markdown table
            f.write(f"| {i} | {query} | Zero-Shot | {zs_response} |  |  |  |\n")

            # Run One-Shot
            os_prompt = one_shot_template.replace("{query}", query)
            os_response = query_ollama(os_prompt).replace("\n", " ")
            f.write(f"| {i} | {query} | One-Shot | {os_response} |  |  |  |\n")
            
    print("\nDone! Results written to eval/results.md. Open the file to add your manual scores.")

if __name__ == "__main__":
    main()
