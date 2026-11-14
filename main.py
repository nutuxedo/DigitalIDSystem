# CLI menu and other stuff
# Redo soon with GUI (Kotlin/Java)

import json
import os
import socket
import subprocess
import sys
from datetime import date
from pathlib import Path

import qr_generator
from sheets import load_id_lists

GENERATED_QR_PATH = Path("generated_qr_images")

EXIT_TYPOS = {"exis", "exix", "exid", "exir", "exitt", "wxit", "rxit", "dxit", "efit"}

EVENT_CONFIG_FILE = Path("event_config.json")
verifier_process = None
VERIFIER_HOST = "127.0.0.1"
VERIFIER_PORT = 5000


def get_expiry_date(current_value=None):
    # Keep asking until the user provides a valid expiry date.
    while True:
        prompt = "Expiry date (YYYY-MM-DD)"
        if current_value:
            prompt += f" [{current_value}]"
        expiry_date = input(f"{prompt}: ").strip() or current_value

        if expiry_date == "exit":
            return None

        try:
            date.fromisoformat(expiry_date)
        except (TypeError, ValueError):
            print("Expiry date must use YYYY-MM-DD format.")
            continue

        if expiry_date:
            return expiry_date

        print("Expiry date cannot be empty. Please input a date.")


def get_event_name(current_value=None):
    # Collect the event name, keeping the existing value as the default.
    while True:
        print("To go back, type 'exit'")
        prompt = "Event name"

        if current_value:
            prompt += f" [{current_value}]"
        event_name = input(f"{prompt}: ").strip() or current_value

        if event_name == "exit":
            return None

        if not event_name:
            print("Event name cannot be empty.")
            continue

        return event_name


def load_event_config():
    if not EVENT_CONFIG_FILE.exists():
        return None

    try:
        config = json.loads(EVENT_CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Could not read event settings from '{EVENT_CONFIG_FILE}'."
        ) from error

    if not isinstance(config, dict):
        raise TypeError(f"Event settings in '{EVENT_CONFIG_FILE}' are invalid.")

    event_name = config.get("event_name")
    expiry_date = config.get("expiry_date")
    if not isinstance(event_name, str) or not event_name.strip():
        raise RuntimeError(f"Event name in '{EVENT_CONFIG_FILE}' is invalid.")
    try:
        date.fromisoformat(expiry_date)
    except (TypeError, ValueError) as error:
        raise RuntimeError(
            f"Expiry date in '{EVENT_CONFIG_FILE}' must use YYYY-MM-DD format."
        ) from error

    return {"event_name": event_name.strip(), "expiry_date": expiry_date}


