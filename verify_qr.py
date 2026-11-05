# qr verification

import base64
import json
from datetime import date

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

PUBLIC_KEY_FILE = "signing_public_key.pem"

def check_expiry(payload):
    expiry_date = date.fromisoformat(payload["expiry"])
    
    if expiry_date < date.today():
        print("Error: QR is EXPIRED.")
        return False
    
    print("QR is still valid.")
    return True

def check_status(payload):
    status = payload.get("status", "").strip().lower()

    if status != "approved":
        print(f"Error: ID status is {status or 'missing'}.")
        return False

    print("ID status is approved.")
    return True

def load_public_key():
    with open(PUBLIC_KEY_FILE, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())
    

def verify_payload(payload, public_key):
    signature_text = payload.pop("signature", None)
    
    if signature_text is None:
        print("Error: QR has no signature.")
        return False
    
    try:
        signature = base64.b64decode(signature_text, validate=True)
        
        message = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        
        public_key.verify(signature, message)
    except (InvalidSignature, ValueError):
        print("Error: QR data has been TAMPERED.")
        return False
    
    print("QR signature is valid.")
    return True

# Verification test if runned here directly
if __name__ == "__main__":
    print("Paste the JSON text from your QR code:")
    qr_text = input("> ")

    try:
        payload = json.loads(qr_text)
    except json.JSONDecodeError:
        print("Error: QR data is not valid JSON.")
        raise SystemExit(1)

    public_key = load_public_key()
    if verify_payload(payload, public_key) and check_expiry(payload):
        check_status(payload)