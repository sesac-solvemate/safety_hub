import pandas as pd
from util import *

# # 제조업 예방자료
# file_path = '/home/ny/Safety_Hub/data/제조업_[2024-산업안전실-174]_안전보건공단(장마철길잡이 2023)이홍석-내지-웹용(최ᄌ.pdf'
# saved_path = '/home/ny/Safety_Hub/data/Manufacturing_rainy1.csv'

# /home/ny/Safety_Hub/data/제조업_[2023-교육혁신실-992] 240109 [안전보건공단] 직업계고 카드북3_금속성형기계작ᄋ.pdf
# /home/ny/Safety_Hub/data/제조업_[2023-교육혁신실-993] 240109 [안전보건공단] 직업계고 카드북4_금속절삭기계_인.pdf
# /home/ny/Safety_Hub/data/제조업_[2023-교육혁신실-994] 240221 [안전보건공단] 직업계고 카드북5_식품제조작업_인.pdf
# /home/ny/Safety_Hub/data/제조업_[2024-산업안전실-174]_안전보건공단(장마철길잡이 2023)이홍석-내지-웹용(최ᄌ.pdf

# pages = range(26, 71)

# pdf2csv(pages, '제조업', file_path, saved_path)

# # 건설업 예방자료 
# /home/ny/Safety_Hub/data/건설업_[2023-건설안전실-625]_231123 2023년 동절기 건설현장.pdf
# /home/ny/Safety_Hub/data/건설업_[2024-건설안전실-63] [2024-건설안전실-63]_해빙기 안전보건 길잡이.pdf
# /home/ny/Safety_Hub/data/건설업_[2024-건설안전실-234]_2024 장마철 건설현장 길잡이_홈페이지.pdf

# file_path = '/home/ny/Safety_Hub/data/Constructing_prevence.pdf'
# saved_path = '/home/ny/Safety_Hub/data/Constructing_prevence.csv'
# pages = range(83, 101)

# file_path = '/home/ny/Safety_Hub/data/건설업_[2024-건설안전실-234]_2024 장마철 건설현장 길잡이_홈페이지.pdf'
# saved_path = '/home/ny/Safety_Hub/data/Constructing_rainy1.csv'
# pages = range(17, 67)

# pdf2csv(pages, '건설업', file_path, saved_path)

# from tika import parser
# pdf_path = "/test.pdf"
# parsed = parser.from_file(pdf_path)
# txt = open('output.txt', 'w', encoding = 'utf-8')
# print(parsed['content'], file = txt)
# txt.close()

# file_path = '/home/ny/Safety_Hub/data/건설업_[2024-건설안전실-63] [2024-건설안전실-63]_해빙기 안전보건 길잡이.pdf'
# saved_path = '/home/ny/Safety_Hub/data/Constructing_thaw1.csv'
# pages = range(15, 54)
# parsed = parser.from_file(file_path)
# txt = open('output.txt', 'w', encoding = 'utf-8')

# pdf2csv(pages, '건설업', file_path, saved_path)

# with open("test.csv", "wt", encoding = 'utf8') as f: # wt: write mode
#     writer = csv.writer(f)
#     writer.writerows(rows)


# file_path = '/home/ny/Safety_Hub/data/한전케이피에스주식회사_산업안전 및 사고예방에 관한 사항_20231231.pdf'
# saved_path = '/home/ny/Safety_Hub/data/prac.csv'

# pages = range(0, 21)

# pdf2csv(pages, '제조업, 건설업', file_path, saved_path)

path = '/home/ny/Safety_Hub/data/disease.csv'
# saved_path = '/home/ny/Safety_Hub/data/prac.csv'
df = pd.read_csv(path, encoding='cp949')
df.to_csv(path, index=False)