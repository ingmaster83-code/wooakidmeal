#!/usr/bin/env python3
"""
fix_ad_placeholder.py - 로컬 빌드시 JEKYLL_ENV=production을 안 줘서 전체 페이지에
박힌 광고 placeholder를 실제 AdSense ins 태그로 일괄 치환.
(모든 {% include ad.html %} 호출이 slot 파라미터 없이 기본값만 써서 문자열이 전부 동일함)

사용법: python scripts/fix_ad_placeholder.py
"""
import sys
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"

PLACEHOLDER = '<div class="ad-placeholder">📢 광고 영역 (배포 시 AdSense로 교체)</div>'
REAL_AD = (
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-6464921081676309" '
    'data-ad-slot="7080296704" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
)


def main():
    fixed = 0
    scanned = 0
    for f in DOCS.rglob("*.html"):
        scanned += 1
        text = f.read_text(encoding="utf-8")
        if PLACEHOLDER in text:
            text = text.replace(PLACEHOLDER, REAL_AD)
            f.write_text(text, encoding="utf-8")
            fixed += 1
        if scanned % 20000 == 0:
            print(f"  진행: {scanned}개 스캔, {fixed}개 수정", flush=True)

    print(f"\n완료: {scanned}개 파일 스캔, {fixed}개 파일에서 광고 placeholder 치환")


if __name__ == "__main__":
    main()
