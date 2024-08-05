import sys
import pandas as pd

from util import *
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

##############  Data crawling ##############
file_path = './작업 중.pdf'
saved_path = './danger22.csv'
pages = range(0, 1)
pdf2csv(pages, '컨베이어', file_path, saved_path)

##############  Data chunking ##############
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap  = 100,
    length_function = len,
)

for i in tqdm(range(1, 23)):
    data_list = []
    file_path = f'./cond_danger{i}.csv'
    df = pd.read_csv(file_path)
    
    loader = CSVLoader(file_path=file_path, encoding='utf-8')
    data = loader.load()
    
    texts = text_splitter.split_text(data[0].page_content)

    for j in range(len(texts)):
        data_list.append(texts[j])

    data_df = pd.DataFrame(data_list)
    data_df.to_csv(file_path, index=False, encoding='utf-8-sig')
print('The End')

##############  Data labeling : 위험 요인 ##############
path = './cond_danger22.csv'
df = pd.read_csv(path)
df['label'] = None

for i in range(len(df)):
    df['label'][i] = '컨베이어' 

df.to_csv(path, index=False)

##############  Data concatenation ##############
conveyer_list = []
electricity_list = []
painting_list = []
chemistry_list  = []
bone_disease_list = []
inversion_list = []
forklift_list = []
crane_list = []
transportation_list = []
workplace_list = []

for i in range(1, 23):
    path = f'./cond_danger{i}.csv'
    df = pd.read_csv(path)

    if df['label'][0] == '컨베이어':
        conveyer_list.append(path)
    elif df['label'][0] == '전기':
        electricity_list.append(path)
    elif df['label'][0] == '도장':
        painting_list.append(path)
    elif df['label'][0] == '화학':
        chemistry_list.append(path)
    elif df['label'][0] == '근골질환':
        bone_disease_list.append(path)
    elif df['label'][0] == '전도':
        inversion_list.append(path)
    elif df['label'][0] == '지게차':
        forklift_list.append(path)
    elif df['label'][0] == '크레인':
        crane_list.append(path)
    elif df['label'][0] == '인력운반':
        transportation_list.append(path)
    elif df['label'][0] == '작업장':
        workplace_list.append(path)

# total = conveyer + electricity + painting + chemistry + bone_disease + inversion + forklift + crane + transportation + workplace
# print(len(total))

df_concat('conveyer', conveyer_list)
df_concat('electricity', electricity_list)
df_concat('painting', painting_list)
df_concat('chemistry', chemistry_list)
df_concat('bone_disease', bone_disease_list)
df_concat('inversion', inversion_list)
df_concat('forklift', forklift_list)
df_concat('crane', crane_list)
df_concat('transportation', transportation_list)
df_concat('workplace', workplace_list)
