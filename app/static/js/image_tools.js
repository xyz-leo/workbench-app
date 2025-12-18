document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("image-files");
    const presetRadios = document.querySelectorAll("input[name='resize-preset']");
    const widthInput = document.getElementById("custom-width");
    const heightInput = document.getElementById("custom-height");
    const submitBtn = document.getElementById("resize-image");

    submitBtn.addEventListener("click", async () => {
        const files = fileInput.files;
        if (!files.length) {
            alert("Select at least one image.");
            return;
        }

        if (files.length > 10) {
            alert("Maximum of 10 images.");
            return;
        }

        const selectedPreset = [...presetRadios].find(r => r.checked);
        if (!selectedPreset) {
            alert("Select a preset or custom size.");
            return;
        }

        const formData = new FormData();

        for (const file of files) {
            formData.append("files", file);
        }

        if (selectedPreset.value === "custom") {
            const width = widthInput.value;
            const height = heightInput.value;

            if (!width || !height) {
                alert("Custom size requires width and height.");
                return;
            }

            formData.append("width", width);
            formData.append("height", height);
        } else {
            formData.append("preset", selectedPreset.value);
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "Processing...";

        try {
            const response = await fetch("/api/image-tools/resize", {
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
            a.download = "resized_images.zip";
            a.click();

            URL.revokeObjectURL(url);
        } catch (err) {
            alert(err.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Resize Images";
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("image-files");
    const filterCheckboxes = document.querySelectorAll(
        "input[name='filter']"
    );
    const intensityInput = document.getElementById("filter-intensity");
    const applyBtn = document.getElementById("apply-filters");

    if (!applyBtn) return;

    applyBtn.addEventListener("click", async () => {
        const files = fileInput.files;

        if (!files.length) {
            alert("Select at least one image.");
            return;
        }

        if (files.length > 10) {
            alert("Maximum of 10 images.");
            return;
        }

        // Collect selected filters
        const selectedFilters = [...filterCheckboxes]
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (!selectedFilters.length) {
            alert("Select at least one filter.");
            return;
        }

        const intensity = intensityInput.value;

        const formData = new FormData();

        for (const file of files) {
            formData.append("files", file);
        }

        // Multiple filters → repeated field
        selectedFilters.forEach(filter => {
            formData.append("filters", filter);
        });

        formData.append("intensity", intensity);

        applyBtn.disabled = true;
        applyBtn.textContent = "Processing...";

        try {
            const response = await fetch(
                "/api/image-tools/filters",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {
                throw new Error("Processing failed.");
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "filtered_images.zip";
            document.body.appendChild(a);
            a.click();
            a.remove();

            URL.revokeObjectURL(url);

        } catch (err) {
            alert(err.message);
        } finally {
            applyBtn.disabled = false;
            applyBtn.textContent = "Apply Filters";
        }
    });
});

