import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

fixture = Path(__file__).resolve().parents[1] / "data" / "api_response.json"

def load_payload(url=None):
    if url is None:
        return json.loads(fixture.read_text(encoding="utf-8"))
    if urlparse(url).scheme != "https":
        raise ValueError("신뢰할 수 있는 HTTPS URL만 사용하세요.")
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "DataProcessing-Lesson/1.0"})
    with urlopen(request, timeout=10) as response:
        if "json" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("JSON 응답이 아닙니다.")
        content = response.read(1_000_001)
    if len(content) > 1_000_000:
        raise ValueError("응답 크기 제한(1MB) 초과")
    return json.loads(content.decode("utf-8"))

if __name__ == "__main__":
    payload = load_payload(sys.argv[1] if len(sys.argv) > 1 else None)
    print("Payload type:", type(payload).__name__)
    if isinstance(payload, dict) and "data" in payload:
        print("Records:", len(payload["data"]))
