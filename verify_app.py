# Flask web app for QR verification
# This code is heavily AI-assisted with GitHub Copilot
# Prototype only- final app might be native development (Kotlin/Java)
# Run with: .venv/bin/python verify_app.py
# Then open: https://127.0.0.1:5000 (current device)
# Run this on a phone: https://<computer-local-ip>:5000
# To find your computer IP address, run 'ipconfig' (Windows) / 'ip a' (Linux)

import json
from pathlib import Path

# Flask creates the web app and handles browser requests.
from flask import Flask, jsonify, request, send_from_directory

from sheets import load_id_lists

# Reuse the same verification checks as the command-line verifier.
from verify_qr import check_expiry, load_public_key, verify_payload

verify_app = Flask(__name__)
verify_app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


# home page
@verify_app.get("/")
def home():
    # This page opens the phone camera and reads QR codes.
    return """
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 1.5rem;
            font-family: system-ui, sans-serif;
            font-size: 1rem;
            line-height: 1.5;
        }

        button {
            width: 100%;
            min-height: 3.25rem;
            padding: 0.75rem 1rem;
            border: 0;
            border-radius: 0.5rem;
            background: #aa1717;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
        }

        #reader {
            width: 100%;
            max-width: 32rem;
            margin-top: 1rem;
        }

        #result {
            overflow-wrap: anywhere;
        }

        #details {
            max-width: 32rem;
            margin-top: 1rem;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 0.75rem;
            background: #f7f7f7;
        }

        #details h3 {
            margin-top: 0;
        }

        #details dl {
            display: grid;
            grid-template-columns: minmax(7rem, 0.8fr) 1.2fr;
            gap: 0.5rem 1rem;
            margin: 0;
        }

        #details dt {
            font-weight: 600;
        }

        #details dd {
            margin: 0;
            overflow-wrap: anywhere;
        }

        #sheets-status {
            display: inline-block;
            margin: 0.75rem 0;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            background: #666;
            color: white;
            font-size: 0.9rem;
        }

        @media (min-width: 600px) {
            body {
                max-width: 42rem;
                margin: 0 auto;
            }

            button {
                width: auto;
                min-width: 12rem;
            }
        }
    </style>
    <h1>DigitalIDSystem verifier</h1>
    <p>(working prototype)</p>
    <div id="sheets-status">Google Sheets: checking...</div>
    <button id="scan-button" onclick="startScan()">Scan QR</button>
    <h2 id="result"></h2>
    <script src="/html5-qrcode.min.js"></script>
    <div id="reader"></div>

    <div id="details">
        <h3>ID details</h3>
        <dl>
            <dt>ID</dt><dd id="detail-id">—</dd>
            <dt>First name</dt><dd id="detail-firstname">—</dd>
            <dt>Last name</dt><dd id="detail-lastname">—</dd>
            <dt>Role</dt><dd id="detail-role">—</dd>
            <dt>Band</dt><dd id="detail-bandname">—</dd>
            <dt>Event</dt><dd id="detail-event">—</dd>
            <dt>Expiry date</dt><dd id="detail-expiry">—</dd>
            <dt>Status</dt><dd id="detail-status">—</dd>
        </dl>
    </div>

    <script>
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

            // Prefer the rear/main camera, avoiding ultrawide lenses.
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

    checkSheetsStatus();

    async function verifyQr(decodedText) {
        const result = document.getElementById("result");
        result.textContent = "Checking...";
        result.style.color = "black";
        for (const field of detailFields) {
            document.getElementById(`detail-${field}`).textContent = "—";
        }

        try {
            // Send the QR data to the /verify Flask endpoint.
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
            // Show an error if the browser cannot contact Flask.
            result.textContent = "Could not check online ID data. Try again.";
            result.style.color = "red";
        }
    }
    </script>
"""


@verify_app.get("/status")
def sheets_status():
    try:
        load_id_lists()
    except RuntimeError:
        return jsonify(connected=False), 503

    return jsonify(connected=True)


# verify scanned QR data
@verify_app.post("/verify")
def verify():
    # Validate a scanned QR payload and return a browser-friendly result.
    # Read the JSON request sent by the browser.
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not isinstance(body.get("qr_data"), str):
        return jsonify(accepted=False, message="Invalid QR request."), 400

    try:
        # Convert the QR text back into the signed payload.
        payload = json.loads(body["qr_data"])
        if not isinstance(payload, dict):
            raise TypeError("QR data must be a JSON object.")

        # Check the signature and expiry date before consulting live status.
        public_key = load_public_key()

        if not verify_payload(payload, public_key):
            return jsonify(
                accepted=False,
                message="QR code is invalid or has been tampered with.",
            ), 400

        details = {
            # Return safe display fields without exposing the signature.
            field: payload[field]
            for field in (
                "id",
                "firstname",
                "lastname",
                "role",
                "bandname",
                "event",
                "expiry",
                "status",
            )
            if field in payload
        }

        if not check_expiry(payload):
            return jsonify(
                accepted=False,
                message="QR code has expired.",
                details=details,
            ), 400

        id_number = payload.get("id")
        if not isinstance(id_number, str) or not id_number.strip():
            return jsonify(
                accepted=False,
                message="QR code is missing a valid ID number.",
                details=details,
            ), 400

        try:
            # Compare the signed record with the current Google Sheets record.
            current_records = load_id_lists()
        except RuntimeError:
            details["status"] = str(payload.get("status", "unknown")).strip().lower()
            return jsonify(
                accepted=False,
                message="Offline and online ID data do not match, check Google Sheets",
                details=details,
            ), 503

        current_record = current_records.get(id_number.strip())
        if current_record is None:
            return jsonify(
                accepted=False,
                message="ID was not found in the current registry.",
                details=details,
            ), 400

        current_status = current_record.get("status", "").strip().lower()
        details["status"] = current_status

        if current_status != "approved":
            # Report the live registry decision before comparing the old QR status.
            messages = {
                "pending": "ID is pending approval.",
                "revoked": "ID has been revoked.",
                "unknown": "ID status is unknown.",
                "denied": "ID access has been denied.",
            }
            return jsonify(
                accepted=False,
                message=messages.get(current_status, "ID is not approved."),
                details=details,
            ), 400

        fields_to_compare = (
            "firstname",
            "lastname",
            "role",
            "bandname",
            "status",
        )
        for field in fields_to_compare:
            signed_value = str(payload.get(field, "")).strip().casefold()
            current_value = str(current_record.get(field, "")).strip().casefold()
            if signed_value != current_value:
                return jsonify(
                    accepted=False,
                    message="QR code does not match the current registry.",
                    details=details,
                ), 400

    except (OSError, TypeError, ValueError, KeyError) as error:
        return jsonify(
            accepted=False,
            message=f"Unable to verify QR code: {error}",
        ), 400

    return jsonify(
        accepted=True,
        message="ID verified and approved.",
        details=details,
    )


@verify_app.get("/html5-qrcode.min.js")
def scanner_library():
    # Serve the local QR scanner library to the verification page.
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
        debug=False,
        ssl_context="adhoc"
    )