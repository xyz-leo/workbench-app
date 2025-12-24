from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips


def merge_videos(
    input_paths: list[Path],
    output_path: Path,
) -> None:
    if len(input_paths) < 2:
        raise ValueError("At least two videos are required")

    clips = [VideoFileClip(str(p)) for p in input_paths]

    try:
        final = concatenate_videoclips(clips)
        final.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
        )
    finally:
        for c in clips:
            c.close()

