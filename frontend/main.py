from ui_menu import show_menu
from backend_connector import run_backend
from display_formatter import show_students

USERNAME="admin"
PASSWORD="1234"

def login():

    u=input("Username: ")
    p=input("Password: ")

    if u==USERNAME and p==PASSWORD:
        return True
    else:
        print("Login failed")
        return False

def add_student():

    roll=input("Roll: ")
    if not roll.isdigit():
        print("Error: Roll must be a number")
        return

    name=input("Name: ")
    cls=input("Class: ")
    contact=input("Contact: ")

    output=run_backend(["add_student",roll,name,cls,contact])

    if output is None:
        print("Error: Failed to add student")
    else:
        print(output.strip())

def view_students():

    data=run_backend(["view_students"])
    if data is None:
        print("Error: Failed to retrieve students")
    else:
        show_students(data)

def search_student():

    roll=input("Enter Roll: ")
    if not roll.isdigit():
        print("Error: Roll must be a number")
        return

    data=run_backend(["search_student",roll])
    if data is None:
        print("Error: Failed to search")
    else:
        print(data.strip())

def main():

    if not login():
        return

    while True:

        show_menu()

        choice=input("Select: ")

        if choice=="1":
            add_student()

        elif choice=="2":
            view_students()

        elif choice=="3":
            search_student()

        elif choice=="4":
            break

if __name__=="__main__":
    main()