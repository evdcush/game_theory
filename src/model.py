import os
import anthropic
import google.generativeai as genai
import time
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

####### data generation close-source models #######

claude_key = os.getenv('$ANTHROPIC_API_KEY')
gemini_key = ""
open_ai_key = ""

def call_anthropic_api(message, system_prompt):
    api_client = anthropic.Anthropic(
        api_key=claude_key,
    )
    system_prompt = system_prompt
    message = api_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=3000,
        temperature=1,
        system=system_prompt,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return message.content[0].text

def call_gemini_api(message):
    retries = 60  # Maximum number of retries
    while retries > 0:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message)
            return response.text
        except Exception as e:
            retries -= 1
            time.sleep(0.1)

def call_gpt4_api(message, system_prompt):
    openai_client = OpenAI(api_key=open_ai_key)
    response = openai_client.chat.completions.create(
        model = "gpt-4-1106-preview", 
        messages=[
            {"role": "system","content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content

def call_gpt35_api(message, system_prompt):
    openai_client = OpenAI(api_key=open_ai_key)
    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system","content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content


def close_source_call(model, message, system_prompt):
    if model == 'gemini':
        result = call_gemini_api(message)
    elif model == 'claude':
        result = call_anthropic_api(message, system_prompt)
    elif model == 'gpt4':
        result = call_gpt4_api(message, system_prompt)
    elif model == 'gemini':
        result = call_gpt35_api(message, system_prompt)

    return result
