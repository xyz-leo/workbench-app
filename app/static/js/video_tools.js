document.addEventListener("DOMContentLoaded", () => {
    const videoInput = document.getElementById("video-files");
    const musicInput = document.getElementById("music-file");
    const musicStartInput = document.getElementById("music-start");
    const volumeInput = document.getElementById("music-volume");
    const processBtn = document.getElementById("process-video");

    processBtn.addEventListener("click", async () => {

        // -----------------------------
        // Validate videos
        // -----------------------------
        const videos = Array.from(videoInput.files);

        if (!videos.length) {
            alert("Select at least one video.");
            return;
        }

        if (videos.length > 3) {
            alert("Maximum of 3 videos.");
            return;
        }

        // order videos by filename
        videos.sort((a, b) => a.name.localeCompare(b.name));

        // -----------------------------
        // Build FormData
        // -----------------------------
        const formData = new FormData();

        for (const video of videos) {
            formData.append("videos", video);
        }

        // -----------------------------
        // Optional music
        // -----------------------------
        if (musicInput.files.length) {
            formData.append("music", musicInput.files[0]);

            const musicStart = musicStartInput.value.trim();
            const volume = volumeInput.value.trim();

            if (musicStart !== "") {
                formData.append("music_start", musicStart);
            }

            if (volume !== "") {
                formData.append("volume", volume);
            }
        }

        // -----------------------------
        // UI feedback
        // -----------------------------
        processBtn.disabled = true;
        processBtn.textContent = "Processing...";

        try {
            const response = await fetch("/api/video-tools/process", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Processing failed.");
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "video.mp4";
            document.body.appendChild(a);
            a.click();
            a.remove();

            URL.revokeObjectURL(url);

        } catch (err) {
            alert(err.message);
        } finally {
            processBtn.disabled = false;
            processBtn.textContent = "Process Video";
        }
    });
});

