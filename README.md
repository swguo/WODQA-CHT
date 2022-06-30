# WODQA-CHT
WODQA-CHT : A Dataset and Baselines for Traditional Chinese Wikipedia Open Domain QA

# setup
```
pip install -q -r requirement.txt
```
# Inverted Index for wiki Corpus
```
python -m pyserini.index.lucene \\ <br>
  --collection JsonCollection \\  <br>
  --input corpus \\  <br>
  --language zh \\  <br>
  --index Index/Wiki_Chinese \\  <br>
  --generator DefaultLuceneDocumentGenerator \\  <br>
  --threads 1 \\  <br>
  --storePositions --storeDocvectors --storeRaw
```  
  
 # Running
 
 ## Naive QG without filter
 ```
 python main.py -t naive
 ```
 
 ## Entity pass filter-1
 ```
 python main.py -t f1
 ```
 
 ## Question pass filter-1&2
 ```
 python main.py -t f2
 ```
  
 ## Full filter passed
 ```
 python main.py -t all
 ```
 
 # Framework
![image](https://user-images.githubusercontent.com/5722978/176619116-018ca6cc-835c-4c88-9435-a4fae1e42cfe.png)


 # Baseline Sore
 
| Dataset  | EM  | F1  |  Example | Avg.Len(q)  | Avg.Len(a)  |  
|---|---|---|---|---|---|
|  Naive            | 29.30 %  | 26.90 %  | 1k  | 21.58  | 4.67  |
|  F1 filter        | 32.23 %  | 30.77 %  | 1k  | 21.17  | 5.69  |
|  F1+F2 filter     | 35.40 %  | 34.35 %  | 1k  | 26.25  | 5.79  |
|  F1+F2+F3 filter  | 64.71 %  | 60.94 %  | 425 | 26.76  | 5.96  |

EM : Exact Match <br>
F1 : F1 score <br> 
Examples: number of QA pairs <br>
Avg. Len(q) : The avg length of questions <br>
Avg. Len(a) : The avg length of answers <br>
