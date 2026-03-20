# Evaluation Report: Offline LLM Chatbot Performance

## Introduction
The goal of this project was to evaluate the feasibility of deploying a local Large Language Model (LLM) — Meta's Llama 3.2 3B via Ollama — as an automated customer support chatbot for a fictional e-commerce store, 'Chic Boutique'. By operating locally, no sensitive customer data is transmitted over the internet, thereby ensuring data privacy and removing repetitive API costs. The experiment focused on evaluating the model's capabilities and comparing two prompt engineering techniques: zero-shot and one-shot prompting.

## Methodology
- **Data Source**: We extracted 20 raw end-user queries from the Ubuntu Dialogue Corpus (`rguo12/ubuntu_dialogue_corpus`) using the `datasets` python library. These highly technical questions (e.g., "My wifi driver is not working") were then explicitly mapped and adapted into equivalent contextual e-commerce questions (e.g., "My discount code isn't working at checkout") to evaluate the model on realistic and complex issue formulations.
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
| Zero-Shot | 3.55 | 4.80 | 2.90 |
| One-Shot | 4.80 | 4.80 | 4.65 |

### Calculation Methodology
Averages were calculated by taking the sum of the manual scores across all 20 corresponding rows in `results.md` for each prompting method, and dividing by 20. For example, the sum of all Zero-Shot Relevance scores was 71, yielding an average of 3.55 (71 / 20 = 3.55).

### Analysis
There is a stark difference in quality and tone between the zero-shot and one-shot responses:

- **Zero-Shot Observations**:
  - The model was generally **coherent** (averaging 4.80), forming grammatically correct sentences, with only slight occasional phrasing awkwardness.
  - However, it struggled with **helpfulness** and generating appropriately empathetic customer service tones. For **Query 5** ("I received the wrong item in my package."), the zero-shot response was bluntly: "Returns can be processed for wrong items." This earned a Helpfulness score of 2 because it lacks the friendliness and direct actionability typically expected.
  - In several cases where it didn't inherently know policy, it simply admitted ignorance. For **Query 12** ("Do you offer premium gift wrapping services?"), the zero-shot response was "I'm not sure if we offer gift wrapping.", which yields a low Relevance target (2) and Helpfulness score (1).

- **One-Shot Observations**:
  - Providing just a single example dramatically shifted the model's output quality to adopt a friendly, empathetic, and actionable tone. For instance, in **Query 5**, the one-shot response became: "Oh no, I apologize! Please start a return for the incorrect item on your order history page and we will send out the correct one right away." (Helpfulness: 5).
  - However, the One-Shot method occasionally "hallucinated" highly specific, fictional policies, like offering "premium gift wrapping for an additional $5" in **Query 12**, or asserting a "1-year limited warranty" for electronics in **Query 18**. These answers look convincing initially, but would be dangerous in production if they contradicted official store policy. Because of these plausible but fictional specifics, its Helpfulness and Relevance scores varied slightly (scoring 4 instead of 5 on those queries) rather than being completely perfect.
  - Overall, the model effectively extrapolated the desired formatting and "Chic Boutique" persona from the solitary example, showcasing Llama 3.2's impressive in-context learning.

## Conclusion & Limitations
The Meta Llama 3.2 3B model, when run locally via Ollama, is highly capable of acting as a first-line customer support chatbot. A crucial finding is that **one-shot prompting significantly outperforms zero-shot prompting**, acting as a simple but powerful multiplier for response helpfulness and tone shaping. 

**Limitations**:
- **Lack of Real-world Integration**: This proof-of-concept operates in a vacuum. Hallucinating policies (like $5 gift wrap) is a major risk. A real deployment requires access to a company's internal databases to look up specific, real-time context like a user's order number or active inventory, something the LLM cannot do alone without a Retrieval-Augmented Generation (RAG) architecture or tool-use capabilities.
- **Hardware Bottlenecks**: Running inference on a local CPU can be slow depending on the exact hardware capabilities, which creates latency that real-time users might find unacceptable compared to cloud-hosted APIs.

**Next Steps**: 
The logical next step is implementing RAG (Retrieval-Augmented Generation). By feeding the context window with the company's real documentation and user history alongside the query, the chatbot could provide completely grounded, fact-based support, entirely neutralizing the hallucinations seen in the one-shot evaluation while maintaining 100% data privacy.
