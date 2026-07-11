# Base Model Evaluation

## Project

**OmniAssist AI – Customer Support Assistant**

---

# Objective

The objective of this evaluation is to analyze the performance of the original **Qwen2.5-1.5B-Instruct** model on customer support related questions before performing any task-specific fine-tuning.

This baseline evaluation helps establish the strengths and limitations of the pretrained model and serves as a reference for measuring improvements after Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO).

---

# Base Model

| Property | Value |
|-----------|-------|
| Model | Qwen2.5-1.5B-Instruct |
| Fine-Tuning | None |
| Quantization | 4-bit QLoRA Ready |
| Domain | Customer Support |

---

# Evaluation Methodology

The base model was evaluated using ten customer support prompts covering common user queries.

The evaluation focused on the following aspects:

- Correctness
- Domain Accuracy
- Clarity
- Helpfulness
- Professional Tone
- Safety
- Specificity

---

# Evaluation Questions

| Question | Observation |
|-----------|-------------|
| How can I cancel my order? | Generic cancellation guidance without company-specific workflow. |
| I want a refund for my purchase. | Provides general refund advice but lacks detailed policy information. |
| How do I change my shipping address? | Suggests contacting support but does not explain the process clearly. |
| My order hasn't arrived yet. | Gives a reasonable response but lacks troubleshooting steps. |
| I received a damaged product. | Suggests contacting customer service without structured replacement guidance. |
| How do I track my order? | Explains shipment tracking in general terms. |
| I entered the wrong delivery address. | Provides generic recommendations without considering shipping status. |
| My payment failed during checkout. | Suggests retrying payment but lacks practical troubleshooting. |
| How do I return an item? | Gives general return information without describing the return workflow. |
| How can I contact customer support? | Recommends contacting support but without detailed contact options. |

---

## Quantitative Observations

Across the evaluation prompts, the base model demonstrated:

- Consistent semantic understanding (BERTScore approximately 0.82–0.87)
- Moderate lexical overlap (ROUGE-1 generally between 0.12–0.21)
- Low BLEU scores due to the absence of exact reference responses

These results indicate that the model produces coherent responses but lacks customer support domain specialization.

---

# Observations

The base model demonstrates strong general language understanding and can answer customer support questions in a coherent and grammatically correct manner.

However, several limitations were observed:

- Responses are generic rather than domain-specific.
- Customer support procedures are often incomplete.
- Answers occasionally lack actionable guidance.
- Company-specific policies are not reflected.
- Responses are less consistent across similar questions.

Although the model produces safe and professional responses, it has not yet learned the desired customer support style for this project.

---

# Strengths

- Fluent natural language generation.
- Good reasoning ability.
- Professional tone.
- Safe responses.
- Handles a wide range of customer support topics.

---

# Limitations

- Limited domain specialization.
- Generic responses.
- Missing policy-specific details.
- Less consistent terminology.
- Reduced task-specific accuracy.

---

# Conclusion

The evaluation demonstrates that the pretrained **Qwen2.5-1.5B-Instruct** model provides a solid foundation for customer support tasks but lacks the domain-specific knowledge required for accurate and consistent responses.

This baseline serves as the reference point for evaluating improvements obtained through:

- Supervised Fine-Tuning (SFT)
- Direct Preference Optimization (DPO)

Subsequent evaluations compare the fine-tuned models against this baseline to measure improvements in response quality, domain relevance, and overall helpfulness.