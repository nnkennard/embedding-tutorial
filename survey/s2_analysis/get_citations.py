import collections
import glob
import gzip
import json
import pickle
import tqdm


CORPUS_IDS = {
    # Distributed Representations of Words and Phrases and their Compositionality
    '16447573': "w2v1",
    # Efficient Estimation of Word Representations in Vector Space
    '5959482': "w2v2",
    # GloVe: Global Vectors for Word Representation
    '1957433': 'glove',
}


def main():

  citers = collections.defaultdict(list)
  for filename in tqdm.tqdm(glob.glob("s2_data/citations/*.gz")):
    with gzip.open(filename, 'r') as f:
      for line in tqdm.tqdm(f):
        obj = json.loads(line)
        if obj['citedcorpusid'] in CORPUS_IDS:
          citers[obj["citedcorpusid"]].append(obj)
  with open('citation_info.pkl', 'wb') as f:
    pickle.dump(citers, f)


if __name__ == "__main__":
  main()

