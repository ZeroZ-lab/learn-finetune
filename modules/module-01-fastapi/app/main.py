import os
import json
import time
from typing import Dict, Generator, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse, StreamingResponse

try:
    from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
except Exception:  # pragma: no cover - 允许无 prometheus 依赖运行
    Counter = None  # type: ignore
    Summary = None  # type: ignore
    generate_latest = None  # type: ignore
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"  # type: ignore


app = FastAPI(title="Module 01 - FastAPI SSE Demo")

# 简易指标
if Counter and Summary:
    REQ_TOTAL = Counter("app_requests_total", "Total HTTP requests")
    CHAT_TOKENS = Counter("chat_tokens_total", "Total tokens streamed")
    REQ_LATENCY = Summary("app_request_latency_seconds", "Request latency")
else:  # 回退占位
    REQ_TOTAL = CHAT_TOKENS = REQ_LATENCY = None

# 简易限流（每 IP 每 60s 最多 10 次）
RATE_LIMIT_WINDOW = 60.0
RATE_LIMIT_MAX = 10
_ip_hits: Dict[str, list[float]] = {}


def _check_api_key(x_api_key: Optional[str]) -> None:
    expected = os.getenv("API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")


def _rate_limit(ip: str) -> None:
    now = time.time()
    hits = _ip_hits.setdefault(ip, [])
    # 清理窗口外记录
    _ip_hits[ip] = [t for t in hits if now - t <= RATE_LIMIT_WINDOW]
    if len(_ip_hits[ip]) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    _ip_hits[ip].append(now)


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def token_stream(prompt: str = "你好") -> Generator[bytes, None, None]:
    tokens = list(prompt) + ["，", "世", "界", "！"]
    for i, tok in enumerate(tokens):
        payload = {"id": i, "content": tok, "done": False}
        if CHAT_TOKENS:
            CHAT_TOKENS.inc()
        yield _sse(payload).encode("utf-8")
        time.sleep(0.1)
    yield _sse({"id": len(tokens), "content": "", "done": True}).encode("utf-8")


@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    return "OK"


@app.get("/health", response_class=PlainTextResponse)
def health(x_api_key: Optional[str] = Header(default=None), request: Request = None):  # type: ignore
    if REQ_TOTAL:
        REQ_TOTAL.inc()
    _check_api_key(x_api_key)
    _rate_limit(request.client.host if request and request.client else "unknown")  # type: ignore
    return "healthy"


@app.get("/chat")
def chat(
    prompt: str = "你好，SSE",
    x_api_key: Optional[str] = Header(default=None),
    request: Request = None,  # type: ignore
):
    _check_api_key(x_api_key)
    _rate_limit(request.client.host if request and request.client else "unknown")  # type: ignore

    def _gen():
        start = time.time()
        try:
            yield from token_stream(prompt)
        finally:
            if REQ_TOTAL:
                REQ_TOTAL.inc()
            if REQ_LATENCY:
                REQ_LATENCY.observe(time.time() - start)

    return StreamingResponse(_gen(), media_type="text/event-stream")


@app.get("/metrics")
def metrics():
    if not generate_latest:
        return PlainTextResponse("prometheus_client not installed", status_code=501)
    data = generate_latest()  # type: ignore
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)  # type: ignore


if __name__ == "__main__":
    # 便于本地启动：python app/main.py
    import uvicorn  # type: ignore

    uvicorn.run(app, host="0.0.0.0", port=8000)

