import qr_generator
from sheets import load_id_lists


# main code
def get_expiry_date():
    while True:
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()

        if expiry_date:
            return expiry_date

        print("Expiry date cannot be empty. Please input a date.")

def get_event_name():
    while True:
        event_name = input("Enter event name (to exit the program, type exit): ").strip()
        
        if event_name.lower() == "exit":
            print("Exiting program.")
            raise SystemExit
        
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
    print(f"\n--- Digital ID: {id_number} ---")
    print(f"Event:  {event_name}")
    print(f"Name:   {person['firstname']} {person['lastname']}")
    print(f"Role:   {person['role']}")
    print(f"Band:   {person['bandname']}")
    print(f"Headshot picture: {person['headshot']}")
    print(f"Expiry date: {expiry_date}")
    print("------------------------------")

def identify_id(id_number, id_lists, event_name, expiry_date):
    person = id_lists.get(id_number)

    if person is None:
        print(f"No ID number found on Google Sheets: {id_number}")
        print("Check the ID number and try again.")
        return

    status = person["status"].strip().lower()

    if status in ("revoked", "denied"):
        print(f"\nAccess denied for ID: {id_number}")
        print(f"Reason: status is {status}.")
        return
    
    if status == "pending":
        print("\nThis ID is currently PENDING.")
        display_id(id_number, person, event_name, expiry_date)
        return
    
    if status != "approved":
        print(f"\nThis ID has an invalid status: {status!r}.")
        print("ID status should either be the following: approved, pending, denied or revoked")
        print("Access denied. Check Google Sheets and try again.")
        return
    
    print("\nThis ID is APPROVED.")
    display_id(id_number, person, event_name, expiry_date)
    qr_generator.qr_inquiry(id_number, person, event_name, expiry_date)

def id_lookup():
    event_name = get_event_name()
    expiry_date = get_expiry_date()
    
    try:
        print("Obtaining information from Google Sheets...")
        id_lists = load_id_lists()
    except RuntimeError as error:
        print(f"Could not load ID data: {error}")
        return

    user_id = input("Enter ID number: ")
    identify_id(user_id, id_lists, event_name, expiry_date)


def verify_qr_image():
    from verify_qr import (
        check_expiry,
        check_status,
        decode_qr_image,
        load_public_key,
        verify_payload,
    )

    image_path = input("Enter the path to the QR image: ").strip()
    if not image_path:
        print("QR image path cannot be empty.")
        return

    try:
        payload = decode_qr_image(image_path)
        public_key = load_public_key()
        if verify_payload(payload, public_key) and check_expiry(payload):
            check_status(payload)
    except (OSError, RuntimeError, TypeError, ValueError, KeyError) as error:
        print(f"Could not verify QR image: {error}")


def show_menu():
    print("Digital ID System")
    print("1. ID lookup and generate QR code")
    print("2. Verify QR image")
    print("3. Start QR verifier server (No function)")
    print("3. Exit")


def main():
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
        elif choice == "4":
            print("Exiting program.")
            return
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
    

# launch program
if __name__ == "__main__":
    main()
    