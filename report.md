# Evaluation Report: Offline LLM Chatbot Performance

## Introduction
The goal of this project was to evaluate the feasibility of deploying a local Large Language Model (LLM) — Meta's Llama 3.2 3B via Ollama — as an automated customer support chatbot for a fictional e-commerce store, 'Chic Boutique'. By operating locally, no sensitive customer data is transmitted over the internet, thereby ensuring data privacy and removing repetitive API costs. The experiment focused on evaluating the model's capabilities and comparing two prompt engineering techniques: zero-shot and one-shot prompting.

## Methodology
- **Data Source**: Reused 20 diverse, realistic user queries representing common customer support issues. These were adapted from the Ubuntu Dialogue Corpus to fit an e-commerce context.
- **Model**: Meta's Llama 3.2 3B parameter model, executed locally using the Ollama inference server.
- **Prompt Engineering**:
  - **Zero-Shot**: Provided the model with a basic role description and context ("You are a helpful... customer support agent") along with the user query, without any examples.
  - **One-Shot**: Provided the model with the same role description, plus one complete, hardcoded example of an ideal query-response pair (specifically outlining the return policy).
- **Evaluation Criteria** (Scored Manually from 1-5):
  - **Relevance**: How well the response addressed the customer's query.
  - **Coherence**: Grammatical correctness and ease of understanding.
  - **Helpfulness**: Usefulness and actionability of the answer.

## Results & Analysis

| Method | Avg Relevance | Avg Coherence | Avg Helpfulness |
|---|---|---|---|
| Zero-Shot | 3.65 | 5.00 | 2.95 |
| One-Shot | 5.00 | 5.00 | 5.00 |

### Analysis
There is a stark difference in quality and tone between the zero-shot and one-shot responses:

- **Zero-Shot Observations**:
  - The model was consistently **coherent** (scoring 5 across almost all queries). It formed grammatically correct, sensible sentences.
  - However, it struggled with **helpfulness** and generating appropriately empathetic customer service tones. Responses like "Returns can be processed for wrong items." are technically relevant but lack the friendliness and direct actionability typically expected.
  - In several cases where it didn't inherently know policy (e.g., "Do you offer gift wrapping services?"), it simply admitted ignorance rather than gracefully making up a plausible corporate response (due to the explicit prompt instruction not to make things up). While rule-abiding, this yields a low helpfulness score (1 or 2). 

- **One-Shot Observations**:
  - Providing just a single example dramatically shifted the model's output quality. The responses instantly adopted a friendly, empathetic, and actionable tone (e.g., "I'm so sorry! Please reply to this with a photo...").
  - The model effectively extrapolated the desired formatting and "Chic Boutique" persona from the solitary example, showcasing Llama 3.2's remarkable ability for in-context learning.
  - It successfully generated plausible policies for things like international shipping and gift wrapping without hallucinating dangerous out-of-character actions.

## Conclusion & Limitations
The Meta Llama 3.2 3B model, when run locally via Ollama, is highly capable of acting as a first-line customer support chatbot. A crucial finding is that **one-shot prompting significantly outperforms zero-shot prompting**, acting as a simple but powerful multiplier for response helpfulness and tone shaping.

**Limitations**:
- **Lack of Real-world Integration**: This proof-of-concept operates in a vacuum. A real deployment requires access to a company's internal databases to look up specific, real-time context like a user's order number or active inventory, something the LLM cannot do alone without a Retrieval-Augmented Generation (RAG) architecture or tool-use capabilities.
- **Hardware Bottlenecks**: Running inference on a local CPU can be slow depending on the exact hardware capabilities, which creates latency that real-time users might find unacceptable compared to cloud-hosted APIs.

**Next Steps**: 
The logical next step is implementing RAG (Retrieval-Augmented Generation). By feeding the context window with the company's real documentation and user history alongside the query, the chatbot could provide completely grounded, fact-based support, overcoming the risk of minor policy hallucinations while maintaining 100% data privacy.