def save_event_config(event_name, expiry_date):
    config = {
        "event_name": event_name,
        "expiry_date": expiry_date,
    }
    try:
        EVENT_CONFIG_FILE.write_text(
            json.dumps(config, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as error:
        raise RuntimeError(
            f"Could not save event settings to '{EVENT_CONFIG_FILE}'."
        ) from error


def configure_event():
    # Ask for settings once and save them for later runs.
    current_config = load_event_config()
    current_event = current_config["event_name"] if current_config else None
    current_expiry = current_config["expiry_date"] if current_config else None
    event_name = get_event_name(current_event)
    if event_name is None:
        print("Returning to menu.")
        return None

    expiry_date = get_expiry_date(current_expiry)
    if expiry_date is None:
        print("Returning to menu.")
        return None

    save_event_config(event_name, expiry_date)
    print(f"Event settings saved to {EVENT_CONFIG_FILE}.")
    return {"event_name": event_name, "expiry_date": expiry_date}


def get_event_config():
    config = load_event_config()
    if config is None:
        print("No event details found, please set them.")
        return configure_event()
    return config


def display_id(id_number, person, event_name, expiry_date):
    # Show the details attached to the matching ID record.
    print(f"\n--- Digital ID: {id_number} ---")
    print(f"Event:  {event_name}")
    print(f"Name:   {person['firstname']} {person['lastname']}")
    print(f"Role:   {person['role']}")
    print(f"Band:   {person['bandname']}")
    print(f"Headshot picture: {person['headshot']}")
    print(f"Expiry date: {expiry_date}")
    print("------------------------------")


def identify_id(id_number, id_lists, event_name, expiry_date):
    # Apply the record status before displaying details or generating a QR code.
    person = id_lists.get(id_number)

    if person is None:
        # A missing ID cannot be approved.
        print(f"No ID number found on Google Sheets: {id_number}")
        print("Check the ID number and try again.")
        return

    status = person["status"].strip().lower()

    if status in ("revoked", "denied"):
        # Revoked and denied records never receive access.
        print(f"\nAccess denied for ID: {id_number}")
        print(f"Reason: status is {status}.")
        id_lookup()
        return

    if status == "pending":
        # Pending records can be viewed but cannot generate an approved QR code.
        print("\nThis ID is currently pending.")
        display_id(id_number, person, event_name, expiry_date)
        return

    if status != "approved":
        # Treat unrecognized statuses as invalid rather than allowing access.
        print(f"\nThis ID has an invalid status: {status!r}.")
        print(
            "ID status should either be the following: approved, pending, denied or revoked"
        )
        print("Access denied. Check Google Sheets and try again.")
        return

    print("\nThis ID is APPROVED.")
    display_id(id_number, person, event_name, expiry_date)
    # Only approved records can proceed to optional QR generation.
    qr_generator.qr_inquiry(id_number, person, event_name, expiry_date)


# Option 1
def id_lookup():
    # Load saved event details, then process one ID.
    try:
        config = get_event_config()
    except RuntimeError as error:
        print(f"Could not load event settings: {error}")
        return
    if config is None:
        return

    event_name = config["event_name"]
    expiry_date = config["expiry_date"]

    try:
        print("Obtaining information from Google Sheets...")
        id_lists = load_id_lists()
    except RuntimeError as error:
        print(f"Could not load ID data: {error}")
        return

    print("Google Sheets connected.")
    while True:
        print("To return to menu, type 'exit'")
        user_id = input("Enter ID number: ")
        if user_id in EXIT_TYPOS:
            print("Did you mean exit?")
        if user_id == "exit":
            print("Returning to menu...")
            break
        else:
            identify_id(user_id, id_lists, event_name, expiry_date)


# Option 2
def verify_qr_image():
    # Verify a saved QR image without starting the Flask server.
    from verify_qr import (
        check_expiry,
        check_status,
        decode_qr_image,
        load_public_key,
        verify_payload,
    )

    while True:
        print("To return to menu, type 'exit'.")
        image_input = input(
            f"Enter QR filename (inside {GENERATED_QR_PATH}) or enter a specific path: "
        ).strip()
        if not image_input:
            print("QR image path cannot be empty.")
            continue
        if image_input in EXIT_TYPOS:
            print("Did you mean exit?")
        if image_input == "exit":
            print("Returning to menu.")
            break
        image_path = Path(image_input)
        if not image_path.is_absolute() and image_path.parent == Path("."):
            image_path = GENERATED_QR_PATH / image_path
        try:
            payload = decode_qr_image(str(image_path))
            public_key = load_public_key()
            if verify_payload(payload, public_key) and check_expiry(payload):
                check_status(payload)
                break
        except (OSError, RuntimeError, TypeError, ValueError, KeyError) as error:
            print(f"Could not verify QR image: {error}")


def start_verifier():
    global verifier_process
    if verifier_process is not None and verifier_process.poll() is None:
        print(f"QR verifier is already running (PID {verifier_process.pid}).")
        return
    try:
        with socket.create_connection((VERIFIER_HOST, VERIFIER_PORT), timeout=0.5):
            print(f"QR verifier is already running on port {VERIFIER_PORT}.")
            return
    except OSError:
        pass
    cmd = [sys.executable, "verify_app.py"]
    try:
        if os.name == "nt":
            verifier_process = subprocess.Popen(
                cmd,
                creationflags=subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )
        else:
            verifier_process = subprocess.Popen(
                cmd,
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )
    except OSError as error:
        verifier_process = None
        print(f"Could not start QR verifier: {error}")
        return

    print(f"QR verifier started (PID {verifier_process.pid}).")


def stop_verifier():
    global verifier_process

    if verifier_process is None or verifier_process.poll() is not None:
        verifier_process = None
        print("QR verifier is not running.")
        return

    verifier_process.terminate()
    try:
        verifier_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        verifier_process.kill()
        verifier_process.wait()

    print("QR verifier stopped.")
    verifier_process = None


# CLI menu
def show_menu():
    # Display the actions available from the command-line menu.
    try:
        config = load_event_config()
    except RuntimeError as error:
        config = None
        print(f"Could not load event settings. ({error})")

    event_name = config["event_name"] if config else "Not set"
    expiry_date = config["expiry_date"] if config else "Not set"

    with open("VERSION.txt", "r", encoding="utf-8") as file:
        version = file.read()

    print("DigitalIDSystem (placeholder)")
    print(version)
    print("\n========================================")
    print("\nCurrent event details")
    print(f"\nEvent name: {event_name}")
    print(f"Expiry date: {expiry_date}")
    print("\nTo change these details, type 5.")
    print("\n========================================")
    print("\n1. ID lookup and generate QR code")
    print("2. Verify QR image")
    print("3. Start QR verifier server")
    print("4. Stop QR verifier server")
    print("5. Edit event settings")
    print("6. Exit (or type 'exit')")


# program initialization
def main():
    # Keep the application running until the user chooses to exit.
    while True:
        print()
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            id_lookup()
        elif choice == "2":
            verify_qr_image()
        elif choice == "3":
            start_verifier()
        elif choice == "4":
            stop_verifier()
        elif choice == "5":
            try:
                configure_event()
            except RuntimeError as error:
                print(f"Could not save event settings: {error}")
        elif choice in EXIT_TYPOS:
            print("Did you mean exit?")
        elif choice in ("6", "exit"):
            print("Exiting program.")
            raise SystemExit
        else:
            print("Invalid option.")


# launch program
if __name__ == "__main__":
    main()
