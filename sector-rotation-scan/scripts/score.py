#!/usr/bin/env python3
"""4단계 가중 점수 계산기.

입력 JSON (파일 경로 또는 stdin):
  [{"sector": "전력망 장비", "펀더멘털 변곡": 4, "미반영도": 3, "촉매 가시성": 5,
    "자본 흐름": 4, "구조성": 5, "투자 가능성": 4}, ...]

출력: 가중 점수 내림차순 Markdown 표 (부록 '점수 계산표'에 그대로 붙여 넣는다).
"""
import json
import sys

WEIGHTS = {
    "펀더멘털 변곡": 0.25,
    "미반영도": 0.20,
    "촉매 가시성": 0.20,
    "자본 흐름": 0.15,
    "구조성": 0.10,
    "투자 가능성": 0.10,
}


def main():
    src = open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin
    rows = json.load(src)

    results = []
    for row in rows:
        missing = [k for k in WEIGHTS if k not in row]
        if missing:
            sys.exit(f"{row.get('sector', '?')}: 누락된 기준 {missing}")
        bad = [k for k in WEIGHTS if not 1 <= row[k] <= 5]
        if bad:
            sys.exit(f"{row['sector']}: 1~5 범위를 벗어난 점수 {bad}")
        total = sum(row[k] * w for k, w in WEIGHTS.items())
        results.append((row["sector"], row, round(total, 2)))

    results.sort(key=lambda r: r[2], reverse=True)

    header = ["순위", "섹터"] + [f"{k} ({int(w * 100)}%)" for k, w in WEIGHTS.items()] + ["가중 합계"]
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for i, (sector, row, total) in enumerate(results, 1):
        cells = [str(i), sector] + [str(row[k]) for k in WEIGHTS] + [f"{total:.2f}"]
        print("| " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
