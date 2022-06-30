import re 
from jieba import posseg
from nltk.translate.bleu_score import sentence_bleu
from sklearn.metrics import jaccard_score
import jieba
import jieba.analyse

#載入包含維基百科 Entity 的分詞表

#jieba.analyse.set_idf_path(f'v2/idf.txt-wiki.big.txt')
jieba.set_dictionary(f'v2/dict.txt-wiki.big.txt')
jieba.analyse.set_stop_words(f'../extra_data/stopwords_cn.txt')

# 自動篩選合格 entity
def entity_select(df,top_n=100):
    # 挑選沒有特殊符號的 entity
    # 預設挑100個 entity
    ent_list = []
    idx = 0
    for ent in df['title']:
        if idx >= top_n:
            break
        if (not check_symbol(ent)) \
                and (not check_num(ent)) \
                and (not check_letter(ent)) \
                and (len(ent)>3):
            ent_list.append(ent)
            idx=idx+1
            
    return ent_list
            
    
# 判斷字串是否包含指定符號
def check_symbol(string):
    # import required package 
    # Function checks if the string 
    # contains any special character 
    # Make own character set and pass  
    # this as argument in compile method 
    regex = re.compile('[@_!#$%^&\+\-\－*()<>?/\|·}{~:]') 

    # Pass the string in search  
    # method of regex object.     
    if(regex.search(string) == None): 
        return False # 沒有特殊符號

    else: 
        return True # 包含特殊符號
    
# 判斷字串是否包含數字
def check_num(string):  
    regex = re.compile('\d')  
    if(regex.search(string) == None): 
        return False # 沒有數字

    else: 
        return True # 包含數字
    
# 判斷字串是否包含字母 
def check_letter(string):
    regex = re.compile('[A-Za-z]')  
    if(regex.search(string) == None): 
        return False # 沒有字母

    else: 
        return True # 包含字母
    
# 去除數字、字母和符號
def remove_letter_symbol(string):
    # 去除數字
    s = re.sub(r'[\d+]','',string)
    # 去除特殊符號
    s = re.sub(r'[^\w]','',s)
    # 去除英文字母
    s = re.sub(r'[A_Za_z]','',s)
    
    return s
# 篩選品質好的 Question
# jeiba 詞性表 https://blog.csdn.net/qq_16494381/article/details/123531446
def filter_q(df,top_n=100):
    b_qaulity_q = []
    # Interrogative word 疑問詞
    IW = ['哪','誰','哪裡','什麼']
    check_list = []
    
    for idx,q in enumerate(df.iterrows()):
        
        article =q[1]['article']
        quest = q[1]['question']
        ans = q[1]['answer']
        if idx>top_n:
            break   
            
        # 問題中出現UNK的不適合出題
        if '[UNK]' in quest:
            continue
            
        words = posseg.cut(q[1]['question'])
        
        check_col = {'id':q[0],'article':article,'q':quest,'a':ans,'iw':0,'v':0,'n':0,'dup':0}
        
        # 1. 檢測各條件欄位
        for word, flag in words:
            #print(f'{word} {flag}') 
            if word in IW  :
                check_col['iw']=1
                
            if 'n' in flag or flag.lower() in ['loc','per','org','f','vn','nr','ns','nw','nz','s']:
                check_col['n']=1
                
            if 'v' in flag or flag.lower() in ['vd']:
                check_col['v']=1
                
        if not q[1]['answer'] in q[1]['question']:
            check_col['dup'] = 1
        
        b_qaulity_q.append(check_col)
           
        
    return b_qaulity_q

# question 滿足屬性欄位條件
def q_propty_ck():
    
    return []
# 透過 google search對question 和 answer 可回答性檢測
def q_m_s_ck():
    
    return []


#define Jaccard Similarity function
# https://www.statology.org/jaccard-similarity-python/
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html
# macro : 計算每個標籤的指標，並找到它們的未加權平均值。這沒有考慮標籤不平衡。
# weighted : 計算每個標籤的指標，並找到它們的平均值，按支持度加權（每個標籤的真實實例數）。這會改變“宏觀”以解決標籤不平衡問題。
def jaccard(y_true, y_pred):
    j = jaccard_score(y_true, y_pred, average="micro")
    return j

    
import requests
from bs4 import BeautifulSoup 
from googlesearch import search

# 使用 google serarch 查找維基百科，回傳答案
def google_search(q):
    page_list = list(search(q, num_results=3,lang='zh-tw'))
    ans_set = []
    for p in page_list:
        if (not 'zh.m.wikipedia' in p) and (not 'zh.wiki' in p):
            continue
        print(p)
        # making requests instance
        reqs = requests.get(p)
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')  
        
        # displaying the title
        ans_for_title = soup.find('title')
        ans_set.append(ans_for_title.get_text())  
        
        # 維基百科中的標題
        ans_for_h1 = soup.find('h1',{'class':'firstHeading'})
        ans_set.append(ans_for_h1.get_text())
    
    return ans_set     
    
# 創建停用詞list  
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords

stopwords = stopwordslist('../extra_data/stopwords_cn.txt')  # 這裏加載停用詞的路徑

# 移除句子內的停用字
def movestopwords(sentence):
    print('in movestopwords fun')
    outstr = ''
    for word in sentence:           #句子中的每一個字，
        #print(word)
        if word not in stopwords:   #這裏和英文不一樣，應爲如果這樣用，就是字母了
            if word != '\t'and'\n':
                outstr += word
                outstr += " "    #確實不需要這句，word本身就有可能是空格
    return outstr

# 用結巴取關鍵字(TFIDF)
def extract_tfidf_kw(sentence):
    # , allowPOS=('n','nr','ns','a','nw','org','per','loc')
    keywords = jieba.analyse.extract_tags(sentence, topK=25, withWeight=True)

    return [k[0].strip() for k in keywords]

def BLEU(reference, candidate):
    b1 = sentence_bleu(reference, candidate,weights=(1, 0, 0, 0))   
    b2 = sentence_bleu(reference, candidate,weights=(0.5, 0.5, 0, 0)) 
    b3 = sentence_bleu(reference, candidate,weights=(0.33, 0.33, 0.33, 0))
    b4 = sentence_bleu(reference, candidate,weights=(0.25, 0.25, 0.25, 0.25))
    
    return b1,b2,b3,b4

import lawrouge
rouge = lawrouge.Rouge()


def cn_lawrouge(Q,A1):
    scores = rouge.get_scores([Q], [A1], avg=2) 
    return scores
    
    