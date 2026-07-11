# OmniAssist AI

> A modular end-to-end Large Language Model (LLM) fine-tuning framework implementing **Supervised Fine-Tuning (SFT)** and **Direct Preference Optimization (DPO)** using **QLoRA**, along with a configurable inference, evaluation, and model comparison pipeline.

---

## Project Overview

OmniAssist AI is a complete LLM fine-tuning framework developed to demonstrate modern post-training techniques on open-source language models.

The project provides an end-to-end workflow covering:

- Dataset preparation
- Supervised Fine-Tuning (SFT)
- Direct Preference Optimization (DPO)
- Adapter-based inference
- Automatic evaluation
- Model comparison
- Hugging Face integration

The framework is designed with a modular architecture so that different base models, datasets, adapters, and evaluation strategies can be integrated with minimal code changes.

---

## Features

- QLoRA-based parameter-efficient fine-tuning
- Supervised Fine-Tuning (SFT)
- Direct Preference Optimization (DPO)
- PEFT LoRA adapters
- 4-bit quantization using BitsAndBytes
- Modular project architecture
- Configuration-driven training pipeline
- Local adapter inference
- Hugging Face adapter inference
- Automatic evaluation pipeline
- Automatic comparison framework
- BLEU evaluation
- ROUGE-1 evaluation
- ROUGE-2 evaluation
- ROUGE-L evaluation
- BERTScore evaluation
- Markdown comparison report generation
- Easily extensible architecture

---

## Tech Stack

### Programming Language

- Python

### Deep Learning

- PyTorch
- Transformers
- PEFT
- TRL

### Fine-Tuning

- QLoRA
- LoRA
- SFT
- DPO

### Model

- Qwen2.5-1.5B-Instruct

### Dataset

- Customer Support Dataset

### Evaluation

- BLEU
- ROUGE
- BERTScore

### Tools

- Hugging Face Hub
- Google Colab
- Git
- GitHub

---

## Implementation Notes

This project implements a complete parameter-efficient fine-tuning workflow using the Hugging Face ecosystem.

The implementation includes:

- Transformers
- PEFT
- TRL
- BitsAndBytes
- PyTorch

The fine-tuning pipeline consists of:

1. Dataset preprocessing
2. Instruction dataset generation
3. Supervised Fine-Tuning (SFT)
4. Preference dataset generation
5. Direct Preference Optimization (DPO)
6. Inference
7. Automatic evaluation
8. Model comparison

The project uses a modular architecture that separates preprocessing, training, inference, evaluation, and comparison into independent components for easier maintenance and future extension.

---

## Project Architecture

```
                    Raw Dataset
                         │
                         ▼
                Dataset Preprocessing
                         │
                         ▼
               Instruction Dataset
                         │
                         ▼
                Supervised Fine-Tuning
                         │
                         ▼
                    SFT Adapter
                         │
                         ▼
              Preference Dataset
                         │
                         ▼
            Direct Preference Optimization
                         │
                         ▼
                    DPO Adapter
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
     Inference Pipeline         Evaluation Pipeline
          │                             │
          └──────────────┬──────────────┘
                         ▼
                Comparison Framework
                         │
                         ▼
              Markdown Comparison Report
```

---

# Repository Structure

```
OmniAssist-AI/

├── adapters/
│   ├── sft/
│   └── dpo/
│
├── comparison/
│   ├── outputs/
│   └── comparison_report.md
│
├── data/
│   ├── raw/
│   ├── instruction/
│   └── preference/
│
├── evaluation/
│   ├── prompts.json
│   ├── base_outputs.json
│   ├── sft_outputs.json
│   ├── dpo_outputs.json
│   └── comparison_report.md
│
├── notebooks/
│
├── src/
│   ├── comparison/
│   ├── config/
│   ├── datasets/
│   ├── evaluation/
│   ├── inference/
│   ├── loaders/
│   ├── training/
│   └── utils/
│
├── requirements.txt
├── requirements-colab.txt
└── README.md
```

---

# Fine-Tuning Pipeline

The project follows a two-stage fine-tuning strategy.

## Stage 1 — Supervised Fine-Tuning (SFT)

The base model is first trained on an instruction dataset using supervised learning to improve its ability to follow user instructions.

**Output**

- LoRA Adapter
- Fine-tuned SFT Model

---

## Stage 2 — Direct Preference Optimization (DPO)

The SFT adapter is then used as the initialization point for Direct Preference Optimization.

Preference pairs containing **chosen** and **rejected** responses are used to align the model with preferred outputs.

**Output**

