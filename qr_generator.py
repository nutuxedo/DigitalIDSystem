import json
import re
from pathlib import Path

import qrcode


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
            break
        if answer == "n":
            print("QR not generated\n")
            break
        print("Please enter Y or N.")