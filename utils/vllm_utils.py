import os
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

from utils.setting import CUDA_VISIBLE_DEVICES

os.environ['CUDA_VISIBLE_DEVICES'] = CUDA_VISIBLE_DEVICES


def tokenizer_initial(tokenizer_path=r'/home/yinrigao/models/qwen25_coder_7b'):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    return tokenizer


def model_initial(model_path=r"/home/yinrigao/models/qwen25_coder_7b"):
    model = LLM(model=model_path)
    return model


def param_initial(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=1024):
    return SamplingParams(temperature=temperature,
                          top_p=top_p,
                          repetition_penalty=repetition_penalty,
                          max_tokens=max_tokens)


def model_inference(message, tokenizer, model, sampling_params=param_initial()):
    text = tokenizer.apply_chat_template(
        message,
        tokenize=False,
        add_generation_prompt=True
    )
    outputs = model.generate([text], sampling_params)
    # print(outputs[0].outputs[0].text)
    return outputs[0].outputs[0].text
