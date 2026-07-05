from huggingface_hub import InferenceClient
import requests

HF_TOKEN = "<YOUR_HUGGING_FACE_TOKEN>"

OPENROUTER_KEY = "<YOUR_OPENROUTER_API_KEY>"

HF_MODELS = [
    "Qwen/Qwen2.5-1.5B-Instruct",
    "Qwen/Qwen2.5-1.5B",
    "meta-llama/Llama-3.2-3B-Instruct",
    "meta-llama/Llama-3.2-1B",
]

OPENROUTER_MODELS = [
    "qwen/qwen-2.5-1.5b-instruct",
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-2-2b-it",
    "liquid/lfm-2.5-1.2b-instruct:free",
]


def test_hf(model):
    print("=" * 80)
    print(f"Hugging Face -> {model}")

    client = InferenceClient(api_key=HF_TOKEN)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Say Hello."
                }
            ],
            max_tokens=20,
        )

        print("SUCCESS")
        print(response.choices[0].message.content)

    except Exception as e:
        print("FAILED")
        print(type(e).__name__)
        print(e)


def test_openrouter(model):

    print("=" * 80)
    print(f"OpenRouter -> {model}")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Say Hello."
            }
        ],
    }

    r = requests.post(url, headers=headers, json=payload)

    print("Status:", r.status_code)

    try:
        print(r.json())
    except Exception:
        print(r.text)


print("\nTesting Hugging Face\n")

for model in HF_MODELS:
    test_hf(model)

print("\nTesting OpenRouter\n")

for model in OPENROUTER_MODELS:
    test_openrouter(model)