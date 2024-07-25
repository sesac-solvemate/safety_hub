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

random.seed(7)

############## Models ##############
device = torch.device('cuda')
model_path = 'Dongjin-kr/ko-reranker'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
model.eval()
####################################

############## Gold Documents ##############
doc1_path = './Constructing_prevence.csv' 
doc2_path = './Manufacturing_prevence.csv'

doc1 = pd.read_csv(doc1_path)
doc2 = pd.read_csv(doc2_path)
# docs = doc1 + doc2

docs = []
for i in range(len(doc1)):
    docs.append(doc1['label'][i] + doc1['text'][i])
for i in range(len(doc2)):
    docs.append(doc2['label'][i] + doc2['text'][i])
###########################################

query = '제조업에서 끼임 사고를 예방하는 방법을 알려줘'
answer = []

pairs = []
sim = []
for doc in docs:
    pairs.append([query, doc])

with torch.no_grad():
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512).to(device)
    scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
    scores = exp_normalize(scores.detach().cpu().numpy())
    sim.append(scores)
    # print(scores)
    
top_3 = np.argsort(sim)[0][len(sim)-3:]
content = ''

for i in top_3:
    content += docs[i]

file_path = './reranker.json'
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(content, file, ensure_ascii=False, indent=4)
print('The End')
