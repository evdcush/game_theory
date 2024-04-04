import anthropic
import google.generativeai as genai
import time
from openai import OpenAI
from vllm import LLM, SamplingParams
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

####### data generation close-source models #######

claude_key = ""
gemini_key = ""
open_ai_key = ""

def call_anthropic_api(message):
    api_client = anthropic.Anthropic(
        api_key=claude_key,
    )
    system_prompt = "You are a rational assistant that carefully answer the question."
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

def call_gpt4_api(message):
    openai_client = OpenAI(api_key=open_ai_key)
    response = openai_client.chat.completions.create(
        model = "gpt-4-1106-preview", 
        messages=[
            {"role": "user", "content": message},
        ],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content

def call_gpt35_api(message):
    openai_client = OpenAI(api_key=open_ai_key)
    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content


def close_source_call(model, message):
    if model == 'gemini':
        result = call_gemini_api(message)
    elif model == 'claude':
        result = call_anthropic_api(message)
    elif model == 'gpt4':
        result = call_gpt4_api(message)
    elif model == 'gemini':
        result = call_gpt35_api(message)

    return result

####### model evaluation with scaling #######
####### tulu #######
def run_tulu_7(text_prompt, model_name=None):
    sampling_params = SamplingParams(temperature=0, max_tokens=1000)
    if model_name is None:
        model_name = 'allenai/tulu-2-7b'
        download_dir = 'pretrained_models'
    else:
        download_dir = model_name
    llm = LLM(
        model=model_name,
        download_dir=download_dir,
        trust_remote_code=True,
        tensor_parallel_size=4, 
        max_num_seqs=4,
        max_num_batched_tokens=4 * 8192,
    )
    text_prompt = ['<|user|>\n'+t+'<|assistant|>\n' for t in text_prompt]
    predictions = llm.generate(text_prompt, sampling_params)
    all_predictions = []
    for RequestOutput in predictions:
        output = RequestOutput.outputs[0].text
        all_predictions.append(output)
    return all_predictions 

def run_tulu_13(text_prompt, model_name=None):
    sampling_params = SamplingParams(temperature=0, max_tokens=1000)
    if model_name is None:
        model_name = 'allenai/tulu-2-13b'
        download_dir = 'pretrained_models'
    else:
        download_dir = model_name
    llm = LLM(
        model=model_name,
        download_dir=download_dir,
        trust_remote_code=True,
        tensor_parallel_size=4, 
        max_num_seqs=4,
        max_num_batched_tokens=4 * 8192,
    )
    text_prompt = ['<|user|>\n'+t+'<|assistant|>\n' for t in text_prompt]
    predictions = llm.generate(text_prompt, sampling_params)
    all_predictions = []
    for RequestOutput in predictions:
        output = RequestOutput.outputs[0].text
        all_predictions.append(output)
    return all_predictions 

def run_tulu_70(text_prompt, model_name=None):
    sampling_params = SamplingParams(temperature=0, max_tokens=1000)
    if model_name is None:
        model_name = 'allenai/tulu-2-70b'
        download_dir = 'pretrained_models'
    else:
        download_dir = model_name
    llm = LLM(
        model=model_name,
        download_dir=download_dir,
        trust_remote_code=True,
        tensor_parallel_size=4, 
        max_num_seqs=4,
        max_num_batched_tokens=4 * 8192,
    )
    predictions = llm.generate(text_prompt, sampling_params)
    all_predictions = []
    for RequestOutput in predictions:
        output = RequestOutput.outputs[0].text
        all_predictions.append(output)
    return all_predictions 
