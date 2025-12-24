from flask import (
    Blueprint,
    request,
    send_file,
    jsonify,
    after_this_request,
)
from pathlib import Path
import uuid

from backend.video.video_service import process_video
from backend.utils.temp_cleanup import cleanup_temp_dir


# -----------------------------
# Blueprint
# -----------------------------

video_bp = Blueprint(
    "video",
    __name__,
    url_prefix="/api/video-tools"
)

# -----------------------------
# Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMP_DIR = PROJECT_ROOT / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Limits
# -----------------------------

MAX_VIDEOS = 3


# =========================================================
# Process video route
# =========================================================

@video_bp.route("/process", methods=["POST"])
def process_video_route():

    videos = request.files.getlist("videos")
    music = request.files.get("music")

    if not videos:
        return jsonify({"error": "At least one video is required"}), 400

    if len(videos) > MAX_VIDEOS:
        return jsonify({"error": f"Maximum {MAX_VIDEOS} videos allowed"}), 400

    music_start = request.form.get("music_start", type=int, default=0)
    volume = request.form.get("volume", type=float, default=1.0)

    # -----------------------------
    # Create isolated work directory
    # -----------------------------

    work_dir = TEMP_DIR / f"video_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Guaranteed cleanup AFTER response
    # -----------------------------

    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    try:
        video_paths = []

        # -----------------------------
        # Save videos
        # -----------------------------

        for file in videos:
            suffix = Path(file.filename).suffix or ".mp4"
            path = work_dir / f"video_{uuid.uuid4().hex}{suffix}"
            file.save(path)
            video_paths.append(path)

        # -----------------------------
        # Save music (optional)
        # -----------------------------

        music_path = None
        if music:
            suffix = Path(music.filename).suffix or ".mp3"
            music_path = work_dir / f"music_{uuid.uuid4().hex}{suffix}"
            music.save(music_path)

        # -----------------------------
        # Output path
        # -----------------------------

        output_path = work_dir / "final_video.mp4"

        # -----------------------------
        # Process
        # -----------------------------

        process_video(
            video_paths=video_paths,
            music_path=music_path,
            output_path=output_path,
            music_start=music_start,
            volume=volume,
        )

        # -----------------------------
        # Send result
        # -----------------------------

        return send_file(
            output_path,
            as_attachment=True,
            download_name="video.mp4",
        )

    except Exception as e:
        cleanup_temp_dir(work_dir)  # safety net
        return jsonify({"error": str(e)}), 400

