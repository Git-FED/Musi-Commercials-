#!/usr/bin/env python3
"""Extract frames at 10%, 50%, 70%, 80%, and 95% of a video's duration."""
import shutil, subprocess, sys
from pathlib import Path

def main():
    if len(sys.argv) not in (2,3): raise SystemExit("Usage: python3 frame_check.py <video-file> [duration-seconds]")
    video=Path(sys.argv[1])
    if not video.is_file(): raise SystemExit(f"Missing video file: {video}")
    if not shutil.which("ffmpeg"): raise SystemExit("ffmpeg not found on PATH")
    duration=float(sys.argv[2]) if len(sys.argv)==3 else None
    if duration is None:
        probe=["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(video)]
        duration=float(subprocess.check_output(probe,text=True).strip())
    for pct,label in [(0.10,"1s"),(0.50,"5s"),(0.70,"7s"),(0.80,"8s"),(0.95,"9.5s")]:
        timestamp=min(duration-0.001, duration*pct)
        out=video.with_name(f"{video.stem}-{label}.png")
        subprocess.run(["ffmpeg","-y","-ss",f"{timestamp:.3f}","-i",str(video),"-frames:v","1",str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print(out)
if __name__ == "__main__": main()
