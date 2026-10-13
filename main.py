# id system
# link to Google Sheets

testinfo = {
    "ID-001": {
        "lastname": "Doe",
        "firstname": "John",
        "role": "Band",
        "bandname": "Bucket",
        "status": "pending",
    }
}
# debug test
# print(testinfo)

def display_id(id_number, person):
    print(f"\n--- Digital ID: {id_number} ---")
    print(f"Name:   {person['firstname']} {person['lastname']}")
    print(f"Role:   {person['role']}")
    print(f"Band:   {person['bandname']}")
    print("------------------------------")  

def identify_id(id_number):
    person = testinfo.get(id_number)
    
    if person is None:
        print(f"No ID number found: {id_number}")
        return
    
    status = person["status"].lower()

    if person["status"].lower() == "revoked":
        print(f"\nThis ID is DENIED/REVOKED: {id_number}")
        return
    
    if person["status"].lower() == "pending":
        print(f"\nThis ID is currently PENDING.")
        display_id(id_number, person)
        return
    
    if status != "approved":
        print("Invalid status. Access denied.")
        return
    
    print(f"\nThis ID is APPROVED.")
    display_id(id_number, person)

# user input 
user_id = input("Enter ID number: ")
identify_id(user_id)