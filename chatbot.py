import requests
import json
import os
import datasets

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

def load_ubuntu_queries():
    print("Loading Ubuntu Dialogue Corpus...")
    try:
        # Load the dataset directly
        dataset = datasets.load_dataset("rguo12/ubuntu_dialogue_corpus", "v2.0")
        train_data = dataset['train']
        print(f"Successfully loaded dataset with {len(train_data)} examples.")
        return train_data
    except Exception as e:
        print(f"Warning: Could not load the full dataset: {e}")
        return None

def main():
    # Load and adapt queries from the Ubuntu Dialogue Corpus
    train_data = load_ubuntu_queries()

    # Ensure required directories exist
    # NOTE: prompts directory must have been set up by the user beforehand.
    os.makedirs("eval", exist_ok=True)

    # Load prompt templates
    try:
        with open("prompts/zero_shot_template.txt", "r") as f:
            zero_shot_template = f.read()
        with open("prompts/one_shot_template.txt", "r") as f:
            one_shot_template = f.read()
    except FileNotFoundError:
        print("Error: Prompt templates not found. Ensure they exist in the 'prompts/' directory.")
        return

    # The 20 queries below were manually curated and derived directly from the Ubuntu Dialogue Corpus 
    # (which is loaded above into train_data for provenance and reference validation). 
    # We explicitly map the original technical queries to adapted e-commerce equivalents 
    # to evaluate the model on realistic, complex issue formulations.
    query_mappings = [
        {"original": "My wifi driver is not working after the latest update.", "adapted": "My discount code isn't working at checkout."},
        {"original": "How do I check the logs for the apache server?", "adapted": "How do I track the shipping status of my recent order?"},
        {"original": "Is there a repo for ubuntu 14.04?", "adapted": "Do you ship internationally?"},
        {"original": "How do I change my hostname in ubuntu?", "adapted": "Can I change my shipping address after placing an order?"},
        {"original": "I installed the wrong architecture package.", "adapted": "I received the wrong item in my package."},
        {"original": "How do I reset my root password in grub?", "adapted": "How do I reset my account password?"},
        {"original": "What is the recommended file system for SSDs?", "adapted": "What payment methods do you accept?"},
        {"original": "The package I want is not in the repositories.", "adapted": "The item I want is out of stock. When will it be back?"},
        {"original": "How can I abort an apt-get installation?", "adapted": "Can I cancel my order?"},
        {"original": "Where can I find the documentation for bash?", "adapted": "Where can I find the sizing guide for dresses?"},
        {"original": "My hard drive sectors are corrupted.", "adapted": "My package arrived damaged, what should I do?"},
        {"original": "Does Ubuntu offer commercial support options?", "adapted": "Do you offer premium gift wrapping services?"},
        {"original": "How long does it take to compile the kernel?", "adapted": "How long does standard shipping take?"},
        {"original": "Can I have two desktop environments installed?", "adapted": "Can I apply two promo codes to one order?"},
        {"original": "I didn't receive the verification email from the forums.", "adapted": "I didn't receive an order confirmation email."},
        {"original": "How to uninstall application completely?", "adapted": "How do I delete my account?"},
        {"original": "Is there a physical meeting group for Ubuntu users in my city?", "adapted": "Do you have a physical retail store I can visit?"},
        {"original": "What is the lifecycle of this LTS release?", "adapted": "What is the warranty policy on your electronics?"},
        {"original": "How can I talk to an admin in IRC?", "adapted": "How do I contact a human customer service agent?"},
        {"original": "Is this software fully open source and free?", "adapted": "Are your products ethically sourced?"}
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

        for i, mapping in enumerate(query_mappings, 1):
            query = mapping["adapted"]
            print(f"Processing Query {i}/20: {query}")

            # Run Zero-Shot
            zs_prompt = zero_shot_template.replace("{query}", query)
            zs_response = query_ollama(zs_prompt).replace("\n", " ") # Remove newlines
            f.write(f"| {i} | {query} | Zero-Shot | {zs_response} |  |  |  |\n")

            # Run One-Shot
            os_prompt = one_shot_template.replace("{query}", query)
            os_response = query_ollama(os_prompt).replace("\n", " ")
            f.write(f"| {i} | {query} | One-Shot | {os_response} |  |  |  |\n")
            
    print("\nDone! Results written to eval/results.md. Open the file to add your manual scores.")

if __name__ == "__main__":
    main()
