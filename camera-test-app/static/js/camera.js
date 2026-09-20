const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const statusEl = document.getElementById("status");
const switchBtn = document.getElementById("switchBtn");
const captureBtn = document.getElementById("captureBtn");
const retakeBtn = document.getElementById("retakeBtn");
const preview = document.getElementById("preview");
const previewImg = document.getElementById("previewImg");

let currentStream = null;
let facingMode = "environment"; // rear camera by default on mobile

async function startCamera() {
    stopCamera();
    setStatus("Requesting camera access...");

    try {
        currentStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode },
            audio: false,
        });
        video.srcObject = currentStream;
        setStatus("");
    } catch (err) {
        setStatus(`Camera error: ${err.message}`);
    }
}

function stopCamera() {
    if (currentStream) {
        currentStream.getTracks().forEach((track) => track.stop());
        currentStream = null;
    }
}

function setStatus(message) {
    statusEl.textContent = message;
}

switchBtn.addEventListener("click", () => {
    facingMode = facingMode === "environment" ? "user" : "environment";
    startCamera();
});

captureBtn.addEventListener("click", async () => {
    if (!currentStream) {
        setStatus("Camera is not active.");
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.9);

    previewImg.src = dataUrl;
    preview.hidden = false;
    setStatus("Uploading photo...");

    try {
        const res = await fetch("/capture", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: dataUrl }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Upload failed");
        setStatus(`Saved as ${data.filename}`);
    } catch (err) {
        setStatus(`Upload error: ${err.message}`);
    }
});

retakeBtn.addEventListener("click", () => {
    preview.hidden = true;
    setStatus("");
});

if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    setStatus("This browser does not support camera access.");
} else {
    startCamera();
}
