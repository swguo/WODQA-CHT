import unit.helper as h
import unit.IR as ir
import pandas as pd
from tqdm import tqdm
import jieba.analyse
import numpy as np
from scipy import spatial
import csv

def run():
  ent_list_df = pd.read_csv(f'ent_list-f1.csv')
  ent_list = ent_list_df['ent'].tolist()
  e_idx = -1
  print(f'共有 {len(ent_list)} 個 Entity')
  q_QA_pair_df_f_all = pd.DataFrame()
  with open('ODQA-Dataset-qg-stream.csv', 'a', newline='') as sfile:
      writer = csv.writer(sfile)
      #加入 csv 標題
      if e_idx<0:
          writer.writerow(['id','q','a','article','iw','v','n','dup','len'])
      for ent in tqdm(ent_list[e_idx+1:]):
          print(ent) 
          # 查詢文章
          QA_pair_df = ir.EntityRetriver(ent)
          
          # 篩選品質好的 Question
          q_QA_pair = h.filter_q(QA_pair_df)
          print(q_QA_pair) 
          # 如果沒資料，不紀錄這筆Q
          if not q_QA_pair: # List is empty
              continue

             
          q_QA_pair_df_f = pd.DataFrame(q_QA_pair)

          q_QA_pair_df_f['len'] = q_QA_pair_df_f['q'].str.len() 


          for index,row in tqdm(q_QA_pair_df_f.iterrows(),total=q_QA_pair_df_f.shape[0]):           

              writer.writerow([row.id,
                                  row.q,
                                  row.a,
                                  row.article,
                                  row.iw,
                                  row.v,
                                  row.n,
                                  row.dup,
                                  row.len])

          q_QA_pair_df_f_all = pd.concat([q_QA_pair_df_f_all,q_QA_pair_df_f], axis=0, ignore_index=True)