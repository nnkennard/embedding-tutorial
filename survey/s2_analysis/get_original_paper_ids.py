import glob
import gzip
import json
import tqdm


PAPER_IDS = {
    # Distributed Representations of Words and Phrases and their Compositionality
    "w2v1": "87f40e6f3022adbc1f1905e3e506abad05a9964f",
    # Efficient Estimation of Word Representations in Vector Space
    "w2v2": "330da625c15427c6e42ccfa3b747fb29e5835bf0",
    # GloVe: Global Vectors for Word Representation
    "glove": "f37e1b62a767a307c046404ca96bc140b3e68cb5",
}


def main():

  for filename in tqdm.tqdm(glob.glob("s2_data/papers/*.gz")):
    with gzip.open(filename, 'r') as f:
      for line in tqdm.tqdm(f):
        obj = json.loads(line)
        if obj['url'] is None:
          print("Problem: ", line)
        elif obj["url"].split("/")[-1] in PAPER_IDS.values():
          print("Found: ", line)


if __name__ == "__main__":
  main()

