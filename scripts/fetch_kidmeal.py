"""
fetch_kidmeal.py — 전국아동복지급식정보표준데이터 (아동급식카드 가맹점) 다운로드
data.go.kr download/standard.json 직접 다운로드 (API 키 불필요)
"""
import json
import time
from pathlib import Path
import requests

BASE = "https://www.data.go.kr/download/standard.json"
PUBLIC_DATA_PK = "15034530"
SVC_TABLE = "tn_pubr_public_chil_wlfare_mlsv_svc"

COLUMNS = [
    "MRHST_NM", "MRHST_CODE", "CTPRVN_NM", "SIGNGU_NM", "SIGNGU_CODE",
    "RDNMADR", "LNMADR", "LATITUDE", "LONGITUDE", "PHONE_NUMBER",
    "WEEKDAY_OPER_OPEN_HHMM", "WEEKDAY_OPER_COLSE_HHMM",
    "SAT_OPER_OPER_OPEN_HHMM", "SAT_OPER_CLOSE_HHMM",
    "HOLIDAY_OPER_OPEN_HHMM", "HOLIDAY_CLOSE_OPEN_HHMM",
    "DLVR_OPER_OPEN_HHMM", "DLVR_CLOSE_OPEN_HHMM",
    "INSTITUTION_NM", "INSTITUTION_PHONE_NUMBER", "REFERENCE_DATE",
]

OUT = Path(__file__).parent.parent / "_rawdata" / "kidmeal_raw.json"


def fetch_all():
    total = []
    page = 1
    while True:
        params = [("publicDataPk", PUBLIC_DATA_PK)] + [("colNmList", c) for c in COLUMNS] + [
            ("totalCount", "400000"), ("svcTableNm", SVC_TABLE),
            ("perPage", "10000"), ("page", str(page)),
        ]
        r = requests.get(BASE, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=90)
        data = r.json()
        if isinstance(data, dict) or not data:
            break
        total.extend(data)
        print(f"page {page}: {len(data)} (cumulative {len(total)})")
        if len(data) < 10000:
            break
        page += 1
        time.sleep(0.2)
    return total


def main():
    items = fetch_all()

    # 50% 안전장치: 기존 파일보다 절반 미만이면 저장 중단
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
            if len(items) < len(old) * 0.5:
                print(f"경고: 새 데이터({len(items)})가 기존({len(old)})의 50% 미만 — 저장 중단")
                return
        except Exception:
            pass

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    print(f"\n총 {len(items)}건 저장 → {OUT}")


if __name__ == "__main__":
    main()
