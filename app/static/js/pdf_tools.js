// Merge PDF
document.getElementById("merge-pdf").addEventListener("click", async () => {
    const input = document.getElementById("pdf-files");
    if (!input.files.length) {
        alert("Please select at least two PDF files.");
        return;
    }

    if (input.files.length < 2) {
        alert("Select at least two PDFs to merge.");
        return;
    }

    const formData = new FormData();
    for (const file of input.files) {
        formData.append("pdfs", file);
    }

    try {
        const response = await fetch("/pdf-tools/merge", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            alert(data.error || "Error merging PDFs");
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "merged.pdf";
        a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});


// Split PDF
const splitButton = document.getElementById("split-pdf");
const splitInput = document.getElementById("pdf-files");

splitButton.addEventListener("click", async () => {
    if (!splitInput.files.length) {
        alert("Select a PDF to split.");
        return;
    }

    if (splitInput.files.length !== 1) {
        alert("Select exactly one PDF to split.");
        return;
    }

    const formData = new FormData();
    formData.append("pdf", splitInput.files[0]);

    try {
        const response = await fetch("/pdf-tools/split", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            alert(data.error || "Error splitting PDF");
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "pages.zip";
        a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
});


// Compress PDF
document.getElementById("compress-pdf").addEventListener("click", async () => {
    const fileInput = document.getElementById("pdf-files");
    if (!fileInput.files.length) return alert("Select a PDF file to compress");

    if (fileInput.files.length > 1) return alert("Please select only one PDF to compress");

    const qualityInput = document.getElementById("pdf-quality");
    let quality = parseInt(qualityInput.value);
    if (isNaN(quality) || quality < 5 || quality > 100) {
        quality = 20; // fallback default
    }

    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);
    formData.append("quality", quality); // pass quality to backend

    const response = await fetch("/pdf-tools/compress", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        return alert(error.error || "Failed to compress PDF");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileInput.files[0].name.replace(/\.pdf$/i, "_compressed.pdf");
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
});
