# Flask web app for QR verification
# This code is heavily AI-assisted with GitHub Copilot
# To edit the website, head to templates/index.html
# Prototype only- final app might be native development (Kotlin/Java)
# Run with: .venv/bin/python verify_app.py
# Then open: https://127.0.0.1:5000 (current device)
# Run this on a phone: https://<computer-local-ip>:5000
# To find your computer IP address, run 'ipconfig' (Windows) / 'ip a' (Linux)

import json
from pathlib import Path

# Flask creates the web app and handles browser requests.
from flask import Flask, jsonify, render_template, request, send_from_directory

from sheets import load_id_lists

# Reuse the same verification checks as the command-line verifier.
from verify_qr import check_expiry, load_public_key, verify_payload

verify_app = Flask(__name__)
verify_app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


# home page
@verify_app.get("/")
def home():
    # This page opens the phone camera and reads QR codes.
    return render_template("index.html")


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
    verify_app.run(host="0.0.0.0", port=5000, debug=False, ssl_context="adhoc")
