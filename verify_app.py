# Flask web app for QR verification
# Prototype only- final app might be native development (Kotlin/Java)
# Run with: .venv/bin/python verify_app.py
# Then open: https://127.0.0.1:5000 (current device)
# Run this on a phone: https://<computer-local-ip>:5000
# To find your computer IP address, run 'ipconfig' (Windows) / 'ip a' (Linux)

import json
from pathlib import Path

# Flask creates the web app and handles browser requests.
from flask import Flask, jsonify, request, send_from_directory

# Reuse the same verification checks as the command-line verifier.
from verify_qr import check_expiry, load_public_key, verify_payload

verify_app = Flask(__name__)


# home page
@verify_app.get("/")
def home():
    # This page opens the phone camera and reads QR codes.
    return """
    <h1>Bouncer Verifier</h1>
    <p>Scan an event QR code to verify it.</p>
    <button onclick="startScan()">Scan QR</button>
    <h2 id="result"></h2>

    <script src="/html5-qrcode.min.js"></script>
    <div id="reader"></div>

    <script>
    let scanner;

    async function startScan() {
        scanner = new Html5Qrcode("reader");

        try {
            const cameras = await Html5Qrcode.getCameras();

            if (!cameras.length) {
                throw new Error("No camera found");
            }

            // Prefer the rear/main camera, avoiding ultrawide lenses.
            const camera =
                cameras.find(c => /back|rear|main|1x/i.test(c.label) &&
                                  !/0[.]5x|ultra.?wide|wide/i.test(c.label))
                || cameras.find(c => /back|rear|environment/i.test(c.label))
                || cameras[0];

            await scanner.start(
                camera.id,
                { fps: 10, qrbox: { width: 450, height: 450 } },
                async decodedText => {
                    await verifyQr(decodedText);
                    await scanner.stop();
                },
                () => {}
            );
        } catch (error) {
            console.error("Camera error:", error);

            document.getElementById("result").textContent =
                "Camera error: " + String(error);
        }
    }

    async function verifyQr(decodedText) {
        const result = document.getElementById("result");
        result.textContent = "Checking...";
        result.style.color = "black";

        try {
            // Send the QR data to the /verify Flask endpoint.
            const response = await fetch("/verify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ qr_data: decodedText })
            });
            const data = await response.json();
            result.textContent = data.message;
            result.style.color = data.accepted ? "green" : "red";
        } catch (error) {
            // Show an error if the browser cannot contact Flask.
            result.textContent = "Verification service unavailable.";
            result.style.color = "red";
        }
    }
    </script>
"""


# verify scanned QR data
@verify_app.post("/verify")
def verify():
    # Read the JSON request sent by the browser.
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not isinstance(body.get("qr_data"), str):
        return jsonify(accepted=False, message="Invalid QR request."), 400

    try:
        # Convert the QR text back into the signed payload.
        payload = json.loads(body["qr_data"])
        if not isinstance(payload, dict):
            raise TypeError("QR data must be a JSON object.")

        # Check the signature, expiry date, and approval status.
        public_key = load_public_key()

        if not verify_payload(payload, public_key):
            return jsonify(
                accepted=False,
                message="QR code is invalid or has been tampered with.",
            ), 400

        if not check_expiry(payload):
            return jsonify(
                accepted=False,
                message="QR code has expired.",
            ), 400

        status = str(payload.get("status", "")).strip().lower()

        if status != "approved":
            messages = {
                "pending": "ID is pending approval.",
                "revoked": "ID has been revoked.",
                "unknown": "ID status is unknown.",
                "denied": "ID access has been denied.",
            }
            return jsonify(
                accepted=False,
                message=messages.get(status, "ID is not approved."),
            ), 400

    except (OSError, TypeError, ValueError, KeyError) as error:
        return jsonify(
            accepted=False,
            message=f"Unable to verify QR code: {error}",
        ), 400

    return jsonify(
        accepted=True,
        message="ID verified and approved.",
    )


@verify_app.get("/html5-qrcode.min.js")
def scanner_library():
    return send_from_directory(
        Path(__file__).parent / "static",
        "html5-qrcode.min.js",
    )


# launch the verifier
if __name__ == "__main__":
    # 0.0.0.0 allows another device on the same network to connect.
    # HTTPS is needed for camera access on most phones.
    verify_app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True, 
        ssl_context="adhoc"
    )