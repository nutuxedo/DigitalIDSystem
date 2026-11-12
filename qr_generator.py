import base64
import json
import os
import re
import stat
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
    # Keep the public key synchronized with the private signing key.
    expected_key = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    if PUBLIC_KEY_FILE.exists():
        try:
            stored_public_key = serialization.load_pem_public_key(
                PUBLIC_KEY_FILE.read_bytes()
            )
            stored_key = stored_public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        except (OSError, ValueError, TypeError) as error:
            raise RuntimeError(
                f"Could not load public key '{PUBLIC_KEY_FILE}'."
            ) from error

        if stored_key != expected_key:
            raise RuntimeError(
                "Public/private signing keys do not match. Restore the matching "
                "public key or replace the private key intentionally."
            )
        return

    PUBLIC_KEY_FILE.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def load_or_create_private_key():
    # Load a protected private key or create one for the first run.
    if PRIVATE_KEY_FILE.exists():
        permissions = PRIVATE_KEY_FILE.stat().st_mode
        if permissions & (stat.S_IRWXG | stat.S_IRWXO):
            raise RuntimeError(
                f"Private signing key '{PRIVATE_KEY_FILE}' is accessible by "
                "group or other users. Restrict it to the owner before use."
            )
        return serialization.load_pem_private_key(
            PRIVATE_KEY_FILE.read_bytes(),
            password=None,
        )

    private_key = Ed25519PrivateKey.generate()
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    file_descriptor = os.open(
        PRIVATE_KEY_FILE,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        stat.S_IRUSR | stat.S_IWUSR,
    )
    with os.fdopen(file_descriptor, "wb") as key_file:
        key_file.write(private_key_bytes)

    print(f"Created signing key: {PRIVATE_KEY_FILE}")
    return private_key


private_key = load_or_create_private_key()
public_key = private_key.public_key()
save_public_key(public_key)


def sign_message(message, private_key):
    # Sign the canonical payload before it is placed in the QR code.
    return private_key.sign(message)


def verify_payload(payload):
    # Confirm that the QR payload has not changed since it was signed.
    signature_text = payload.pop("signature", None)

    if signature_text is None:
        print("ERROR: QR code has no signature.")
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
        print("ERROR: QR data was changed or is invalid.")
        return False

    print("Signature is valid.")
    return True


def qr_generation(id_number, person, event_name, expiry_date):
    # Build, sign, and save the QR payload for an approved ID.
    payload = {
        "id": id_number,
        "firstname": person["firstname"],
        "lastname": person["lastname"],
        "role": person["role"],
        "bandname": person["bandname"],
        "status": person["status"],
        "event": event_name,
        "expiry": expiry_date,
    }

    message = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    signature = sign_message(message, private_key)
    payload["signature"] = base64.b64encode(signature).decode("ascii")

    # Keep generated filenames safe and predictable.
    safe_id = re.sub(r"[^A-Za-z0-9_-]+", "_", id_number).strip("_")
    output_folder = Path("generated_qr_images")
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"qr_{safe_id or 'unknown'}.png"
    image = qrcode.make(json.dumps(payload, separators=(",", ":")))
    image.save(output_file)
    return output_file


def qr_inquiry(id_number, person, event_name, expiry_date):
    # Ask for confirmation before creating the QR image.
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
