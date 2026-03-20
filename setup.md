# Quick Setup Guide

Follow these steps to configure your environment and run the offline chatbot.

### 1. Install Ollama
Download and install [Ollama](https://ollama.com/) for your operating system (macOS, Windows, or Linux).
After installation, open a terminal/command prompt and verify the installation:
```bash
ollama --version
```

### 2. Pull the Llama 3.2 Model
Download the Meta Llama 3.2 (3B) model onto your local machine:
```bash
ollama pull llama3.2:3b
```
*(This model operates efficiently on CPUs and integrates seamlessly into this project).*

### 3. Setup the Python Environment
Ensure you have Python installed. Navigate to the project directory and create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:
- For macOS/Linux: `source venv/bin/activate`
- For Windows: `venv\Scripts\activate`

Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Ollama app, ensuring it runs into the background.
Finally, start the inference process using the `chatbot.py` script:
```bash
python chatbot.py
```
After the script finishes, open `eval/results.md` to see the generated outputs and add your own manual evaluation scoring!
