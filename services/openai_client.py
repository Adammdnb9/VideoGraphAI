"""
OpenAI client wrapper for chat completions, embeddings and image generation.
Replace usage of other LLM providers with calls to these helper functions.
"""
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")
openai.api_key = OPENAI_API_KEY

def chat_completion(messages, model="gpt-4o-mini", max_tokens=800, temperature=0.2):
    """
    messages: list of {"role": "system/user/assistant", "content": "..."}
    returns the assistant text
    """
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def generate_script(topic, length_seconds=60, tone="concise"):
    system = {"role":"system","content":"You are a helpful script writer that writes short YouTube-Shorts scripts."}
    user = {"role":"user","content":f"Write a tight, engaging script for a {length_seconds}s YouTube Short about: {topic}. Tone: {tone}. Provide timestamps or scene breakdowns where appropriate."}
    return chat_completion([system, user])

def create_image(prompt, size="1024x1024"):
    """Return URL of generated image using OpenAI Images API."""
    resp = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    return resp.data[0].url

def create_embedding(text, model="text-embedding-3-small"):
    resp = openai.Embedding.create(input=text, model=model)
    return resp.data[0].embedding
