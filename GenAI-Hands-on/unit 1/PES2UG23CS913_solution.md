# Unit 1 Assignment: answers PES2UG23CS913

## The Models to Test


## Experiment 1: Text Generation

**Task**: Generate text using the prompt: `"The future of Artificial Intelligence is"`

### BERT Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **FAILURE** |
| **Observation** | BERT will throw an error or produce incomprehensible output. It may try to output random tokens from its vocabulary or fail completely. |
| **Why This Happened** | BERT is an **Encoder-only** model. It processes input to create contextualized representations but has no decoder to generate new tokens autoregressively (one at a time). The model is not trained for next-token prediction, which is essential for text generation. |
| **Architectural Reason** | Encoder-only models are designed to bidirectionally understand context by attending to all tokens simultaneously. They cannot predict what comes "next" because they process the entire sequence at once, not sequentially. |

### RoBERTa Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **FAILURE** |
| **Observation** | Similar to BERT, RoBERTa will fail or produce nonsensical output. No meaningful text generation occurs. |
| **Why This Happened** | RoBERTa is also an **Encoder-only** model, just with better preprocessing and training. It has the same architectural limitation as BERT - no decoder for sequential generation. |
| **Architectural Reason** | RoBERTa inherits the same Encoder-only architecture from BERT. Even with improved training, without a decoder, it cannot generate tokens sequentially. Text generation requires a decoder that can attend to previously generated tokens. |

### BART Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **SUCCESS** |
| **Observation** | BART successfully generates coherent continuations. Example output: `"The future of Artificial Intelligence is bright and full of possibilities..."` The output is meaningful and contextually relevant. |
| **Why This Happened** | BART is an **Encoder-Decoder** model. It encodes the input prompt and uses its decoder to generate new tokens sequentially, attending to both the input and previously generated tokens. |
| **Architectural Reason** | BART's decoder can predict the next token given the sequence so far. It has a causal attention mask (can only attend to previous tokens), making it suitable for autoregressive generation. This is the standard architecture for language generation models. |

---

## Experiment 2: Masked Language Modeling (Missing Word Prediction)

**Task**: Predict the missing word in: `"The goal of Generative AI is to [MASK] new content."`

### BERT Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **SUCCESS** |
| **Observation** | BERT predicts appropriate words like: `'create'`, `'generate'`, `'produce'`, `'make'`. The predictions are semantically correct and contextually relevant. |
| **Why This Happened** | BERT was explicitly trained on Masked Language Modeling (MLM) as its primary objective. MLM is the core training task where random tokens are masked, and the model learns to predict them. |
| **Architectural Reason** | BERT's bidirectional encoder allows it to see context from both left and right sides of the [MASK] token. This bidirectional context is perfect for predicting what word should be masked. The model's attention mechanism can simultaneously process all surrounding tokens to make a prediction. |

### RoBERTa Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **SUCCESS** |
| **Observation** | RoBERTa predicts similar words: `'create'`, `'generate'`, `'produce'`, `'build'`. Performance is comparable or slightly better than BERT. |
| **Why This Happened** | RoBERTa was also trained on MLM and was built specifically to improve upon BERT's MLM training. It uses better preprocessing and training procedures. |
| **Architectural Reason** | RoBERTa uses the same MLM approach as BERT but with improved training techniques. The bidirectional nature of the encoder makes it highly effective for this task. The architectural advantage is the same as BERT. |

### BART Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **PARTIAL/MODERATE SUCCESS** |
| **Observation** | BART can predict missing words but may not perform as well as BERT/RoBERTa on this specific task. It was not trained specifically for MLM, so predictions might be less accurate. |
| **Why This Happened** | BART was trained on a different objective: denoising autoencoding. While it can handle masked input, it's not its primary training objective like it is for BERT/RoBERTa. |
| **Architectural Reason** | BART's encoder-decoder design gives it some ability to predict masked tokens (through the decoder), but the bidirectional attention of BERT/RoBERTa makes them more optimal for this task. BART is optimized for generation tasks, not masked prediction. |

---

## Experiment 3: Question Answering

**Task**: Answer the question `"What are the risks?"` based on context: `"Generative AI poses significant risks such as hallucinations, bias, and deepfakes."`

### BERT Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **PARTIAL/POOR** |
| **Observation** | Base BERT (not fine-tuned on SQuAD) may produce incorrect answers or random spans from the text. It might extract "significant risks", "hallucinations", "bias", but without proper training, performance is unreliable. |
| **Why This Happened** | BERT-base was not fine-tuned on QA datasets like SQuAD. While BERT can be used for QA, the base model doesn't have task-specific weights. Generic encoder models need fine-tuning for reliable QA performance. |
| **Architectural Reason** | Encoder models can identify relevant spans through attention, but without task-specific training, they struggle. The model lacks a QA head that ranks answer spans properly. BERT is not inherently designed for question-answering. |

