import argparse
import collections
import glob
import json
import tqdm

from google_ngram_downloader import readline_google_store

parser = argparse.ArgumentParser(
    description="Get some ngrams from Google n-grams")
parser.add_argument("-o",
                    "--output_dir",
                    default="ngrams/",
                    type=str,
                    help="directory for output files")
parser.add_argument(
    "-w",
    "--word_list_dir",
    default="./",
    type=str,
    help="location of features.json and categories.json",
)
parser.add_argument(
    "-p",
    "--identifier_prefix",
    type=str,
    help="prefix of identifier from ngram filenames; something from [a-z0-9_].",
)


def get_word_lists(word_list_dir):
  vocab = set()
  with open(f"{word_list_dir}/features.json", "r") as f:
    obj = json.load(f)
    for dim_map in obj:
      vocab.update(dim_map["positives"])
      vocab.update(dim_map["negatives"])
  with open(f"{word_list_dir}/categories.json", "r") as f:
    obj = json.load(f)
    for cat_map in obj:
      vocab.update(cat_map["words"])

  return list(sorted(vocab))


def main():

  args = parser.parse_args()
  words = get_word_lists(args.word_list_dir)

  for fname, url, records in tqdm.tqdm(readline_google_store(ngram_len=5)):
    identifier = fname.split(".")[0].split("-")[-1]
    if not identifier.startswith(args.identifier_prefix):
      continue
    else:
      # Check if the file is already created
      current_files = [
          x.split("/")[-1] for x in glob.glob(f"{args.output_dir}/*")
      ]
      if (f"ngram_results-{identifier}.json" in current_files or
          f"ngram_results-{identifier}.json.gz") in current_files:
        print(f"Skipping {identifier}")
        continue

      ngram_counter = collections.defaultdict(
          lambda: collections.defaultdict(lambda: collections.Counter()))
      for j in tqdm.tqdm(records):
        l1, l2, w, r2, r1 = j.ngram.lower().split()
        if w not in words:
          continue
        else:
          for c_word in [l1, l2, r1, r2]:
            ngram_counter[j.year][w][c_word] += j.match_count

      with open(f"{args.output_dir}/ngram_results-{identifier}.json", "w") as f:
        json.dump(ngram_counter, f)


if __name__ == "__main__":
  main()
