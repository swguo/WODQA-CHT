import unit.helper as h
import unit.IR as ir
import pandas as pd
from tqdm import tqdm
import re



import numpy as np
from scipy import spatial
import jieba
jieba.set_dictionary(f'data/dict.txt-wiki.big.txt')
# 計算相關係數  jaccard score
def cal_cc(x,y):    
    j_score = h.jaccard(x, y)
    return j_score  

# 轉換 keyword 為兩個 one-hot encode 矩陣    
def key_mapping(items,Q_items):          
    idx_mapping = dict((val,key) for key,val in enumerate(items))     
    items_mapping = [1]*len(items)
    
    Q_items_mapping = []

    for item in items:
      boo = False
      for q_item in Q_items:
        if item == q_item:
          Q_items_mapping.append(1)
          print(f'{item},{q_item}')
          boo = True
          break
      if not boo:
        Q_items_mapping.append(0)
    return  items_mapping,  Q_items_mapping
    print(f'len:{len(Q_items_mapping)},{Q_items_mapping}')

def run():
  q_QA_pair_df_f_all = pd.read_csv('ODQA-Dataset-qg-stream.csv')
  q_item_set = []

  for index,row in tqdm(q_QA_pair_df_f_all.iterrows(),total=q_QA_pair_df_f_all.shape[0]):
      #if index > 10 :
      #    break
      #print(f'{index}')
      print(f'Entity:{row.a}')
      #print(row.article)
      keywords = h.extract_tfidf_kw(row.article) 
      
      print("Article：keywords : ",keywords)
      
      
      Q = row.q.replace("\n", "").strip()  # 刪除換行和多餘的空格
      Q_list = list(jieba.cut(Q, cut_all=False))    # jieba分詞
      #print("jieba分詞後：",content_seg)  
          
      #print(f'去停用詞之前Q {Q_list}')
      # 去除停用詞
      Qcontent = h.movestopwords(Q_list)
      
      # 去除空白
      Qcontent = Qcontent.strip()
      
      #print(f'去停用詞之後Q {Qcontent}')
      Qcontent = [x.strip() for x in Qcontent.split(' ')] 
      q_item = list(dict.fromkeys(Qcontent))
      
      # 去除空白的資料
      q_item = [x.strip() for x in q_item if x.strip()!='']
      print("Question：keywords : ", q_item)
      #print('\n')

      
      # 將關鍵字轉換成 one-hot encode 格式 ex:[1,0,1,0,1,1]
      items_mapping,  Q_items_mapping = key_mapping(keywords,q_item)
      # 計算兩個矩陣相關係數
      j_score = cal_cc(items_mapping,  Q_items_mapping)
      print(f'{row.q} {j_score}')
      
      
      
      q_item_set.append([row.q,
                        j_score,
                        ','.join(keywords),
                        ','.join(q_item),
                        row.article,
                        row.a,
                        row.iw,
                        row.v,
                        row.n,
                        row.dup,
                        row.len,
                        ])

  q_item_set_df = pd.DataFrame(q_item_set,columns=['q','jaccard','aitm','qitm','article','answer','iw','v','n','dup','len'])

  mask = (q_item_set_df['q'].str.len() > 10) & (q_item_set_df['q'].str.len() <= 45)
  q_item_set_df = q_item_set_df.loc[mask]

  q_item_set_df = q_item_set_df.loc[q_item_set_df[['iw','v','n','dup']].sum(axis=1)==4]

  q_item_set_df = q_item_set_df.loc[~q_item_set_df['q'].index.duplicated(),:].copy()


  p = re.compile(r'[^\w\s]+')
  q_item_set_df['q'] = [p.sub('', x) for x in q_item_set_df['q'].tolist()]
  q_item_set_df['q'] = q_item_set_df['q']+'?'

  q_item_set_jaccard_df = q_item_set_df.loc[q_item_set_df['jaccard']>0.1]
  q_item_set_jaccard_df.to_csv(f'odqa_f2_jaccard_cn.csv',index=None)
