#!/usr/bin/env bash
# publish.sh — 오늘치 묵상을 올립니다.
#   1) mp3를 인터넷 아카이브로  2) 페이지를 깃허브로
#   사용법:  ./publish.sh
set -e
cd "$(dirname "$0")"

ITEM="${ARCHIVE_ITEM:-urantia-devotion-kr}"
TODAY="$(date +%Y%m%d)"

# 1) mp3 → 인터넷 아카이브   (설치: pip install internetarchive && ia configure)
if command -v ia >/dev/null 2>&1; then
  echo "▸ 아카이브 업로드: $ITEM / ${TODAY}_*.mp3"
  ia upload "$ITEM" site/audio/${TODAY}_*.mp3 --retries 3
else
  echo "▸ ia 명령이 없습니다. archive.org에서 직접 올리십시오:"
  ls -1 site/audio/${TODAY}_*.mp3
fi

# 2) 페이지 → 깃허브 (mp3는 site/.gitignore 로 제외됨)
cd site
git add -A
git commit -m "묵상 $(date +%Y-%m-%d)" || { echo "바뀐 내용이 없습니다."; exit 0; }
git push
echo "▸ 올렸습니다. 잠시 뒤 페이지에 반영됩니다."
