from pathlib import Path
from backend.video.merge_service import merge_videos
from backend.video.music_service import add_music


def process_video(
    *,
    video_paths: list[Path],
    music_path: Path | None,
    output_path: Path,
    music_start: int = 0,
    volume: float = 1.0,
) -> None:

    temp_video = output_path.with_name("temp_video.mp4")

    # 1️⃣ Merge se necessário
    if len(video_paths) > 1:
        merge_videos(video_paths, temp_video)
        base_video = temp_video
    else:
        base_video = video_paths[0]

    # 2️⃣ Add music se existir
    if music_path:
        add_music(
            video_path=base_video,
            music_path=music_path,
            output_path=output_path,
            music_start=music_start,
            volume=volume,
        )
    else:
        # sem música, só move/copia
        base_video.rename(output_path)

