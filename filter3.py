import requests
from bs4 import BeautifulSoup 
from googlesearch import search
from tqdm import tqdm
import pandas as pd
# 使用 google serarch 查找維基百科，回傳答案
def google_search(q):
    page_list = []
    page_lists =  search(q, stop=3, pause=2.0,lang='zh-tw')
    
    for p in page_lists:
        page_list.append(p)
    
    
    ans_set = []
    sentence_set=[]
    for p in tqdm(page_list,desc='google search'):
        print('web page')
        print(p)
        if (not 'zh.m.wikipedia.org' in p)  \
        and (not 'zh.wiki.hancel.org' in p)  \
        and (not 'zh.wikipedia.org' in p):
            continue
        
        # making requests instance
        reqs = requests.get(p,verify=False) #解決 sslcertverificationerror
        
        if reqs.status_code != requests.codes.ok:
            continue
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')  
        
        # 維基百科中的內文
        ans_for_body = ''
        for pv in soup.find_all('p'):
            ans_for_body = ans_for_body+' '+pv.get_text()
        ans_for_body = ans_for_body.replace("\n", "")
        ans_for_body = ans_for_body.replace("\r", "")
        ans_for_body = ans_for_body.strip()    
        ans_for_body = ans_for_body.split('。')[:3]       
        
        
        # 維基百科中的標題
        ans_for_h1 = soup.find('h1',{'class':'firstHeading'})
        ans_set.append([ans_for_h1.get_text(),ans_for_body])
        
    if not ans_set:
        return False
    else:
        return ans_set

import unit.helper as h
def is_answerable(q_origin,q_search,ans):    
    can_answerable = False
    max_r = 0.0
    ans=''
    for q in q_search:
        can_answerable = False
        print(f'g entity :{q[0]}')
        print(q[1])    
        
            
        for page in q[1]:   
            if not page: #如果沒有適合的網頁
                continue
            print(f'into rouge {page},{q_origin},{ans}')            
            rouge_score = h.cn_lawrouge(page,q_origin+','+ans)
            print(f'page: {page},rouge: {rouge_score["p"]}')      
            if rouge_score['p'] > max_r :
                max_r = rouge_score['p']
                ans = q[0]
    return max_r, ans

from os.path import exists
path_to_file = f'odqa_f2_jaccard_cn.csv'
if exists(path_to_file):
    df = pd.read_csv(path_to_file)
else:
    print('找不到檔案')


from tqdm import tqdm
import csv
answerable = []
rouge_score = []
with tqdm(df.iterrows(),total=df.shape[0]) as t:
    try:    
        with open(f'ODQA-Dataset-f3-stream.csv', 'a', newline='') as sfile:
            writer = csv.writer(sfile)
            
            for idx,data in tqdm(t,desc='QA'):                
                print(f'{idx}, Q:{data.q} A:{data.answer} LEN:{data.len}')
                print('='*100) 
                # 問題太短或問題太長都不適合用來做google search，直接放棄這種問題
                if len(data.q) <= 10 or len(data.q) > 45:                
                    print('不可回答')
                    answerable.append(False)
                    rouge_score.append(0)
                    writer.writerow([False,0])                    
                    continue
                q_search = google_search(data.q)
                
                is_answerable_boo = False
                # 如果這個頁面已死，略這一頁
                if not q_search :
                    print('網頁已死')
                    answerable.append(False)
                    rouge_score.append(0)
                    writer.writerow([False,0])
                else:
                    # 透過google search 查出來文章前3段獲取最高rouge分數
                    max_rouge_score,ans = is_answerable(data.q,q_search,data.answer)
                    print(f'rouge_score {max_rouge_score}')
                    
                    if (max_rouge_score >= 0.5) or (ans == data.answer):                    
                        print('可回答')
                        is_answerable_boo = True
                        answerable.append(is_answerable_boo)
                        
                        rouge_score.append(max_rouge_score)
                    else:
                        print('不可回答')
                        is_answerable_boo = False
                        answerable.append(is_answerable_boo)
                        rouge_score.append(max_rouge_score)

                    print('\n')
                    
                    writer.writerow([is_answerable_boo,max_rouge_score])
        sfile.close()
    except KeyboardInterrupt:
        t.close()
        raise
    t.close()

df['answerable'] = answerable
df['max_rouge'] = rouge_score
answerable_df = df.loc[df['answerable']==True]
answerable_df.to_csv(f'odqa_f3_cn.csv',index=None)


