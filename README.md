# WODQA-CHT
WODQA-CHT : A Dataset and Baselines for Traditional Chinese Wikipedia Open Domain QA

# setup
pip install -q -r requirement.txt

# Inverted Index for wiki Corpus
python -m pyserini.index.lucene \\ <br>
  --collection JsonCollection \\  <br>
  --input corpus \\  <br>
  --language zh \\  <br>
  --index Index/Wiki_Chinese \\  <br>
  --generator DefaultLuceneDocumentGenerator \\  <br>
  --threads 1 \\  <br>
  --storePositions --storeDocvectors --storeRaw
  
  
 # Running
 
 ## naive qg without filter
 python main.py -t naive
 
 ## Entity pass filter-1
 python main.py -t f1
 
 ## Question pass filter-2
 python main.py -t f2
  
 ## full filter passed
 python main.py -t all
 
 
 
 
