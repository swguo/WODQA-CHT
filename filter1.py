import unit.helper as h
import unit.IR as ir
import pandas as pd
from tqdm import tqdm


import jieba
from jieba import posseg

df = pd.read_csv('index/wiki_entity.csv')
ent_list = h.entity_select(df,10000) 

ent_list_df = pd.DataFrame(ent_list,columns=['ent'])
ent_list_df.to_csv('ent_list-f1.csv',index=None)