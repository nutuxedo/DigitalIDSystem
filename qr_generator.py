import base64
import json
import re
from pathlib import Path

import qrcode
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

PUBLIC_KEY_FILE = Path("signing_public_key.pem")
PRIVATE_KEY_FILE = Path("signing_private_key.pem")

def save_public_key(public_key):
    if not PUBLIC_KEY_FILE.exists():
        PUBLIC_KEY_FILE.write_bytes(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

def load_or_create_private_key():
    if PRIVATE_KEY_FILE.exists():
        return serialization.load_pem_private_key(
            PRIVATE_KEY_FILE.read_bytes(),
            password=None,
        )

    private_key = Ed25519PrivateKey.generate()
    
    PRIVATE_KEY_FILE.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    
    print(f"Created signing key: {PRIVATE_KEY_FILE}")
    return private_key

private_key = load_or_create_private_key()
public_key = private_key.public_key()
save_public_key(public_key)

# digital signature section
def sign_message(message, private_key):
    return private_key.sign(message)

def verify_payload(payload):
    signature_text = payload.pop("signature", None)

    if signature_text is None:
        print("ERROR: QR code has no signature.")
        return False

    try:
        signature = base64.b64decode(signature_text)

        message = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        public_key.verify(signature, message)
    except (InvalidSignature, ValueError):
        print("ERROR: QR data was changed or is invalid.")
        return False

    print("Signature is valid.")
    return True


# main qr generation
def qr_generation(id_number, person, event_name, expiry_date):
    payload = {
        "id": id_number,
        "firstname": person["firstname"],
        "lastname": person["lastname"],
        "role": person["role"],
        "bandname": person["bandname"],
        "status": person["status"],
        "event": event_name,
        "expiry": expiry_date
    }
    
    message = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    
    signature = sign_message(message, private_key)
    
    payload["signature"] = base64.b64encode(signature).decode("ascii")
    
    safe_id = re.sub(r"[^A-Za-z0-9_-]+", "_", id_number).strip("_")
    output_folder = Path("generated_qr_images")
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"qr_{safe_id or 'unknown'}.png"
    image = qrcode.make(json.dumps(payload, separators=(",", ":")))
    image.save(output_file)
    return output_file
    
# asks for QR generation
def qr_inquiry(id_number, person, event_name, expiry_date):
    while True:
        answer = input("Generate QR code? (Y/n) ").strip().lower()
        if answer in ("y", ""):
            output_file = qr_generation(id_number, person, event_name, expiry_date)
            print(f"QR generated: {output_file}\n")
            print("Located at 'generated_qr_images' folder.")
            break
        if answer == "n":
            print("QR not generated\n")
            break
        print("Please enter Y or N.")
        