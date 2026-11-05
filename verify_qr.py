# qr verification

import base64
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

PUBLIC_KEY_FILE = "signing_public_key.pem"


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