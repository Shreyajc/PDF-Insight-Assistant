from backend.llm import load_llm


def generate_summary(chunks):
    """
    Generate a fast and structured summary using only ONE LLM call.
    Optimized for CPU and 8GB RAM.
    """

    if not chunks:
        return "No document available."

    total = len(chunks)

    # Select representative chunks
    if total <= 4:
        selected = chunks
    else:
        indexes = [
            0,
            total // 3,
            (2 * total) // 3,
            total - 1,
        ]
        selected = [chunks[i] for i in indexes]

    # Merge text from selected chunks
    context = ""

    for chunk in selected:
        text = chunk.page_content.strip()

        # Limit each chunk to keep prompt small
        context += text[:900] + "\n\n"

    prompt = f"""
You are an expert document summarizer.

Read the document excerpts below and generate a detailed but concise Markdown summary.

Do NOT copy sentences.

Summarize in your own words.

Use this exact format.

# Overview

Explain what the document is about.

# Objectives

- Point 1
- Point 2
- Point 3

# Methodology

Explain the methodology used.

# Key Findings

- Finding 1
- Finding 2
- Finding 3

# Conclusion

Write a short conclusion.

Document:

{context}

Markdown Summary:
"""

    return load_llm(
        prompt,
        max_tokens=350
    )