import collections
import csv
from semanticscholar import SemanticScholar

PAPER_IDS = {
    # Distributed Representations of Words and Phrases and their Compositionality
    "w2v1": "87f40e6f3022adbc1f1905e3e506abad05a9964f",
    # Efficient Estimation of Word Representations in Vector Space
    "w2v2": "330da625c15427c6e42ccfa3b747fb29e5835bf0",
    # GloVe: Global Vectors for Word Representation
    "glove": "f37e1b62a767a307c046404ca96bc140b3e68cb5",
}

FIELDS = "paperId title venue year".split()


def main():
  sch = SemanticScholar(timeout=5)

  paper_map = {}
  reference_counter = collections.defaultdict(list)
  venues = collections.Counter()

  for paper_name, paper_id in PAPER_IDS.items():
    paper = sch.paper(paper_id)
    print(paper["title"])
    for c in paper["citations"]:
      reference_counter[c["paperId"]].append(paper_name)
      if c["paperId"] in paper_map:
        continue
      paper_map[c["paperId"]] = c
      venues[c["venue"]] += 1
    print(len(paper_map))

  with open("venue_list.tsv", "w") as f:
    f.write("Venue\tCount")
    for venue, count in venues.most_common():
      f.write("".join([venue, "\t", str(count), "\n"]))

  with open("citation_list.tsv", "w") as f:
    writer = csv.DictWriter(f,
                            fieldnames=FIELDS + ["references"],
                            delimiter="\t")
    writer.writeheader()
    for _, citing_paper in paper_map.items():
      row = {k: citing_paper[k] for k in FIELDS}
      row["references"] = ", ".join(reference_counter[citing_paper["paperId"]])
      writer.writerow(row)


if __name__ == "__main__":
  main()
