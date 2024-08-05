from util import *
from engine import *

label_list = ['conveyer', 'electricity', 'painting', 'chemistry', 'transportation', 'bone_disease', 'inversion', 'forklift1', 'forklift2', 'forklift3', 'crane', 'workplace', '끼임/깔림/부딪힘', '화재']

path = './prompt.json'
content = read_json(path)

############## Generate the context ##############
for label in label_list:
    query = content['label']

    retriever(label, query)
    generator(label, query)

print('The End : Generation Mode')

############## Translate the context ##############
for label in label_list:
    query = content['label']

    translator(label, 'Chinese') 
    translator(label, 'English') 
    translator(label, 'Vietnamese') 
    translator(label, 'Thai') 

print('The End : Translation Mode')

