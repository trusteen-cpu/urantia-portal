# -*- coding: utf-8 -*-
"""
make_updates.py — 저장소의 깃 기록을 읽어 updates.json 을 만듭니다.

홈페이지가 이 파일을 읽어, 최근에 바뀐 페이지에 자동으로 빨간 N 딱지를 붙입니다.
날짜를 손으로 적을 필요가 없습니다.

실행:
    python make_updates.py

저장소 안에서 실행하거나, 아래 REPO 경로를 그대로 두고 아무 데서나 실행해도 됩니다.
깃허브에 푸시하기 직전에 한 번 돌리시면 됩니다.
"""

import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = r"E:\OneDrive\문서\GitHub\urantia-portal"

SKIP_PREFIX = (".github/", ".git/")
SKIP_NAME = (".gitignore", "updates.json")


def main():
    repo = REPO if os.path.isdir(REPO) else os.getcwd()
    print(f"저장소: {repo}")

    try:
        out = subprocess.run(
            ["git", "log", "--name-only", "--date=short", "--pretty=format:%x01%cI"],
            cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except FileNotFoundError:
        print("[중단] 깃을 찾지 못했습니다. 깃허브 데스크탑이 설치된 PC에서 실행하세요.")
        input("\n엔터를 누르면 창이 닫힙니다.")
        return

    if out.returncode != 0:
        print("[중단] 깃 기록을 읽지 못했습니다.")
        print(out.stderr[:400])
        input("\n엔터를 누르면 창이 닫힙니다.")
        return

    paths = {}
    when = None
    for line in out.stdout.splitlines():
        if line.startswith("\x01"):
            when = line[1:].strip()
            continue
        f = line.strip().replace("\\", "/")
        if not f or not when:
            continue
        if f.startswith(SKIP_PREFIX) or os.path.basename(f) in SKIP_NAME:
            continue
        if f not in paths:          # 로그가 최신순이라 처음 만난 것이 마지막 변경
            paths[f] = when[:10]

    # 폴더도 함께 기록 — 폴더 안에서 가장 최근에 바뀐 날짜
    dirs = {}
    for f, d in paths.items():
        parts = f.split("/")
        for i in range(1, len(parts)):
            key = "/".join(parts[:i])
            if key not in dirs or d > dirs[key]:
                dirs[key] = d
    for k, v in dirs.items():
        paths.setdefault(k, v)
        if v > paths[k]:
            paths[k] = v

    data = {"paths": paths}
    out_path = os.path.join(repo, "updates.json")
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=0, sort_keys=True)

    recent = sorted(((d, f) for f, d in paths.items() if "/" in f or f.endswith(".html")),
                    reverse=True)[:10]
    print(f"\n{len(paths)}개 경로 기록 → {out_path}\n")
    print("최근에 바뀐 것:")
    for d, f in recent:
        print(f"   {d}  {f}")
    input("\n엔터를 누르면 창이 닫힙니다.")


if __name__ == "__main__":
    main()
