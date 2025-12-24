from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip


def add_music(
    video_path: Path,
    music_path: Path,
    output_path: Path,
    *,
    music_start: int = 0,
    volume: float = 1.0,
) -> None:

    if music_start < 0:
        raise ValueError("music_start must be >= 0")

    with VideoFileClip(str(video_path)) as video:
        audio = AudioFileClip(str(music_path)).subclip(
            music_start,
            music_start + video.duration,
        )

        audio = audio.volumex(volume)
        final = video.set_audio(audio)

        final.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
        )

