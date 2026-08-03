import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


@st.cache_resource
def load_model():
    """
    Load Qwen only once.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )

    return tokenizer, model


def load_llm(prompt, max_tokens=180):
    """
    Generate answer from Qwen.
    """

    tokenizer, model = load_model()

    messages = [
        {
            "role": "system",
            "content":
            "You are an intelligent research paper assistant. "
            "Answer only from the provided context.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=2048,
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id,
        )

    answer = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:],
        skip_special_tokens=True,
    )

    return answer.strip()