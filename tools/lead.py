"""The lead loop: media/lead.webp, cut from a recording of the projector screen.

    python tools/lead.py

The recipe (media/lead.json) names the recording and the segments to keep, in seconds:
a question being read, answers coming in, the reveal, the leaderboard, the podium.
Segments are joined with short dissolves. The recording is
not in this repository; UPDATING.md says how it was made (a local run of the app).
"""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    r = json.loads((ROOT / "media" / "lead.json").read_text(encoding="utf-8"))
    segs, fps, w, fade = r["segments"], r["fps"], r["width"], r["fade"]
    src = str(ROOT / r["src"])  # relative to the repository; yerel/ is gitignored
    parts = [
        f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps={fps},scale={w}:-2:flags=lanczos,format=yuv420p[s{i}]"
        for i, (a, b) in enumerate(segs)
    ]
    # chain the segments with dissolves
    last, offset = "s0", segs[0][1] - segs[0][0] - fade
    for i in range(1, len(segs)):
        out = f"x{i}"
        parts.append(f"[{last}][s{i}]xfade=transition=fade:duration={fade}:offset={offset:.3f}[{out}]")
        last = out
        offset += segs[i][1] - segs[i][0] - fade
    graph = ";".join(parts) + f";[{last}]null[out]"
    out = ROOT / "media" / "lead.webp"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", graph, "-map", "[out]",
         "-c:v", "libwebp_anim", "-loop", "0", "-quality", str(r["quality"]), "-compression_level", "6",
         "-an", str(out)],
        check=True,
    )
    print(out.relative_to(ROOT), f"{out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
