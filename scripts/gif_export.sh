#!/usr/bin/env bash
set -euo pipefail
# Usage: ./gif_export.sh input.mp4 output.gif
# Target recipe: 896x504, 5 fps, 40 colors, under 10 MB.
if [[ $# -ne 2 ]]; then echo "Usage: $0 input.mp4 output.gif" >&2; exit 2; fi
input=$1; output=$2; palette=$(mktemp --suffix=.png); trap 'rm -f "$palette"' EXIT
ffmpeg -y -i "$input" -vf "fps=5,scale=896:504:flags=lanczos,palettegen=max_colors=40" "$palette"
ffmpeg -y -i "$input" -i "$palette" -lavfi "fps=5,scale=896:504:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2_4a" "$output"
size=$(du -m "$output" | cut -f1)
if (( size >= 10 )); then echo "Warning: GIF is ${size} MB; target is under 10 MB." >&2; fi
