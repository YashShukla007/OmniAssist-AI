# Final Model Evaluation

## Project

**OmniAssist AI – Customer Support Assistant**

---

# Objective

The objective of this evaluation is to analyze the complete fine-tuning pipeline and compare the performance of the following models:

- Base Model
- Supervised Fine-Tuned (SFT) Model
- Direct Preference Optimization (DPO) Model

The evaluation measures how parameter-efficient fine-tuning improves the quality, consistency, and domain relevance of customer support responses.

---

# Models Evaluated

| Model | Description |
|--------|-------------|
| Qwen Base | Original Qwen2.5-1.5B-Instruct model without fine-tuning |
| Qwen SFT | LoRA adapter trained using the Customer Support instruction dataset |
| Qwen DPO | LoRA adapter further optimized using Direct Preference Optimization |

---

# Evaluation Dataset

The evaluation was performed using a predefined set of customer support prompts covering common customer service scenarios, including:

- Order cancellation
- Refund requests
- Shipping address updates
- Delivery delays
- Damaged products
- Order tracking
- Incorrect delivery address
- Payment failures
- Product returns
- Customer support contact

These prompts were used consistently across all three models to ensure a fair comparison.

---

# Evaluation Methodology

The generated responses were analyzed using both qualitative and quantitative evaluation methods.

## Qualitative Evaluation

Each response was assessed for:

- Correctness
- Domain relevance
- Clarity
- Helpfulness
- Professional tone
- Response consistency
- Customer support behavior

---

## Automatic Evaluation Metrics

The comparison framework automatically computes the following NLP evaluation metrics:

| Metric | Purpose |
|---------|---------|
| BLEU | Measures lexical overlap between generated and reference responses |
| ROUGE-1 | Measures unigram similarity |
| ROUGE-2 | Measures bigram similarity |
| ROUGE-L | Measures longest common subsequence similarity |
| BERTScore | Measures semantic similarity using contextual embeddings |

These metrics provide both lexical and semantic evaluation of generated responses.

---

# Metric Summary

The comparison framework evaluates each generated response individually using the following NLP metrics:

- BLEU
- ROUGE-1
- ROUGE-2
- ROUGE-L
- BERTScore

At the current stage of the project, the evaluation is performed on a **per-prompt basis**, allowing detailed analysis of each model's response for every evaluation prompt.

The generated comparison reports include prompt-wise metric values, enabling qualitative and quantitative comparison between the Base, SFT, and DPO models.

Future versions of the evaluation pipeline can be extended to compute aggregate statistics such as average BLEU, average ROUGE scores, and average BERTScore across all evaluation prompts.

---

# Future Enhancement of the Evaluation Framework

The current evaluation pipeline computes NLP metrics for each evaluation prompt individually, enabling detailed prompt-wise analysis of the generated responses.

As a future enhancement, the comparison framework will be extended to automatically compute aggregate evaluation statistics across all prompts.

The planned improvements include:

- Average BLEU Score
- Average ROUGE-1 Score
- Average ROUGE-2 Score
- Average ROUGE-L Score
- Average BERTScore

The future evaluation report will also include a consolidated comparison table similar to the following format:

| Metric | Base Model | SFT Model | DPO Model |
|---------|-----------:|----------:|----------:|
| Average BLEU | To Be Added | To Be Added | To Be Added |
| Average ROUGE-1 | To Be Added | To Be Added | To Be Added |
| Average ROUGE-2 | To Be Added | To Be Added | To Be Added |
| Average ROUGE-L | To Be Added | To Be Added | To Be Added |
| Average BERTScore | To Be Added | To Be Added | To Be Added |

This enhancement will provide a concise quantitative summary of model performance while complementing the existing prompt-wise evaluation. The current implementation already generates detailed metrics for every evaluation prompt, and aggregate statistics will be incorporated in a future version of the project.

---

# Overall Observations

## Base Model

The pretrained model demonstrates strong general language understanding and produces coherent responses.

However, the responses are generally generic and lack customer support domain specialization.

Strengths include:

- Fluent language generation
- Good reasoning ability
- Safe responses
- Professional tone

Limitations include:

- Generic recommendations
- Limited customer support workflow knowledge
- Lower response consistency
- Limited task-specific guidance

---

## Supervised Fine-Tuned (SFT) Model

The SFT model demonstrates clear improvements over the base model.

Observed improvements include:

- Better instruction following
- Improved domain-specific terminology
- More structured responses
- Better consistency
- Improved customer support workflow understanding

The model responds in a more professional and task-oriented manner.

---

## Direct Preference Optimization (DPO) Model

The DPO model further refines the SFT model by learning preferred response behavior.

Observed improvements include:

- Improved response alignment
- Better conversational flow
- More natural responses
- Improved response prioritization
- Better overall customer interaction quality

The DPO stage helps optimize responses beyond supervised learning by incorporating preference information.

---

# Comparative Analysis

| Evaluation Aspect | Base | SFT | DPO |
|-------------------|------|-----|-----|
| Domain Knowledge | Moderate | High | High |
| Instruction Following | Moderate | High | Very High |
| Response Structure | Moderate | High | Very High |
| Customer Support Style | Moderate | High | Very High |
| Response Consistency | Moderate | High | Very High |
| Professional Tone | Good | Better | Best |
| Helpfulness | Moderate | High | Very High |

---

# Automatic Metric Summary

The comparison framework evaluated every generated response using BLEU, ROUGE, and BERTScore metrics.

General observations include:

- BERTScore remained consistently high across all models, indicating strong semantic understanding.
- ROUGE scores improved for several prompts after fine-tuning, reflecting better lexical alignment with reference responses.
- BLEU scores remained relatively low because multiple valid customer support responses can exist for the same query, making exact lexical overlap less representative of response quality.
- The combination of lexical and semantic metrics provides a more balanced evaluation than relying on any single metric.

---

# Key Achievements

The project successfully demonstrates:

- Dataset preprocessing
- Instruction dataset generation
- Preference dataset generation
- Parameter-Efficient Fine-Tuning (PEFT)
- LoRA adaptation
- QLoRA-based training
- Supervised Fine-Tuning (SFT)
- Direct Preference Optimization (DPO)
- Adapter-based inference
- Automatic evaluation
- Multi-model comparison
- BLEU evaluation
- ROUGE evaluation
- BERTScore evaluation
- Markdown report generation

---

# Limitations

Although the fine-tuned models perform better than the pretrained model, a few limitations remain:

- Training was performed on a subset of the available dataset due to Google Colab Free Tier resource constraints.
- The project starts from the instruction-tuned **Qwen2.5-1.5B-Instruct** model and therefore focuses on instruction fine-tuning followed by Direct Preference Optimization.
- Some generated responses still reflect placeholder values inherited from the training dataset.

These limitations provide opportunities for future improvements.

---

# Future Work

Possible extensions include:

- Training on the complete dataset
- Larger preference datasets
- Human evaluation
- RAG integration
- Tool calling
- Function calling
- Multi-turn conversation evaluation
- Deployment as a production-ready customer support assistant

---

# Conclusion

The OmniAssist AI fine-tuning pipeline successfully demonstrates a complete parameter-efficient post-training workflow for Large Language Models.

Starting from the pretrained **Qwen2.5-1.5B-Instruct** model, the project applies Supervised Fine-Tuning followed by Direct Preference Optimization to adapt the model for the Customer Support domain.

The evaluation results show that the fine-tuned models produce more structured, consistent, and domain-relevant responses compared to the original base model while maintaining strong semantic understanding.

The modular architecture of the project further enables easy extension to new domains, datasets, and future alignment techniques.