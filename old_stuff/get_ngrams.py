import collections
import json
from google_ngram_downloader import readline_google_store
import tqdm

def get_word_lists():
  vocab = set()
  with open('features.json', 'r') as f:
    obj = json.load(f)
    for dim_map in obj:
      vocab.update(dim_map['positives'])
      vocab.update(dim_map['negatives'])
  with open('categories.json', 'r') as f:
    obj = json.load(f)
    for cat_map in obj:
      vocab.update(cat_map['words'])

  return list(sorted(vocab))

def main():
  ngram_counter = collections.defaultdict(lambda: collections.defaultdict(
    lambda : collections.Counter()))

  words = get_word_lists()
  for fname, url, records in tqdm.tqdm(readline_google_store(ngram_len=5)):
    for j in tqdm.tqdm(records):
      l1, l2, w, r2, r1 = j.ngram.lower().split()
      if w not in words:
        continue
      else:
        for c_word in [l1, l2, r1, r2]:
          ngram_counter[j.year][w][c_word] += j.match_count

  with open('ngram_results.json', 'w') as f:
    json.dump(ngram_counter, f)


if __name__ == "__main__":
  main()