- DPO Adapter
- Preference-Aligned Model

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/<your-username>/OmniAssist-AI.git

cd OmniAssist-AI
```

---

## Create Virtual Environment

Using **uv**

```bash
uv venv

source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

For Google Colab

```bash
pip install -r requirements-colab.txt
```

---

# Dataset Preparation

The project uses two datasets during the fine-tuning pipeline.

## 1. Instruction Dataset

Used for Supervised Fine-Tuning (SFT).

Each sample contains

- Instruction
- Response

Example

```json
{
    "instruction": "How can I cancel my order?",
    "response": "You can cancel your order from the Orders page before it is shipped."
}
```

---

## 2. Preference Dataset

Used for Direct Preference Optimization.

Each sample contains

- Prompt
- Chosen Response
- Rejected Response

Example

```json
{
    "prompt": "How can I cancel my order?",

    "chosen": "...",

    "rejected": "..."
}
```

---

# Training

## Supervised Fine-Tuning (SFT)

Run

```bash
python -m src.training.train_sft
```

The SFT pipeline

- Loads the base model
- Applies QLoRA
- Fine-tunes using instruction data
- Saves the LoRA adapter

Output

```
adapters/
└── sft/
    └── customer_support/
```

---

## Direct Preference Optimization (DPO)

Run

```bash
python -m src.training.train_dpo
```

The DPO pipeline

- Loads the base model
- Loads the SFT adapter
- Trains using preference pairs
- Saves the DPO adapter

Output

```
adapters/
└── dpo/
    └── customer_support/
```

---

# Inference

The inference pipeline supports multiple model types.

- Base Model
- SFT Adapter
- DPO Adapter

Configuration is controlled through

```
src/inference/inference_config.py
```

Run

```bash
python -m src.inference.inference
```

Supported Adapter Sources

- Local
- Hugging Face Hub

Switching between them only requires changing

```python
ADAPTER_SOURCE
```

No code modifications are required.

---

# Evaluation

The project includes an automatic evaluation pipeline.

Run

```bash
python -m src.evaluation.run_full_evaluation
```

The evaluation pipeline

- Loads evaluation prompts
- Generates responses
- Saves outputs
- Creates comparison reports

Generated Outputs

```
evaluation/

base_outputs.json

sft_outputs.json

dpo_outputs.json

comparison_report.md
```

---

# Automatic NLP Metrics

The framework evaluates generated responses using multiple NLP metrics.

## BLEU

Measures n-gram overlap between generated and reference responses.

Higher BLEU indicates closer lexical similarity.

---

## ROUGE-1

Measures unigram overlap.

Useful for checking important keyword coverage.

---

## ROUGE-2

Measures bigram overlap.

Provides a stricter evaluation than ROUGE-1.

---

## ROUGE-L

Measures the Longest Common Subsequence (LCS).

Captures sentence-level similarity.

---

## BERTScore

Measures semantic similarity using contextual embeddings.

Unlike BLEU and ROUGE, BERTScore can recognize paraphrases and semantically equivalent responses.

---

# Comparison Framework

The project provides a modular comparison framework capable of evaluating multiple models.

Run

```bash
python -m src.comparison.compare_models
```

Current supported models

- Base Model
- Local SFT Adapter
- Hugging Face SFT Adapter
- Local DPO Adapter
- Hugging Face DPO Adapter

New models can be added simply by editing

```
src/comparison/comparison_config.py
```

No code changes are required.

---

# Generated Comparison Report

The comparison framework automatically generates

```
comparison/comparison_report.md
```

The report contains

- Prompt
- Reference Response
- Model Response
- BLEU
- ROUGE-1
- ROUGE-2
- ROUGE-L
- BERTScore
- Response Statistics
    - Words
    - Characters
    - Sentences
    - Average Word Length

This enables side-by-side comparison of multiple models using both lexical and semantic evaluation metrics.

---

# Hugging Face Integration

The project supports loading adapters from either the local filesystem or the Hugging Face Hub.

Configure the adapter source in

```
src/inference/inference_config.py
```

```python
ADAPTER_SOURCE = "local"
```

or

```python
ADAPTER_SOURCE = "huggingface"
```

Supported repositories

```
SFT Adapter

https://huggingface.co/YashShukla007/OmniAssist-SFT-Customer-Support

DPO Adapter

https://huggingface.co/YashShukla007/OmniAssist-DPO-Customer-Support
```

This allows inference without storing adapters inside the GitHub repository.

---

# Configuration Driven Design

The project follows a configuration-driven architecture.

Almost every component can be modified without changing the implementation.

Configuration files include

```
src/config/
```

