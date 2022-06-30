from pyserini.search.lucene import LuceneSearcher
from pyserini.index import IndexReader
import json
import re
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import requests
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("nyust-eb210/braslab-bert-drcd-384")
model = AutoModelForQuestionAnswering.from_pretrained("nyust-eb210/braslab-bert-drcd-384")
searcher = LuceneSearcher('../Index/Wiki_Chinese')
index_reader = IndexReader('../Index/Wiki_Chinese')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = AutoModelForQuestionAnswering.from_pretrained("nyust-eb210/braslab-bert-drcd-384").to(device)

def Retreiver(quesion):
    searcher.set_language('zh')
    hits = searcher.search(quesion, k=10)
      # for hit in hits:
        # print(hit.raw)
    return hits

def simpleReader(text, query):
    

  encoded_input = tokenizer(text, query, return_tensors="pt").to(device)
  qa_outputs = model(**encoded_input)

  start = torch.argmax(qa_outputs.start_logits).item()
  end = torch.argmax(qa_outputs.end_logits).item()
  answer = encoded_input.input_ids.tolist()[0][start : end + 1]
  answer = "".join(tokenizer.decode(answer).split())

  start_prob = torch.max(torch.nn.Softmax(dim=-1)(qa_outputs.start_logits)).item()
  end_prob = torch.max(torch.nn.Softmax(dim=-1)(qa_outputs.end_logits)).item()
  confidence = (start_prob + end_prob) / 2
  return answer


def answerPosFinder(cxt, ans):
  start = cxt.find(ans)
  end = start+len(ans)
  ans_pos = [(m.start(), m.end()) for m in re.finditer(ans, cxt)]

  QGpairs=[]
  for i in ans_pos:
    pair = {"article":cxt,
            "answers":{
                "ans_detail":[
                  {
                      "tag":ans,
                      "start_at":i[0],
                      "end_at":i[1]
                  }            
                ]
            }
            }
    QGpairs.append(pair)
      
  return QGpairs


def EntityRetriver(entity):
    hits = Retreiver(entity)
    QA_pair = []
    
    #print(f'Total of aritcle: {len(hits)}\n')
    for idx,i in enumerate(hits):
      #print(f'artical {idx}\n')
      
      qanswer = entity
      ctx = json.loads(i.raw)["contents"]  
      #print(f'artical {ctx}\n')
      for qa in answerPosFinder(ctx, qanswer):
        #print(f'Number of hit in article: {len(qa)}')
        r = requests.post("https://ch-api.queratorai.com/generate-question", json=qa)
        if "question_detail" in json.loads(r.text):
            for q in json.loads(r.text)["question_detail"][0]["question"]:
              #print({"question":q, "answer":qanswer})
              QA_pair.append({"article":qa['article'],"question":q, "answer":qanswer})
        if len(QA_pair) >=100 :
            break

    QA_pair_df = pd.DataFrame(QA_pair)
    return QA_pair_df

def EntityRetriver2(entity):
    hits = Retreiver(entity)
    QA_pair = []
    
    return []
    