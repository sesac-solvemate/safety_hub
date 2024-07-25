import os
import re
import json

import numpy as np
import pandas as pd

from pypdf import PdfReader

def pdf2csv(pages, label, file_path, saved_path):
    '''
        pages: range(i, j)
        label: 제조업 or 건설업
        file_path : pdf file path
        saved_path : csv file saved path
    '''
    data = []   
    header = ['label', 'text']

    reader = PdfReader(file_path)

    for i in pages:
        page = reader.pages[i]
        text = page.extract_text()
        # with open(saved_path, "wt", encoding = 'utf8') as f: # wt: write mode
        #     writer = csv.writer(f)
        #     writer.writerows(rows)

        # 글자 깨지는 부분 제거
        clean_text = re.sub(r'[^\u3131-\u3163\uac00-\ud7a3a-zA-Z0-9\s.,%ㆍ•]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        data.append((label, clean_text))

    data_df = pd.DataFrame(data)
    # data_df.to_csv(saved_path, index=False, header=header, encoding='utf-8-sig')
    data_df.to_csv(saved_path, index=False, header=header)
    
    print(f'Saving the file : {saved_path}')

def exp_normalize(x):
    '''
        scoring the similarity between gold and query
        x: retrieved documents
    '''
    b = x.max()
    y = np.exp(x - b)

    return y / y.sum()

def read_json(path):
    '''
        path: json file path
    '''
    with open(path, encoding='utf-8') as f:
        text = json.load(f)

    return text

def read_csv(path):
    '''
        path: csv file path
    '''
    df = pd.read_csv(path, encoding='utf-8')
    
    doc = []
    for i in range(len(df)):
        text = df['text'][i]
        doc.append(text)

    return doc


