# CLI menu and other stuff
# Redo soon with GUI (Kotlin/Java)

import qr_generator
from sheets import load_id_lists


def get_expiry_date():
    # Keep asking until the user provides an expiry date.
    while True:
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()

        if expiry_date:
            return expiry_date

        print("Expiry date cannot be empty. Please input a date.")

def get_event_name():
    # Collect the event name and provide a quick way back to the menu.
    while True:
        print("To return to menu, type 'exit'")
        event_name = input("Enter event name: ").strip()
        
        if event_name.lower() == "exit":
            print("Returning to menu...")
            main()
        
        if event_name.lower() in (
            "exis", 
            "exix", 
            "exid", 
            "exir", 
            "exitt", 
            "wxit", 
            "rxit", 
            "dxit", 
            "efit"
        ):
            print("Did you mean 'exit'?")
            continue

        if not event_name:
            print("Event name cannot be empty.")
            continue
        
        return event_name

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
        id_lookup()
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
        print("\nThis ID is currently PENDING.")
        display_id(id_number, person, event_name, expiry_date)
        id_lookup()
        return
    
    if status != "approved":
        # Treat unrecognized statuses as invalid rather than allowing access.
        print(f"\nThis ID has an invalid status: {status!r}.")
        print("ID status should either be the following: approved, pending, denied or revoked")
        print("Access denied. Check Google Sheets and try again.")
        return
    
    print("\nThis ID is APPROVED.")
    display_id(id_number, person, event_name, expiry_date)
    # Only approved records can proceed to optional QR generation.
    qr_generator.qr_inquiry(id_number, person, event_name, expiry_date)

# Option 1
def id_lookup():
    # Gather lookup details, load the registry, and process one ID.
    event_name = get_event_name()
    expiry_date = get_expiry_date()
    
    try:
        print("Obtaining information from Google Sheets...")
        id_lists = load_id_lists()
    except RuntimeError as error:
        print(f"Could not load ID data: {error}")
        return

    print("Google Sheets connected.")
    print("To return to menu, type 'exit'")
    user_id = input("Enter ID number: ")
    if user_id == "exit":
        print("Returning to menu...")
        main()
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

    print("To return to menu, type 'exit'.")
    image_path = input("Enter the path to the QR image: ").strip()
    if not image_path:
        print("QR image path cannot be empty.")
        return
    
    if image_path == "exit":
        print("Returning to menu.")
        return

    try:
        payload = decode_qr_image(image_path)
        public_key = load_public_key()
        if verify_payload(payload, public_key) and check_expiry(payload):
            check_status(payload)
    except (OSError, RuntimeError, TypeError, ValueError, KeyError) as error:
        print(f"Could not verify QR image: {error}")

# CLI menu
def show_menu():
    # Display the actions available from the command-line menu.
    print("DigitalIDSystem (placeholder)")
    print("1. ID lookup and generate QR code")
    print("2. Verify QR image")
    print("3. Start QR verifier server (No function)")
    print("4. Exit (or type 'exit')")

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
            print("To add. Please launch 'verify_app.py'.")    
        elif choice in ("4", "exit"):
            print("Exiting program.")
            raise SystemExit
        else:
            print("Invalid option.")
    

# launch program
if __name__ == "__main__":
    main()
    