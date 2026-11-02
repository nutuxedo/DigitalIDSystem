from sheets import load_id_lists


def display_id(id_number, person):
    print(f"\n--- Digital ID: {id_number} ---")
    print(f"Name:   {person['firstname']} {person['lastname']}")
    print(f"Role:   {person['role']}")
    print(f"Band:   {person['bandname']}")
    print(f"Headshot picture: {person['headshot']}")
    print("------------------------------")  

def identify_id(id_number, id_lists):
    person = id_lists.get(id_number)
    
    if person is None:
        print(f"No ID number found: {id_number}")
        return
    
    status = person["status"].lower()

    if status == "revoked":
        print(f"\nThis ID is DENIED/REVOKED: {id_number}")
        return
    
    if status == "pending":
        print("\nThis ID is currently PENDING.")
        display_id(id_number, person)
        return
    
    if status != "approved":
        print("Invalid status. Access denied.")
        return
    
    print("\nThis ID is APPROVED.")
    display_id(id_number, person)

# user input 
def main():
    try:
        id_lists = load_id_lists()
    except RuntimeError as error:
        print(f"Could not load ID data: {error}")
        return

    user_id = input("Enter ID number: ")
    identify_id(user_id, id_lists)

# launch program
if __name__ == "__main__":
    main()
    