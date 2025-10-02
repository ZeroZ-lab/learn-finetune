import argparse


def monthly_token_cost(
    req_per_day: int,
    avg_tokens: int,
    price_per_1k: float,
    days: int = 30,
) -> float:
    tokens_month = req_per_day * avg_tokens * days
    return (tokens_month / 1000.0) * price_per_1k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--req-per-day", type=int, required=True)
    ap.add_argument("--avg-tokens", type=int, required=True)
    ap.add_argument("--price-per-1k", type=float, required=True, help="单位：USD/1K tokens")
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()

    cost = monthly_token_cost(args.req_per_day, args.avg_tokens, args.price_per_1k, args.days)
    print({
        "req_per_day": args.req_per_day,
        "avg_tokens": args.avg_tokens,
        "price_per_1k": args.price_per_1k,
        "days": args.days,
        "monthly_cost": round(cost, 4),
    })


if __name__ == "__main__":
    main()

