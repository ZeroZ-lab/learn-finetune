import argparse
from pathlib import Path

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from retrievers import Document, LocalTfidfRetriever


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", required=True, help="Plaintext file, one document per line")
    ap.add_argument("--index", required=True, help="Path to save local index (pickle)")
    args = ap.parse_args()

    docs = []
    with open(args.docs, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            text = line.strip()
            if not text:
                continue
            docs.append(Document(doc_id=f"doc-{i}", text=text, meta={"line": i}))

    retr = LocalTfidfRetriever()
    retr.ingest(docs)
    Path(args.index).parent.mkdir(parents=True, exist_ok=True)
    retr.save(args.index)
    print(f"indexed docs: {len(docs)} -> {args.index}")


if __name__ == "__main__":
    main()