- model_config.py
- training_config.py
- dpo_config.py

```
src/inference/
```

- inference_config.py

```
src/comparison/
```

- comparison_config.py

Changing

- base model
- adapter source
- adapter path
- Hugging Face repository

requires modifying only the configuration files.

---

# Example Workflow

```
Prepare Dataset

        │

        ▼

Train SFT Adapter

        │

        ▼

Train DPO Adapter

        │

        ▼

Run Inference

        │

        ▼

Run Evaluation

        │

        ▼

Compare Models

        │

        ▼

Generate Markdown Report
```

---

# Results

The project successfully implements

- Parameter Efficient Fine-Tuning (PEFT)
- QLoRA
- Supervised Fine-Tuning
- Direct Preference Optimization
- Local Adapter Loading
- Hugging Face Adapter Loading
- Automatic Evaluation
- Automatic Comparison Framework

The comparison report provides

- Reference Response
- Generated Response
- BLEU
- ROUGE-1
- ROUGE-2
- ROUGE-L
- BERTScore
- Word Statistics
- Character Statistics
- Sentence Statistics
- Average Word Length

allowing objective comparison of multiple models.

---

# Current Project Capabilities

✔ QLoRA Training

✔ Supervised Fine-Tuning (SFT)

✔ Direct Preference Optimization (DPO)

✔ Modular Model Loader

✔ Local Adapter Inference

✔ Hugging Face Adapter Inference

✔ Automatic Evaluation Pipeline

✔ Automatic Comparison Framework

✔ BLEU Evaluation

✔ ROUGE Evaluation

✔ BERTScore Evaluation

✔ Markdown Report Generation

✔ Configuration Driven Architecture

✔ Easily Extendable Codebase

---

# Limitations

Although the framework is fully functional, a few limitations remain.

- The dataset contains placeholder values such as support phone numbers and website URLs, which may occasionally appear in generated responses.

- Automatic evaluation metrics cannot fully capture factual correctness or response helpfulness.

- Human evaluation is not currently included.

- LLM-as-a-Judge evaluation is planned as a future enhancement.

- The project starts from the pretrained instruction-tuned model **Qwen2.5-1.5B-Instruct** and therefore focuses on instruction fine-tuning (SFT) followed by Direct Preference Optimization (DPO).

- A separate non-instruction fine-tuning stage was not included, as the selected base model already provides strong instruction-following capabilities.

---

## Challenges Faced

- Limited GPU memory while fine-tuning large language models.
- Preparing high-quality instruction and preference datasets.
- Choosing appropriate LoRA hyperparameters.
- Managing adapter checkpoints.
- Evaluating model quality beyond lexical similarity.
- Maintaining a modular architecture for future extension.

---

## Final Observations

The DPO-aligned model consistently generated more domain-specific and professional responses than the base model.

Automatic evaluation using BLEU, ROUGE, and BERTScore indicated improved similarity with reference responses.

The modular architecture enables easy experimentation with different base models, adapters, and evaluation strategies.

---

# Future Improvements

The modular architecture allows additional features to be integrated easily.

Planned improvements include

- LLM-as-a-Judge
- Win Rate Comparison
- Hallucination Detection
- Faithfulness Metrics
- Toxicity Evaluation
- Response Latency Benchmarking
- GPU Memory Benchmarking
- Multi-Domain Fine-Tuning
- Automatic Leaderboard Generation
- Interactive Evaluation Dashboard
- Adapter Fusion
- Multi-Adapter Comparison

---

# Learning Outcomes

This project provided hands-on experience with

- Large Language Models
- Hugging Face Transformers
- PEFT
- LoRA
- QLoRA
- Supervised Fine-Tuning
- Direct Preference Optimization
- Preference Datasets
- Hugging Face Hub
- Adapter-Based Fine-Tuning
- Modular Software Design
- NLP Evaluation Metrics
- Model Comparison Frameworks

---

# Acknowledgements

This project makes use of several outstanding open-source libraries.

- Hugging Face Transformers
- Hugging Face Hub
- PEFT
- TRL
- PyTorch
- BitsAndBytes
- BERTScore
- NLTK
- ROUGE Score

Special thanks to the open-source community for making modern LLM research accessible.

---

# License

This project is intended for educational and research purposes.

Please ensure compliance with the licenses of the datasets, pretrained models, and third-party libraries used.

---

# Author

**Yash Shukla**

GitHub

https://github.com/YashShukla007

LinkedIn

https://www.linkedin.com/in/yashshukla2508/

---

# Star the Repository ⭐

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps support future development and encourages further work on open-source LLM fine-tuning projects.