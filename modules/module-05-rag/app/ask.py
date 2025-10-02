import argparse
from pathlib import Path

from modules.module-05-rag.retrievers import LocalTfidfRetriever
from modules.module-05-rag.rerankers import simple_rerank


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    retr = LocalTfidfRetriever.load(args.index)
    results = retr.search(args.query, top_k=args.top_k)
    # 填充文本用于重排演示（本地实现不保存原文，真实系统应保存 chunk 文本）
    cands = [(doc_id, score, meta, f"[placeholder content for {doc_id}]") for doc_id, score, meta in results]
    reranked = simple_rerank(args.query, cands, top_k=args.top_k)

    for doc_id, score, meta, text in reranked:
        print({"doc_id": doc_id, "score": round(score, 4), "meta": meta})


if __name__ == "__main__":
    main()

