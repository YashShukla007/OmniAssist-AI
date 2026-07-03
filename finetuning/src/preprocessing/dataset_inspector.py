from datasets import load_dataset
import pandas as pd


dataset = load_dataset(
    "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
)

train = dataset["train"]

print("=" * 80)

print("Rows :", len(train))

print("=" * 80)

print(train.features)

print("=" * 80)

df = train.to_pandas()

print(df.head())

print("=" * 80)

print(df.describe(include="all"))