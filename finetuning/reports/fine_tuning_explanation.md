# Fine-Tuning Methodology

## Project

**OmniAssist AI – Customer Support Assistant**

---

# Objective

The objective of this project is to adapt a pretrained Large Language Model (LLM) for the Customer Support domain using parameter-efficient fine-tuning techniques.

Instead of training an entire model from scratch, the project leverages modern fine-tuning methods to efficiently specialize the model while significantly reducing computational requirements.

The complete workflow consists of:

1. Dataset Preparation
2. Supervised Fine-Tuning (SFT)
3. Direct Preference Optimization (DPO)
4. Inference
5. Evaluation
6. Model Comparison

---

# Base Model

The project uses the following pretrained model:

| Property | Value |
|----------|-------|
| Model | Qwen2.5-1.5B-Instruct |
| Model Type | Instruction-Tuned Large Language Model |
| Provider | Qwen |
| Parameters | 1.5 Billion |

The base model already possesses strong language understanding and instruction-following capabilities.

This project further specializes the model for Customer Support tasks.

---

# Dataset Preparation

The fine-tuning process begins with dataset preparation.

The preprocessing pipeline performs the following operations:

- Dataset inspection
- Invalid sample removal
- Duplicate removal
- Dataset cleaning
- Chat dataset generation
- Instruction dataset generation
- Preference dataset generation

The generated datasets are stored separately for different training stages.

---

# Instruction Dataset

The instruction dataset follows the standard instruction tuning format.

Example:

```json
{
    "instruction": "How can I cancel my order?",
    "input": "",
    "output": "You can cancel your order by visiting the Orders page before shipment..."
}
```

This dataset is used for Supervised Fine-Tuning.

---

# Preference Dataset

The preference dataset is used for Direct Preference Optimization.

Each record contains:

- Prompt
- Preferred (Chosen) Response
- Less Preferred (Rejected) Response

Example:

```json
{
    "prompt": "How do I return an item?",
    "chosen": "...",
    "rejected": "..."
}
```

This enables the model to learn preferred response behavior instead of simply predicting the next token.

---

# Parameter-Efficient Fine-Tuning (PEFT)

Training every parameter of a large language model is computationally expensive.

Instead, this project uses **Parameter-Efficient Fine-Tuning (PEFT)**.

PEFT trains only a small number of additional parameters while keeping the original model weights frozen.

Benefits include:

- Reduced GPU memory usage
- Faster training
- Smaller checkpoints
- Efficient deployment
- Easy adapter sharing

---

# LoRA (Low-Rank Adaptation)

LoRA introduces trainable low-rank matrices into selected transformer layers.

Instead of modifying all model weights, only these lightweight adapter parameters are optimized during training.

Advantages of LoRA include:

- Significantly fewer trainable parameters
- Lower storage requirements
- Faster fine-tuning
- Ability to switch between multiple adapters without modifying the base model

---

# QLoRA

To further reduce hardware requirements, the project uses **QLoRA (Quantized LoRA)**.

QLoRA combines:

- 4-bit model quantization
- LoRA adapters

The project uses:

- 4-bit NF4 quantization
- Double Quantization
- bfloat16 computation

Benefits include:

- Reduced GPU memory consumption
- Faster loading
- Efficient fine-tuning on Google Colab Free Tier
- No significant loss in model quality

---

# Supervised Fine-Tuning (SFT)

The first training stage is Supervised Fine-Tuning.

The model learns from instruction-response pairs.

Training workflow:

```
Instruction Dataset

↓

Base Model

↓

QLoRA

↓

LoRA Adapter

↓

SFT Training

↓

SFT Adapter
```

The resulting adapter enables the model to generate more accurate and domain-specific customer support responses.

---

# Direct Preference Optimization (DPO)

After Supervised Fine-Tuning, the project performs Direct Preference Optimization.

Instead of learning from instruction-response pairs, DPO learns from preference pairs.

Training workflow:

```
Preference Dataset

↓

Base Model

↓

Load SFT Adapter

↓

DPO Training

↓

DPO Adapter
```

This stage improves:

- Response quality
- Response alignment
- Conversational naturalness
- User preference satisfaction

---

# Inference

The inference pipeline supports multiple model configurations.

Supported models include:

- Base Model
- Local SFT Adapter
- Hugging Face SFT Adapter
- Local DPO Adapter
- Hugging Face DPO Adapter

The model loader automatically loads the appropriate adapter based on the inference configuration.

---

# Evaluation

Generated responses are evaluated using predefined customer support prompts.

The project supports automatic evaluation of:

- Base Model
- SFT Model
- DPO Model

Outputs are saved as JSON files for further analysis.

---

# Model Comparison

The project includes a configuration-driven comparison framework.

The comparison pipeline:

- Loads multiple models
- Generates responses
- Saves outputs
- Produces Markdown reports

New models can be added simply by updating the comparison configuration.

---

# Automatic NLP Evaluation

The project evaluates generated responses using several widely adopted NLP metrics.

### BLEU

Measures lexical overlap between generated responses and reference responses.

---

### ROUGE-1

Measures unigram similarity.

---

### ROUGE-2

Measures bigram similarity.

---

### ROUGE-L

Measures similarity based on the Longest Common Subsequence (LCS), capturing sentence-level structure.

---

### BERTScore

Measures semantic similarity using contextual embeddings generated by transformer models.

Unlike lexical metrics, BERTScore evaluates whether two responses convey the same meaning even if different words are used.

---

# Project Architecture

```
Raw Dataset

↓

Dataset Cleaning

↓

Instruction Dataset

↓

Preference Dataset

↓

SFT Training

↓

DPO Training

↓

Inference

↓

Evaluation

↓

Comparison

↓

Reports
```

---

# Libraries Used

The implementation is built using the Hugging Face ecosystem.

Major libraries include:

- PyTorch
- Transformers
- PEFT
- TRL
- BitsAndBytes
- Datasets
- Accelerate
- Hugging Face Hub
- ROUGE Score
- BERTScore
- NLTK

---

# Limitations

The project has a few practical limitations:

- Training was performed using the Google Colab Free Tier.
- Dataset subset sampling was used to reduce training time.
- The workflow starts from the instruction-tuned **Qwen2.5-1.5B-Instruct** model and therefore focuses on instruction fine-tuning followed by Direct Preference Optimization.
- Some responses still contain template placeholders inherited from the original dataset.

---

# Future Improvements

Possible future extensions include:

- Full dataset training
- Human preference collection
- Retrieval-Augmented Generation (RAG)
- Tool Calling
- Function Calling
- Multi-turn conversation evaluation
- Reinforcement Learning from Human Feedback (RLHF)
- Deployment as a production-ready customer support assistant

---

# Conclusion

This project demonstrates a complete parameter-efficient fine-tuning workflow for adapting a pretrained Large Language Model to the Customer Support domain.

By combining dataset preprocessing, Supervised Fine-Tuning, Direct Preference Optimization, inference, evaluation, and automated model comparison, the project provides an end-to-end pipeline that is modular, extensible, and suitable for future research and production deployment.

The architecture emphasizes efficient training through LoRA and QLoRA while maintaining strong response quality and enabling easy extension to additional domains and fine-tuning strategies.