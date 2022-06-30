import re
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score


def getUnique(df_ans):
        return pd.unique(df_ans).tolist()
def f1(y_true,y_pred):
    print(type(y_true))
    print(type(y_pred))
    f1_s = f1_score(y_true, y_pred, average='micro')
    return f1_s
def mean(df):
    # Question
    print(f'Average length of quetstion : {df["q"].apply(len).mean()}')
    # True ans
    print(f'Average length of quetstion : {df["true"].apply(len).mean()}')

def key_mapping(answer_df):
    uniquw_key = getUnique(answer_df['true'])

    idx_mapping = dict((val,key) for key,val in enumerate(uniquw_key)) 

    t_answer = pd.DataFrame()
    t_answer['true'] = answer_df['true']
    # True Answer mapping idx
    t_answer['idx'] = t_answer['true'].replace(idx_mapping)
    
    
    p_answer = pd.DataFrame()
    p_answer['predict'] = answer_df['predict']
    p = re.compile(r'[^\w\s]+')
    p_answer['predict'] = [p.sub('', str(x)) for x in p_answer['predict'].tolist()]
    # Prediction Answer name mapping to idx
    p_answer['idx'] = np.where(~p_answer['predict'].isin(uniquw_key) , -1, p_answer['predict'].replace(idx_mapping))
    
    return t_answer,p_answer

def em(QA_Pair):
    count = 0
    for idi,datai in QA_Pair.iterrows():
        #print(f'{datai.q},{datai.predict}')
        for idj,dataj in QA_Pair.iterrows():
            if datai.q == dataj.q and datai.predict == dataj.true:
                count = count +1
    em = count/QA_Pair.shape[0]
    return em

def run(pred_f3_cn_str,odqa_f3_cn_str):
  answer_df = pd.read_csv(f'qa_predict/nyust-eb210/braslab-bert-drcd-384/LuceneSearcher/{pred_f3_cn_str}.csv')
  quest_df = pd.read_csv(f'{odqa_f3_cn_str}.csv')
  answer_df['q'] = quest_df['q']

  t_answer,p_answer = key_mapping(answer_df)
  f1_score = f1(t_answer['idx'].to_list(),p_answer['idx'].to_list())
  em_score = em(answer_df)

  print(f1_score)
  print(em_score)

  mean(answer_df)

