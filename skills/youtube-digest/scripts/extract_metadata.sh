#!/bin/bash
# YouTube 메타데이터 추출
# Usage: ./extract_metadata.sh <URL>

URL="$1"

if [ -z "$URL" ]; then
  echo "Usage: $0 <YouTube URL>"
  exit 1
fi

yt-dlp --dump-json --no-download "$URL"
