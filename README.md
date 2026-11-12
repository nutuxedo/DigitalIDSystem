# Digital ID System

A Python CLI digital ID platform for issuing and verifying event credentials.

> [!NOTE] NOTE
> This is a working prototype, changes in development will occur rapidly and may not reflect the final system.

## Features

* Able to read ID entries from Google Form via Google Sheets integration through OAuth
* Lookup ID entries and generate a QR with given information
* Local server (Flask) and offline-capable for QR verification
* Python cryptography signature via Ed25519

## How it works

### ID Lookup and QR generation

1. Asks for event name and expiry date (to be improved soon!).
2. Connects to Google Sheets and loads the ID records. The first time, it asks you to sign in. (OAuth)
3. User enters an ID number from the form.
4. Program checks the Google sheets form.
5. ID status is checked:

   | Status | Result |
   | --- | --- |
   | `approved` | ID is approved and details are shown |
   | `pending` | ID is currently pending and details are shown |
   | `revoked` or `denied` | Access is denied |
   | Any other status | Access is denied |

6. If `approved`, asks whether to generate a QR code. If yes, the QR code is saved in `generated_qr_images`.

7. If the ID number is not found in Google Sheets, the user is notified and asked to try again.

### QR verification

#### Online (Flask server)

1. The Flask server starts with `verify_app.py` and hosts the verifier page.
2. The page can be opened at `https://127.0.0.1:5000` on the computer running the server.
3. A phone on the same network can open `https://<computer-local-ip>:5000` to use the verifier.
4. The page uses the device camera to scan the QR code.
5. The verifier checks the QR code's signature, expiry date, and ID status.
6. The page shows whether the ID is valid and approved.

#### Offline (Python file)

1. The verifier reads a saved QR image from the local computer.
2. It decodes the QR code and checks its digital signature.
3. It checks whether the QR code has expired.
4. It checks whether the ID status is approved.
5. The terminal shows whether the QR code is valid and approved.

## Dependencies

* gspread v6.0 or later
* google-auth v2.0 or later
* google-auth-oauthlib v1.0 or later
* qrcode v8.2 or later
* Pillow v13 or later
* cryptography v50.0.2 or later
* opencv-python v4.10 or later
* Flask v3.1.3 or later

Install the dependecies:

```bash
python -m pip install -r requirements.txt
```

## Initial Setup

### Google Sheets (via Google Cloud/OAuth)

> [!NOTE] NOTE
> Make sure you have a Google Cloud account available, this will not incur any credits or payments for using the OAuth session.

Lorem ipsum
