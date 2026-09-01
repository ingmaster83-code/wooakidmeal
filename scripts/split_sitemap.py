#!/usr/bin/env python3
"""
split_sitemap.py - 단일 sitemap.xml(38.8MB, 31만 URL)을 sitemaps.org 프로토콜 기준
(파일당 URL 5만개 이하, 50MB 이하)에 맞게 여러 파일 + sitemap_index.xml로 분할.
Cloudflare Pages의 파일당 25MB 제한도 함께 회피.

사용법: python scripts/split_sitemap.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
SRC = DOCS / "sitemap.xml"
CHUNK_SIZE = 40000  # 여유있게 5만 미만
SITE_URL = "https://wooakidmeal.wooahouse.com"

def main():
    text = SRC.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(.*?)</loc>", text)
    print(f"총 URL {len(urls)}개")

    SRC.unlink()  # 기존 단일 파일 제거

    chunks = [urls[i:i+CHUNK_SIZE] for i in range(0, len(urls), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks, start=1):
        body = "\n".join(f"<url><loc>{u}</loc></url>" for u in chunk)
        xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'
        out = DOCS / f"sitemap-{idx}.xml"
        out.write_text(xml, encoding="utf-8")
        size_mb = out.stat().st_size / 1024 / 1024
        print(f"  sitemap-{idx}.xml: {len(chunk)}개 URL ({size_mb:.1f}MB)")

    index_body = "\n".join(
        f"<sitemap><loc>{SITE_URL}/sitemap-{i}.xml</loc></sitemap>"
        for i in range(1, len(chunks) + 1)
    )
    index_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{index_body}\n</sitemapindex>\n'
    (DOCS / "sitemap.xml").write_text(index_xml, encoding="utf-8")
    print(f"\nsitemap.xml (index, {len(chunks)}개 하위 sitemap 참조) 생성 완료")


if __name__ == "__main__":
    main()
