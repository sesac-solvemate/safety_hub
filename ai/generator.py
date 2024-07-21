import torch
import random
import sys
import json

import numpy as np
import pandas as pd

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import TextStreamer, GenerationConfig
from tqdm import tqdm
from util import *
from engine import *

random.seed(7)

path = './reranker.json' 
content = read_json(path)

############## Korean ##############
model_name='beomi/Llama-3-KoEn-8B-Instruct-preview'
gen = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
gen_tokenizer = AutoTokenizer.from_pretrained(model_name)

query = '제조업에서 끼임 사고를 예방하는 방법을 알려줘'

inputs = f"### 질문 : {query} ### 문맥 : {content} ### 답변 :"
messages = [
            {"role": "system", "content": "질문에 대해 문맥을 바탕으로 답변해줘. 모든 대답은 한국어(Korean)으로 대답해줘."},
            {"role": "user", "content": inputs}, 
        ]

result = generator(messages, gen, gen_tokenizer)
print(result)
############## Korean -> English ##############



############## Korean -> Vietnamese ##############
