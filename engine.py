import torch
import random
import json
import sys
import glob
import bm25s
import numpy as np
import pandas as pd

from util import *
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import TextStreamer, GenerationConfig

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader

def retriever(label, query):
    '''
        label: conveyer, electricity, painting, chemistry, transportation,
                bone_disease, inversion, forklift, crane, workplace
    '''
    path = f'./{label}.csv'
    df = pd.read_csv(path)

    # preparing the corpus
    corpus = []
    for i in range(len(df)):
        corpus.append(df['0'][i])

    # calculating the similarity on sparse retriever 
    sparse_retriever = bm25s.BM25(corpus=corpus)
    sparse_retriever.index(bm25s.tokenize(corpus))
    results, scores_1 = sparse_retriever.retrieve(bm25s.tokenize(query), k=len(corpus))

    # calculating the similarity on dense retriever 
    pairs, scores_2 = [], []

    for doc in corpus:
        pairs.append([query, doc])
        
    device = torch.device('cuda')
    model_path = 'Dongjin-kr/ko-reranker'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        scores_2 = outputs.logits.view(-1).cpu().numpy()

    # weighted sum between scores_1 and scores_2
    weights_1 = 3  # BM25 점수의 가중치
    weights_2 = 1  # Re-ranker 점수의 가중치
    combined_scores = weights_1 * scores_1 + weights_2 * scores_2  

    top_3 = np.argsort(combined_scores)[0][len(combined_scores)-3:]

    content = ''

    for i in top_3:
        content += corpus[i]

    file_path = f'./retriever_{label}.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

    print('The End')

def generator(label, query):
    '''
        label: conveyer, electricity, painting, chemistry, transportation,
                bone_disease, inversion, forklift, crane, workplace
    '''
    path = f'./retriever_{label}.json'
    content = read_json(path)

    # zero-shot 
    # prompt = ChatPromptTemplate.from_template("지시문: 근로자를 위한 안전 교육 자료를 만들거야. 너는 안전 교육관으로서 질문에 대해 검색된 문서를 바탕으로 친절하게 답변해줘. 모든 대답은 한국어(Korean)으로 대답해줘. 답변은 불렛 형식으로 만들어주고 각각에 대해 '~해야 합니다'라고 문장을 끝내줘.\n 질문: {query}\n 검색된 문서: {content}\n 답변: ")
    
    # one-shot
    prompt = ChatPromptTemplate.from_template("지시문: 너는 비상대응 시나리오 작성 전문가야. 모든 대답은 한국어(Korean)으로 대답해줘. \n질문 : 화재에 대한 비상대응 시나리오를 작성해줘. \n답변: <비상대응 시나리오 (화재)>\n1단계 '최초발견자: 비상경보발령(화재발신기) -> 화재신고 (119, 사내 7119번) -> 사무실 보고 (사내 5612번)'\n2단계 '분말소화기 이용 화재진압 및 작업자 대피, 비고: 00공장 앞 00명 대피완료'\n 3단계 '자체 소방대 출동 -> 소화 작업 및 구호 활동'\n질문: {query} \n답변: ")

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    output_parser = StrOutputParser()

    # chaining : prompt + model + output parser
    chain = prompt | llm | output_parser
    # result = chain.invoke({"query": query, "content": content})
    result = chain.invoke({"query": query})
    print(result)

    file_path = f'./generator_{label}.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print('The End')

def translator(label, language):
    '''
        label: conveyer, electricity, painting, chemistry, transportation,
                bone_disease, inversion, forklift, crane, workplace
        language: Chinese, English, Vietnamese, Thai
    '''
    path = f'./generator_{label}.json'
    content = read_json(path)
    
    if language == 'Chinese':
        prompt = ChatPromptTemplate.from_template("지시문: 너는 중국어 번역 전문가야. 아래 내용을 중국어로 번역해줘. \n내용 : {query} \n답변: ")
    elif language == 'English':
        prompt = ChatPromptTemplate.from_template("지시문: 너는 영어 번역 전문가야. 아래 내용을 영어로 번역해줘. \n내용 : {query} \n답변: ")
    elif language == 'Vietnamese':
        prompt = ChatPromptTemplate.from_template("지시문: 너는 베트남어 번역 전문가야. 아래 내용을 베트남어로 번역해줘. \n내용 : {query} \n답변: ")
    elif language == 'Thai':
        prompt = ChatPromptTemplate.from_template("지시문: 너는 태국어 번역 전문가야. 아래 내용을 태국어로 번역해줘. \n내용 : {query} \n답변: ")

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    output_parser = StrOutputParser()

    # chaining : prompt + model + output parser
    chain = prompt | llm | output_parser
    result = chain.invoke({"query": content}) # generation

    file_path = f'./generator_{label}_{language}.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print('The End')
