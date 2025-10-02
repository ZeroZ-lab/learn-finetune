import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("app.main", str(BASE / "app" / "main.py"))
mod = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(mod)  # type: ignore
app = mod.app  # type: ignore


client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.text == "healthy"


def test_chat_streaming_done():
    with client.stream("GET", "/chat") as r:  # type: ignore
        chunks = []
        for chunk in r.iter_lines():
            if not chunk:
                continue
            data = chunk.decode("utf-8") if isinstance(chunk, (bytes, bytearray)) else chunk
            if data.startswith("data:"):
                chunks.append(data)
        assert any('"done": true' in x for x in chunks)
