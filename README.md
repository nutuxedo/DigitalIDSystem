# Digital ID System

A Python CLI digital ID platform for issuing and verifying event credentials.

> **Note:** This is a working prototype, changes in development will occur rapidly and may not reflect the final system.

## Features

* Able to read ID entries from Google Form via Google Sheets integration through OAuth
* Lookup ID entries and generate a QR with given information
* Local server (Flask) and offline-capable for QR verification
* Python cryptography signature via Ed25519

## Dependencies

Refer to requirements.txt

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

Lorem ipsum
