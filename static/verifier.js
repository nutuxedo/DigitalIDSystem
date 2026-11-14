let scanner;
let scanInProgress = false;
let verificationInProgress = false;
const detailFields = [
    "id",
    "firstname",
    "lastname",
    "role",
    "bandname",
    "event",
    "expiry",
    "status"
];

async function fetchWithTimeout(url, options = {}, timeoutMs = 8000) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
        return await fetch(url, { ...options, signal: controller.signal });
    } finally {
        clearTimeout(timeout);
    }
}

async function checkSheetsStatus() {
    const status = document.getElementById("sheets-status");

    try {
        const response = await fetchWithTimeout("/status");
        const data = await response.json();
        status.textContent = data.connected
            ? "Google Sheets: connected"
            : "Google Sheets: unavailable";
        status.style.backgroundColor = data.connected ? "green" : "red";
    } catch (error) {
        status.textContent = "Google Sheets: unavailable";
        status.style.backgroundColor = "red";
    }
}

async function startScan() {
    if (scanInProgress) {
        return;
    }

    scanInProgress = true;
    const scanButton = document.getElementById("scan-button");
    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";
    scanner = new Html5Qrcode("reader");

    try {
        const cameras = await Html5Qrcode.getCameras();

        if (!cameras.length) {
            throw new Error("No camera found");
        }

        const camera =
            cameras.find(c => /back|rear|main|1x/i.test(c.label) &&
                              !/0[.]5x|ultra.?wide|wide/i.test(c.label))
            || cameras.find(c => /back|rear|environment/i.test(c.label))
            || cameras[0];

        const qrSize = Math.min(220, Math.max(140, window.innerWidth - 96));
        await scanner.start(
            camera.id,
            { fps: 10, qrbox: { width: qrSize, height: qrSize } },
            async decodedText => {
                if (!scanInProgress || verificationInProgress) {
                    return;
                }

                verificationInProgress = true;
                try {
                    await scanner.stop();
                } catch (error) {
                    console.error("Could not stop camera:", error);
                }

                try {
                    await verifyQr(decodedText);
                } finally {
                    verificationInProgress = false;
                    scanInProgress = false;
                    scanButton.disabled = false;
                    scanButton.textContent = "Scan QR";
                }
            },
            () => {}
        );
    } catch (error) {
        console.error("Camera error:", error);

        document.getElementById("result").textContent =
            "Camera error: " + String(error);
        scanInProgress = false;
        verificationInProgress = false;
        scanButton.disabled = false;
        scanButton.textContent = "Scan QR";
    }
}

async function verifyQr(decodedText) {
    const result = document.getElementById("result");
    result.textContent = "Checking...";
    result.style.color = "black";
    for (const field of detailFields) {
        document.getElementById(`detail-${field}`).textContent = "—";
    }

    try {
        const response = await fetchWithTimeout("/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ qr_data: decodedText })
        });
        const data = await response.json();
        result.textContent = data.message;
        const status = String(data.details?.status || "").toLowerCase();
        result.style.color = data.accepted
            ? "green"
            : status === "pending"
                ? "orange"
                : "red";

        if (data.details) {
            for (const field of detailFields) {
                const value = data.details[field];
                document.getElementById(`detail-${field}`).textContent =
                    value === undefined ? "—" : String(value);
            }
        }
    } catch (error) {
        result.textContent = "Could not check online ID data. Try again.";
        result.style.color = "red";
    }
}

checkSheetsStatus();
