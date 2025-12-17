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

