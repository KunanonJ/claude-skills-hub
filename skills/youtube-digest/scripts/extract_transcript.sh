#!/bin/bash
# YouTube 자막 추출
# Usage: ./extract_transcript.sh <URL> [output_dir]

URL="$1"
OUTPUT_DIR="${2:-.}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <YouTube URL> [output_dir]"
  exit 1
fi

# JSON3 형식으로 자막 추출 (한국어 > 영어 우선)
yt-dlp --write-auto-sub --sub-lang "ko,en" --skip-download --convert-subs json3 \
  -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$URL"
