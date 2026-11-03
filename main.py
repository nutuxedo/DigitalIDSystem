import qr_generator
from sheets import load_id_lists


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
        
        if event_name:
            return event_name

        print("Event name cannot be empty.")

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

# user input
def main():
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

# launch program
if __name__ == "__main__":
    main()
    