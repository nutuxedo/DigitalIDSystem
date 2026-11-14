# QR Verification-offline based
# For phone server QR scanner, head to verify_app.py

import base64
import importlib
import json
import sys
from datetime import date

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

try:
    cv2 = importlib.import_module("cv2")
except ModuleNotFoundError as error:
    raise RuntimeError(
        "OpenCV is required. Install it with: python -m pip install opencv-python"
    ) from error

PUBLIC_KEY_FILE = "signing_public_key.pem"

def check_expiry(payload):
    # A QR code remains valid through its expiry date.
    expiry = payload.get("expiry")
    if not isinstance(expiry, str):
        raise TypeError("QR expiry date is missing or invalid.") 

    expiry_date = date.fromisoformat(expiry)
    
    if expiry_date < date.today():
        print("Error: QR is EXPIRED.")
        return False
    
    print("QR is still valid.")
    return True

def check_status(payload):
    # Only approved IDs pass the final status check.
    status_value = payload.get("status")
    status = status_value.strip().lower() if isinstance(status_value, str) else ""

    if status != "approved":
        print(f"Error: ID status is {status or 'missing'}.")
        return False

    print("ID status is approved.")
    return True

def load_public_key():
    # Load the public key used to verify QR signatures.
    with open(PUBLIC_KEY_FILE, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())


def decode_qr_image(image_path):
    # Read the image and convert its QR contents into a JSON payload.
    image = cv2.imread(image_path)
    if image is None:
        raise RuntimeError(f"Could not read QR image: {image_path}")

    qr_data, _, _ = cv2.QRCodeDetector().detectAndDecode(image)
    if not qr_data:
        raise RuntimeError(f"No readable QR code found in: {image_path}")

    try:
        return json.loads(qr_data)
    except json.JSONDecodeError as error:
        raise RuntimeError("QR data is not valid JSON.") from error

def verify_payload(payload, public_key):
    # Remove the signature and verify the remaining signed payload.
    if not isinstance(payload, dict):
        raise TypeError("QR payload must be a JSON object.")

    signature_text = payload.pop("signature", None)
    
    if not isinstance(signature_text, str):
        print("Error: QR has no valid signature.")
        return False
    
    try:
        signature = base64.b64decode(signature_text, validate=True)
        
        message = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        
        public_key.verify(signature, message)
    except (InvalidSignature, TypeError, ValueError):
        print("Error: QR data has been TAMPERED.")
        return False
    
    print("QR signature is valid.")
    return True

if __name__ == "__main__":
    # Support direct command-line verification of one saved QR image.
    try:
        payload = decode_qr_image(sys.argv[1])
    except IndexError:
        print("Usage: python verify_qr.py <qr-image> (usually found in generated_qr_images)")
        raise SystemExit(1)
    except RuntimeError as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    public_key = load_public_key()
    if verify_payload(payload, public_key) and check_expiry(payload):
        check_status(payload)