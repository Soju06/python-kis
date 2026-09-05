#!/usr/bin/env bash
# sync_tokens_from_server.example.sh — 서버가 발급한 KIS 토큰을 로컬로 복사
#
# 설치:
#   cp scripts/sync_tokens_from_server.example.sh scripts/sync_tokens_from_server.sh
#   $EDITOR scripts/sync_tokens_from_server.sh   # REMOTE_TOKEN_DIR 과 TOKEN_MAP 을 채운다
#
# 목적: **토큰 발급 주체는 서버**다. 로컬이 같은 앱키로 다시 발급하면 운영
#   봇 토큰과 회전이 충돌한다 (KIS 토큰은 6h 재사용 · 24h 유효).
#   서버 파일을 `configs/token/<앱이름>.json` 으로 가져와 재발급을 피한다.
#
# 방향: **서버 → 로컬 단방향.** 역방향 금지(로컬 발급이 서버 토큰을 무효화한다).
# 보안: SSH 암호화 전송 + 로컬 0700/0600. `configs/token/` 은 gitignore.
#       ⚠️ 이 스크립트는 **토큰 값을 출력하지 않는다**(파일명·개수만).
# 실행: 수동. 만료되면 다시 돌린다 — cron 자동화 비권장.
#
# 채워진 `scripts/sync_tokens_from_server.sh` 는 gitignore 한다. 이 예제만 추적한다.
#
# 사용:
#   bash scripts/sync_tokens_from_server.sh
#   bash scripts/sync_tokens_from_server.sh --dry-run
#   VMKIS_TOKEN_SRC_HOST=other-host bash scripts/sync_tokens_from_server.sh
set -euo pipefail

REMOTE="${VMKIS_TOKEN_SRC_HOST:-stock-bot}"
# 서버의 토큰 디렉터리. 채워진 스크립트에서만 실제 경로를 적는다.
REMOTE_TOKEN_DIR="${VMKIS_TOKEN_SRC_DIR:-/path/on/server/to/token}"

# 원격 파일명=로컬 파일명 (configs/token/ 아래). 이 목록이 개인 서버 정보다.
# 예: "kis_token_example_paper.json=app_paper1.json"
TOKEN_MAP=(
  # "kis_token_example_paper.json=app_paper1.json"
  # "kis_token_example_live.json=app_live1.json"
)

DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    -*) echo "알 수 없는 옵션: $1" >&2; exit 2 ;;
    *) REMOTE="$1"; shift ;;
  esac
done

if [[ "$REMOTE_TOKEN_DIR" == "/path/on/server/to/token" ]]; then
  echo "REMOTE_TOKEN_DIR 을 채우세요. 예제를 복사한 뒤 서버 경로를 적습니다." >&2
  echo "  cp scripts/sync_tokens_from_server.example.sh scripts/sync_tokens_from_server.sh" >&2
  exit 2
fi

mapped=()
for entry in "${TOKEN_MAP[@]+"${TOKEN_MAP[@]}"}"; do
  [[ -z "$entry" || "$entry" == \#* ]] && continue
  mapped+=("$entry")
done

if [[ ${#mapped[@]} -eq 0 ]]; then
  echo "TOKEN_MAP 이 비어 있습니다. 원격 파일=로컬 파일을 적으세요." >&2
  exit 2
fi

LOCAL_REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_TOKEN_DIR="$LOCAL_REPO/configs/token"

echo "[sync] $REMOTE:$REMOTE_TOKEN_DIR → $LOCAL_TOKEN_DIR"

if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "$REMOTE" true 2>/dev/null; then
  echo "  ✗ SSH 연결 실패: $REMOTE  (~/.ssh/config · 보안그룹 확인)" >&2
  exit 1
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "  (dry-run — 복사하지 않음)"
  for entry in "${mapped[@]}"; do
    echo "  - ${entry%%=*} → ${entry#*=}"
  done
  exit 0
fi

install -d -m 700 "$LOCAL_TOKEN_DIR"

copied=0
for entry in "${mapped[@]}"; do
  if [[ "$entry" != *"="* ]]; then
    echo "  ✗ TOKEN_MAP 항목이 원격=로컬 형식이 아닙니다: $entry" >&2
    exit 2
  fi
  remote_name="${entry%%=*}"
  local_name="${entry#*=}"
  if [[ -z "$remote_name" || -z "$local_name" ]]; then
    echo "  ✗ TOKEN_MAP 항목이 비어 있습니다: $entry" >&2
    exit 2
  fi
  dest="$LOCAL_TOKEN_DIR/$local_name"
  if scp -q "$REMOTE:$REMOTE_TOKEN_DIR/$remote_name" "$dest"; then
    chmod 600 "$dest"
    echo "  ✓ $remote_name → $local_name"
    copied=$((copied + 1))
  else
    echo "  ✗ 복사 실패: $remote_name" >&2
    exit 1
  fi
done

echo "[sync] 완료 — ${copied}개. 로컬에서 같은 앱키로 재발급하지 마세요."
echo "       ⚠️ 역방향(로컬 → 서버) 동기화 금지 — 서버 토큰이 무효화된다."
