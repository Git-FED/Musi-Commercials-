#!/usr/bin/env python3
"""Print duration, resolution, and file size for a video."""
import json, shutil, subprocess, sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 verify_video.py <video-file>")
    path = Path(sys.argv[1])
    if not path.is_file(): raise SystemExit(f"Missing video file: {path}")
    if not shutil.which("ffprobe"): raise SystemExit("ffprobe not found on PATH")
    cmd=["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",str(path)]
    try: data=json.loads(subprocess.check_output(cmd, text=True))
    except subprocess.CalledProcessError as e: raise SystemExit(f"Unreadable video: {path}") from e
    duration=float(data["format"]["duration"])
    video=next((s for s in data.get("streams",[]) if "width" in s), None)
    if not video: raise SystemExit("No video stream found")
    print(f"duration: {duration:.3f} seconds")
    print(f"resolution: {video['width']}x{video['height']}")
    print(f"size: {path.stat().st_size / 1024 / 1024:.2f} MB")
if __name__ == "__main__": main()
