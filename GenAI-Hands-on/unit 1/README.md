# Unit 1: Generative AI & NLP Fundamentals

Welcome to the practical session for Unit 1. This folder contains two key components designed to give you a hands-on understanding of Large Language Models (LLMs) and the Hugging Face ecosystem.

## 1. The Interactive Tutorial (`HandsOn-1_Unit1.ipynb`)

**Goal**: To verify your understanding of the NLP pipeline and witness the difference between "Fast" and "High-Quality" models.

**What you will do:**
*   **Hugging Face Setup**: Learn how to use the `transformers` library and the `pipeline()` function.
*   **Model Comparison**: You will verify the performance difference between a small model (`distilgpt2`) and a standard model (`gpt2`) on the same prompt.
*   **NLP Fundamentals**: visualizing what happens "under the hood" (Tokenization, POS Tagging, NER).
*   **Advanced Tasks**: Run experiments with Summarization (Fast vs. Detailed) and Masked Language Modeling.

**Action Item**: Open the notebook, run the cells step-by-step, and read the detailed explanations provided.

---

## 2. The Assignment: The Benchmark Challenge (`Questions_Unit1.md`)

**Goal**: To investigate the architectural limitations of different model types by forcing them to perform tasks they may not be designed for.

**What you will do:**
You are required to create a **new Jupyter Notebook** (`Unit1_Benchmark.ipynb`) and conduct a comparative study.

**The Experiment:**
You will take three specific models:
1.  **BERT** (`bert-base-uncased`)
2.  **RoBERTa** (`roberta-base`)
3.  **BART** (`facebook/bart-base`)

And run **all three models** on the following three tasks:
1.  **Text Generation**: Prompt them to complete a sentence.
2.  **Fill-Mask**: Ask them to predict a missing word.
3.  **Question Answering**: Ask them to answer a specific question based on a context.

**Your Task:**
*   Execute the code for every combination (3 Models x 3 Tasks).
*   **Observe the outputs carefully.** Does the model generate fluent English? Does it output gibberish? Does it fail completely?
*   **Record your findings** in the **Observation Table** provided in `Questions_Unit1.md`.
*   You must explain *why* a certain model behaved the way it did based on its architecture (Encoder vs. Decoder vs. Encoder-Decoder).

> **Note**: There are no "wrong" experiments here. If a model fails or outputs nonsense, that is a valid observation! Your job is to document it.
