#!/usr/bin/env python3
"""
split_search_index.py - search_index.json(27.9MB)을 Cloudflare Pages 25MB 파일당 제한
회피를 위해 여러 조각(search_index-1.json, search_index-2.json, ...)으로 분할하고
manifest(search_index-manifest.json)에 조각 목록을 기록.

사용법: python scripts/split_search_index.py
"""
import json
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
SRC = DOCS / "search_index.json"
CHUNK_COUNT = 6  # 27.9MB / 6 ≈ 4.7MB per file, 25MB 제한에 여유있게

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    print(f"총 레코드 {len(data)}개")

    n = len(data)
    chunk_size = (n + CHUNK_COUNT - 1) // CHUNK_COUNT
    chunks = [data[i:i+chunk_size] for i in range(0, n, chunk_size)]

    SRC.unlink()

    names = []
    for idx, chunk in enumerate(chunks, start=1):
        name = f"search_index-{idx}.json"
        out = DOCS / name
        out.write_text(json.dumps(chunk, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        size_mb = out.stat().st_size / 1024 / 1024
        print(f"  {name}: {len(chunk)}개 ({size_mb:.1f}MB)")
        names.append(name)

    (DOCS / "search_index-manifest.json").write_text(
        json.dumps(names, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nsearch_index-manifest.json 생성 완료 ({len(names)}개 조각)")


if __name__ == "__main__":
    main()
