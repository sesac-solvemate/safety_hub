import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import TextStreamer, GenerationConfig
import json
import sys
import glob
import pandas as pd
from tqdm import tqdm
import random

def generator(x, model, tokenizer):
    '''
        x: messages
    '''
    input_ids = tokenizer.apply_chat_template(
        x, # messages
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)
    
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
        eos_token_id=terminators,
        do_sample=True,
        temperature=1,
        top_p=0.9,
    )   

    response = outputs[0][input_ids.shape[-1]:]
    result = tokenizer.decode(response, skip_special_tokens=True)

    return result
    
