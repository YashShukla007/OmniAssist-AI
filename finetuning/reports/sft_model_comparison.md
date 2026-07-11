# Supervised Fine-Tuning (SFT) Model Comparison

## Project

**OmniAssist AI – Customer Support Assistant**

---

# Objective

The objective of this comparison is to evaluate the improvements achieved after performing **Supervised Fine-Tuning (SFT)** on the Customer Support instruction dataset.

The SFT model is compared against the original **Qwen2.5-1.5B-Instruct** base model using the same set of customer support questions.

---

# Model Information

| Property | Base Model | SFT Model |
|-----------|------------|-----------|
| Model | Qwen2.5-1.5B-Instruct | Qwen2.5-1.5B-Instruct + LoRA Adapter |
| Fine-Tuning | None | Supervised Fine-Tuning |
| Quantization | 4-bit | 4-bit QLoRA |
| Dataset | None | Customer Support Instruction Dataset |

---

# Evaluation Methodology

The same evaluation prompts used for the base model were asked again after Supervised Fine-Tuning.

The responses were compared using the following criteria:

- Correctness
- Domain Accuracy
- Clarity
- Helpfulness
- Professional Tone
- Safety
- Response Specificity

---

# Model Comparison

| Question | Base Model | SFT Model | Better Model | Reason |
|-----------|------------|-----------|--------------|--------|
| Cancel my order | Generic response | More structured cancellation process | SFT | More domain-specific guidance |
| Refund request | Generic refund explanation | Clear refund workflow | SFT | Better customer support behavior |
| Change shipping address | General advice | Practical step-by-step guidance | SFT | Improved clarity |
| Order delayed | Basic explanation | More helpful troubleshooting | SFT | Better customer assistance |
| Damaged product | Generic replacement suggestion | Complete replacement workflow | SFT | More actionable response |
| Track my order | General tracking advice | More structured tracking explanation | SFT | Improved completeness |
| Wrong delivery address | Generic answer | Better handling before and after shipment | SFT | More realistic workflow |
| Payment failure | Retry suggestion | Multiple troubleshooting options | SFT | Better problem-solving |
| Return an item | Generic return policy | Better return process explanation | SFT | Improved domain knowledge |
| Contact support | Basic response | More professional support guidance | SFT | Better customer interaction |

---

## Automatic Evaluation Metrics

The SFT model was evaluated using multiple NLP metrics.

The evaluation included:

- BLEU
- ROUGE-1
- ROUGE-2
- ROUGE-L
- BERTScore

Compared with the base model, the SFT model generally produced:

- Better semantic similarity (higher BERTScore on several prompts)
- Improved ROUGE scores for multiple customer support questions
- More structured and domain-specific responses

---

# Improvements Observed

Compared to the base model, the Supervised Fine-Tuned model demonstrates noticeable improvements.

### Domain Accuracy

The model produces responses that are significantly more relevant to customer support scenarios.

---

### Response Structure

Responses are more organized and easier to follow.

---

### Professional Tone

The model consistently responds in a polite and professional manner suitable for customer interactions.

---

### Helpfulness

The model provides clearer instructions and more actionable guidance.

---

### Consistency

Responses follow a more consistent customer support style across different questions.

---

# Advantages of SFT

- Better instruction following
- Improved customer support terminology
- More detailed responses
- Better formatting
- Improved response consistency
- Reduced generic answers

---

# Remaining Limitations

Although the SFT model improves significantly over the base model, a few limitations remain.

- Responses may still occasionally contain generic wording.
- The model does not explicitly learn user preferences.
- Different valid responses are treated equally during supervised learning.
- Preference alignment is not yet performed.

These limitations motivate the use of **Direct Preference Optimization (DPO)** in the next stage.

---

# Summary

The Supervised Fine-Tuning stage successfully adapts the pretrained language model to the Customer Support domain.

Compared to the original base model, the SFT model demonstrates:

- Better domain understanding
- Improved instruction following
- More detailed responses
- Higher response consistency
- More professional customer support behavior

The generated SFT adapter serves as the foundation for the subsequent Direct Preference Optimization stage.