### RoBERTa Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **PARTIAL/POOR** |
| **Observation** | Similar to BERT, base RoBERTa produces unreliable answers. It might extract "hallucinations, bias, and deepfakes" or similar, but confidence is low and accuracy varies. |
| **Why This Happened** | RoBERTa-base is also not fine-tuned for QA. Like BERT, it requires fine-tuning on QA datasets to perform well. The base model lacks the necessary task-specific adaptation. |
| **Architectural Reason** | Both encoder-only models can identify relevant regions of text through attention, but without QA-specific training, they cannot reliably rank and extract answer spans. They need a task head and QA-specific loss function. |

### BART Result
| Aspect | Detail |
|--------|--------|
| **Classification** | **MODERATE/POOR** |
| **Observation** | BART may generate answers rather than extract them: `"The risks include hallucinations, bias, and deepfakes."` The answer is conceptually correct but formatted differently (generated rather than extracted). |
| **Why This Happened** | BART is a generative model trained for seq2seq tasks. It tends to generate answers rather than extract spans from the context. For extractive QA, this is not ideal. BART is designed for abstractive tasks, not extractive ones. |
| **Architectural Reason** | BART's encoder-decoder architecture makes it generate sequences rather than identify spans. The decoder is trained to produce tokens, not to classify tokens as answer positions. For extractive QA, span classification (encoder-only with QA head) is more suitable. |

---

## Observation Table - Summary

| Task | Model | Classification | Observation | Why? (Architectural Reason) |
|------|-------|-----------------|-------------|---------------------------|
| **Generation** | BERT | Failure | Cannot generate; produces errors or nonsense | Encoder-only; no decoder for sequential token generation |
| | RoBERTa | Failure | Cannot generate; similar limitation to BERT | Encoder-only; lacks generative decoder component |
| | BART | Success | Generates coherent text continuations | Encoder-Decoder; decoder can autoregressively generate tokens |
| **Fill-Mask** | BERT | Success | Predicts 'create', 'generate', etc. correctly | Trained on MLM; bidirectional attention optimal for this task |
| | RoBERTa | Success | Similar/better performance than BERT | Trained on improved MLM; bidirectional attention |
| | BART | Partial Success | Predicts but less accurate than BERT/RoBERTa | Not trained on MLM; encoder-decoder not optimized for this |
| **QA** | BERT | Partial/Poor | Unreliable extraction without fine-tuning | Base model lacks QA-specific training; needs task adaptation |
| | RoBERTa | Partial/Poor | Similar poor performance to BERT | Base model not fine-tuned for QA; requires SQuAD training |
| | BART | Moderate/Poor | Generates answers instead of extracting | Generative architecture; designed for abstractive tasks, not extractive |

---

## Key Takeaways

### 1. Architecture Determines Capability
- **Encoder-Only** (BERT, RoBERTa): Best for understanding, classification, MLM tasks. Cannot generate.
- **Encoder-Decoder** (BART): Best for generation, translation, summarization. Can also perform other tasks.

### 2. Training Matters
- A model's training objective is as important as its architecture. BERT trained on MLM excels at masked prediction.
- Fine-tuning on specific tasks (like SQuAD for QA) dramatically improves performance.

### 3. Task-Model Alignment
- Choosing the right model for the right task is crucial.
- Forcing models to perform tasks they're not designed for reveals architectural limitations.

### 4. Encoder-Decoder Flexibility
- BART's encoder-decoder design makes it more flexible for various tasks, even if it's not always optimal for each.
- Encoders are specialized but cannot generate; decoders are necessary for generation.

---

## Practical Implementation Notes

From the HandsOn-1_Unit1.ipynb notebook, we learned:

1. **Tokenization**: All models require converting text to tokens and token IDs before processing.
2. **Pipelines**: The `pipeline()` function abstracts away complexity, but understanding the underlying architecture is crucial.
3. **BERT vs. Alternatives**: Different models (BERT, RoBERTa, BART) serve different purposes.
4. **Testing Limitations**: Testing models on tasks they're not designed for (like generation with BERT) reveals why architectural choices matter.

---

## Conclusion

This assignment demonstrates that **architecture is destiny** in machine learning. A model's design determines what it can and cannot do. Understanding whether a model is encoder-only, encoder-decoder, or decoder-only is fundamental to choosing the right tool for your task.

- Use **BERT/RoBERTa** for understanding and classification tasks.
- Use **BART** (or other encoder-decoders) for generation tasks.
- Always consider fine-tuning on your specific task for optimal performance.
