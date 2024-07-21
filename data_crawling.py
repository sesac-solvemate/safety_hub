from util import *

# 제조업 예방자료
file_path = '/home/ny/Safety_Hub/Manufacturing_prevence.pdf'
saved_path = '/home/ny/Safety_Hub/Manufacturing_prevence.csv'
pages = range(109, 124)

pdf2csv(pages, '제조업', file_path, saved_path)

# 건설업 예방자료 
file_path = '/home/ny/Safety_Hub/Constructing_prevence.pdf'
saved_path = '/home/ny/Safety_Hub/Constructing_prevence.csv'
pages = range(97, 101)

pdf2csv(pages, '건설업', file_path, saved_path)