# Unit 1 Assignment: answers PES2UG23CS913



## Observation Table 

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



