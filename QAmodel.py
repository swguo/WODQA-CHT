import unit.helper as h
import pandas as pd
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import json
from pyserini.search.lucene import LuceneSearcher
from pyserini.index import IndexReader
import os

model_name = "nyust-eb210/braslab-bert-drcd-384"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

RETREIVAL_MOD = 'LuceneSearcher'
searcher = LuceneSearcher('Index/Wiki_Chinese')
index_reader = IndexReader('Index/Wiki_Chinese')
searcher.set_language('zh')



def Retreiver(quesion):
  
  hits = searcher.search(quesion, k=20)
  # for hit in hits:
    # print(hit.raw)
  return hits

def simulate_search(hits,q):
    jdata = json.loads(searcher.doc(hits[0].docid).raw())
    p_a = simpleReader(jdata["contents"],q)
    return p_a

def simpleReader(text, query):
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForQuestionAnswering.from_pretrained(model_name).to(device)
  encoded_input = tokenizer(text, query, 
                            padding=True, 
                            truncation=True,
                            max_length=512,
                            return_tensors="pt",
                            add_special_tokens = True).to(device)
  qa_outputs = model(**encoded_input)
  start = torch.argmax(qa_outputs.start_logits).item()
  end = torch.argmax(qa_outputs.end_logits).item()
  answer = encoded_input.input_ids.tolist()[0][start : end + 1]
  answer = "".join(tokenizer.decode(answer).split())

  start_prob = torch.max(torch.nn.Softmax(dim=-1)(qa_outputs.start_logits)).item()
  end_prob = torch.max(torch.nn.Softmax(dim=-1)(qa_outputs.end_logits)).item()
  confidence = (start_prob + end_prob) / 2
  return answer


def Prediction(data_df):
    for index,data in tqdm(data_df.iterrows(),total=data_df.shape[0]):
        if data.answerable:
            print(f'index:{index}')
            q = data.q
            print(f'question:{q}')
            hits = searcher.search(q)
            pre_answer = simulate_search(hits,q)
            print(f'true : {data.answer}, pred answer: {pre_answer}')
            answer_set.append([data.answer,pre_answer])
        else:
            answer_set.append([data.answer,''])

    answer_df = pd.DataFrame(answer_set,columns=['true','predict'])
    
    return answer_df

def run(filter,odqa_pred_str,odqa_ans_str):

  answer_set = []

  if not os.path.exists(f'qa_predict/{model_name}/{RETREIVAL_MOD}'):
    os.makedirs(f'qa_predict/{model_name}/{RETREIVAL_MOD}')

  data_df = pd.read_csv(f'{odqa_pred_str}.csv')
  if filter != 'f3':
    data_df['answerable'] = True

  answer_df = Prediction(data_df.loc[:999])

  answer_df.to_csv(f'qa_predict/{model_name}/{RETREIVAL_MOD}/{odqa_ans_str}.csv',index=None)
