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
![image](https://user-images.githubusercontent.com/5722978/181149462-6312c8a2-1242-487e-bfb4-ceacbe58a55b.png)


 # Baseline Sore
 
| Dataset  | EM  | F1  | Avg.Len(q)  | Avg.Len(a)  |  
|---|---|---|---|---|
|  Without filter   | 29.30 %  | 26.90 %  | 21.58  |
|  F1 filter        | 32.23 %  | 30.77 %  | 21.17  |
|  F1+F2 filter     | 35.40 %  | 34.35 %  | 26.25  |
|  F1+F2+F3 filter  | 61.80 %  | 57.30 %  | 26.73  |

EM : Exact Match <br>
F1 : F1 score <br> 
Avg. Len(q) : The avg length of questions <br>
