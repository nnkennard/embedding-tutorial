import collections
import glob
import numpy as np
import pickle
import re

Analogy = collections.namedtuple("Analogy", "a a_ b b_s")

def read_google_analogy_dataset(uncase=False):
  analogies = collections.defaultdict(list)
  with open(f'data/analogy-dataset.txt', 'r') as f:
    for line in f:
      if line.startswith(":"):
        _, analogy_category = line.strip().split()
      else:
        if uncase:
          line = line.lower()
        a, a_, b, b_ = line.strip().split()
        analogies[analogy_category].append(Analogy(a, a_, b, [b_]))
  return analogies



def read_bats_analogy_dataset():
  analogies = collections.defaultdict(list)
  for dirname in glob.glob(f'data/BATS_3.0/*'):
    if dirname.endswith('.json'):
      continue
    for filename in glob.glob(f'{dirname}/*'):
      relation_name, = re.findall('\[[^\[\]]*\]',filename)
      pairs = []
      with open(filename, 'r') as f:
        for line in f:
          x, x_s = line.strip().split()
          pairs.append((x, x_s.split("/")))
      for x_1, x_s_1 in pairs:
        for  x_2, x_s_2 in pairs:
          if x_1 == x_2:
            continue
          else:
            analogies[relation_name].append(Analogy(x_1, x_s_1[0], x_2, x_s_2))
  return analogies
            

def normalize(vector):
  if np.linalg.norm(vector) == 0.0:
    return vector
  else:
    return vector/np.linalg.norm(vector)

def preprocess_askscience(min_count=20):  
    with open('askscience_documents.pkl', 'rb') as f:
        docs = pickle.load(f)
    seen_docs = set()
    vocab_counter = collections.Counter()
    dedup_docs = {}
    for key, doc in docs.items():
        new_doc = tuple([tuple(sent) for sent in doc])
        if new_doc not in seen_docs:
            seen_docs.add(new_doc)
            dedup_docs[key] = doc
            vocab_counter.update(sum(doc, []))
    infreq_remove = set()
    for token, count in vocab_counter.items():
        if count < min_count:
            infreq_remove.add(token)
            
    final_docs = {}
    for key, doc in dedup_docs.items():
        final_docs[key] = [
            [token.lower() for token in sent if token not in infreq_remove]
            for sent in doc
        ]
    return final_docs
