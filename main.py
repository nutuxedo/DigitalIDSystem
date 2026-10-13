# id system
# link to Google Sheets

testinfo = {
    "ID-001": {
        "lastname": "Doe",
        "firstname": "John",
        "role": "Band",
        "bandname": "Bucket",
        "status": "approved",
    }
}
# debug test
# print(testinfo)

def identify_id(id_number):
    person = testinfo.get(id_number)
    
    if person is None:
        print(f"No record found for {id_number}")
        return
    
    print(f"\n--- Digital ID: {id_number} ---")
    print(f"Name:   {person['firstname']} {person['lastname']}")
    print(f"Role:   {person['role']}")
    print(f"Band:   {person['bandname']}")
    print(f"Status: {person['status']}")
    print("------------------------------")
    
    
# user input 
user_id = input("Enter ID number: ")
identify_id(user_id)