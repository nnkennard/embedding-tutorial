import collections
import csv
import glob
import gzip
import json
import pickle
import re
import tqdm

from get_citations import CORPUS_IDS


FIELDNAMES = "citer_id title year venue cited_paper intents".split()
PaperRow = collections.namedtuple("PaperRow", FIELDNAMES)

def main():
  with open('citation_info.pkl', 'rb') as f:
    citation_list_map = pickle.load(f)


  intent_map = collections.defaultdict(list)
  cited_map = collections.defaultdict(list)

  for cited_id, citers in citation_list_map.items():
    cited_name = CORPUS_IDS[cited_id]
    for citer in citers:
      citing_corpus_id = citer['citingcorpusid']
      if citer['intents'] is not None:
        intent_map[citing_corpus_id] += citer['intents']
      cited_map[citing_corpus_id].append(cited_name)

  citers = list(sorted(cited_map.keys()))
  print(citers[:10])
  with open("citers.txt", 'w') as f:
    f.write("\n".join(f'corpusid":{corpus_id},' for corpus_id in citers))

  # Run zgrep command

  rows = []
  with open('temp', 'r') as f:
    for line in tqdm.tqdm(f):
      _, json_str = line.split(":", 1)
      obj = json.loads(json_str)
      if obj['venue']:
        venue = obj['venue']
      elif obj['journal'] is not None and obj['journal']['name']:
        venue = obj['journal']['name']
      else:
        venue = ""
      corpus_id = str(obj['corpusid'])
      rows.append(PaperRow(corpus_id, obj['title'],
      obj['year'], venue,
      "|".join(sorted(set(cited_map[corpus_id]))),
      "|".join(sorted(set(intent_map[corpus_id])))))

  with open('embedding_citations.tsv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter='\t')
    for i in rows:
      print(i)
      writer.writerow(i._asdict())


if __name__ == "__main__":
  main()

