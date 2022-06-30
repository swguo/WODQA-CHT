# WODQA-CHT
WODQA-CHT : A Dataset and Baselines for Traditional Chinese Wikipedia Open Domain QA

# Inverted Index for wiki Corpus
python -m pyserini.index.lucene \\ <br>
  --collection JsonCollection \\
  
  --input corpus \\
  
  --language zh \\
  
  --index Index/Wiki_Chinese \\
  
  --generator DefaultLuceneDocumentGenerator \\
  
  --threads 1 \\
  
  --storePositions --storeDocvectors --storeRaw
