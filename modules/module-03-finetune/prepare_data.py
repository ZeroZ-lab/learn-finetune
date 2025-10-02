import argparse
import json
from pathlib import Path


def valid(rec: dict, min_len: int, max_len: int) -> bool:
    text = "".join([str(rec.get(k, "")) for k in ("instruction", "input", "output")])
    n = len(text)
    return min_len <= n <= max_len


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--min-len", type=int, default=10)
    ap.add_argument("--max-len", type=int, default=2048)
    args = ap.parse_args()

    inp = Path(args.input)
    outp = Path(args.output)
    outp.parent.mkdir(parents=True, exist_ok=True)

    kept = 0
    with inp.open("r", encoding="utf-8") as f, outp.open("w", encoding="utf-8") as w:
        seen = set()
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            key = json.dumps(rec, ensure_ascii=False, sort_keys=True)
            if key in seen:
                continue
            if not valid(rec, args.min_len, args.max_len):
                continue
            w.write(json.dumps(rec, ensure_ascii=False) + "\n")
            seen.add(key)
            kept += 1
    print(f"kept records: {kept}")


if __name__ == "__main__":
    main()

