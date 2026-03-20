# Offline Customer Support Chatbot

This project implements an offline customer support chatbot using Ollama and the Llama 3.2 3B model. It demonstrates the feasibility and benefits of a local LLM deployment for handling sensitive customer inquiries, ensuring data privacy, and exploring the effectiveness of zero-shot versus one-shot prompt engineering techniques.

## Features
- Complete offline inference ensuring zero transmission of customer data.
- Comparison of zero-shot and one-shot prompting strategies.
- 20 adapted real-world queries evaluated.
- Automated generation of a Markdown logging and scoring table.

## Project Structure
- `chatbot.py`: Main executable script for running the chat evaluations.
- `prompts/zero_shot_template.txt`: Prompt template without examples.
- `prompts/one_shot_template.txt`: Prompt template with a single query-response example.
- `eval/results.md`: Auto-generated table containing responses to all queries and scores.
- `report.md`: Detailed analysis of performance using evaluation metrics.
- `setup.md`: Setup guide and instructions.

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/)
- Llama 3.2 3B parameter model in Ollama.
