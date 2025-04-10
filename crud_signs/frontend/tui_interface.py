import os
import requests

BASE_URL = "http://127.0.0.1:8000"
token = None

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def auth_header():
    return {"Authorization": f"Bearer {token}"} if token else {}

def login():
    global token
    clear()
    print("=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")
    response = requests.post(f"{BASE_URL}/token", data={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Login successful.\n")
    else:
        print("Login failed:", response.text)
        exit(1)

# ---- CREATE ----
def create_client():
    clear()
    print("=== CREATE NEW CLIENT ===")
    name = input("Client name: ")
    contact = input("Contact info: ")
    response = requests.post(f"{BASE_URL}/clients/", json={
        "name": name,
        "contact_info": contact
    }, headers=auth_header())
    print("Response:", response.json())

def create_order():
    clear()
    print("=== CREATE NEW ORDER ===")
    client_id = input("Client ID: ")
    description = input("Order description: ")
    due_date = input("Due date (YYYY-MM-DDTHH:MM:SS): ")
    response = requests.post(f"{BASE_URL}/orders/", json={
        "client_id": int(client_id),
        "description": description,
        "due_date": due_date
    }, headers=auth_header())
    print("Response:", response.json())

# ---- READ ----
def view_clients():
    clear()
    print("=== CLIENT LIST ===")
    response = requests.get(f"{BASE_URL}/clients/", headers=auth_header())
    clients = response.json()
    for client in clients:
        print(f"[{client['id']}] {client['name']} - {client['contact_info']}")

def view_orders():
    clear()
    print("=== ORDER LIST ===")
    response = requests.get(f"{BASE_URL}/orders/", headers=auth_header())
    orders = response.json()
    for order in orders:
        print(f"[{order['id']}] Client #{order['client_id']} - {order['description']}")

# ---- UPDATE ----
def update_client():
    clear()
    print("=== UPDATE CLIENT ===")
    client_id = input("Client ID: ")
    name = input("New name (leave blank to keep current): ")
    contact = input("New contact (leave blank to keep current): ")
    data = {}
    if name:
        data["name"] = name
    if contact:
        data["contact_info"] = contact
    response = requests.put(f"{BASE_URL}/clients/{client_id}", json=data, headers=auth_header())
    print("Response:", response.json())

def update_order():
    clear()
    print("=== UPDATE ORDER ===")
    order_id = input("Order ID: ")
    description = input("New description (leave blank to keep current): ")
    status = input("New status (leave blank to keep current): ")
    due_date = input("New due date (leave blank to keep current): ")
    data = {}
    if description:
        data["description"] = description
    if status:
        data["status"] = status
    if due_date:
        data["due_date"] = due_date
    response = requests.put(f"{BASE_URL}/orders/{order_id}", json=data, headers=auth_header())
    print("Response:", response.json())

# ---- DELETE ----
def delete_client():
    clear()
    print("=== DELETE CLIENT ===")
    client_id = input("Client ID: ")
    response = requests.delete(f"{BASE_URL}/clients/{client_id}", headers=auth_header())
    print("Response:", response.json())

def delete_order():
    clear()
    print("=== DELETE ORDER ===")
    order_id = input("Order ID: ")
    response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers=auth_header())
    print("Response:", response.json())

# ---- SEARCH ----
def search_clients():
    clear()
    print("=== SEARCH CLIENTS ===")
    query = input("Search term (name contains): ")
    response = requests.get(f"{BASE_URL}/clients/search/", params={"query": query}, headers=auth_header())
    results = response.json()
    for client in results:
        print(f"[{client['id']}] {client['name']} - {client['contact_info']}")

# ---- MENUS ----
def menu():
    while True:
        clear()
        print("ABL DATABASE MANAGEMENT TOOL")
        print("=============================")
        print("1. Create")
        print("2. View")
        print("3. Update")
        print("4. Delete")
        print("5. Search")
        print("6. Exit")
        print()
        choice = input("Select an option: ")

        if choice == "1":
            create_menu()
        elif choice == "2":
            view_menu()
        elif choice == "3":
            update_menu()
        elif choice == "4":
            delete_menu()
        elif choice == "5":
            search_clients()
            input("Press Enter to continue...")
        elif choice == "6":
            exit()
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

def create_menu():
    clear()
    print("=== CREATE MENU ===")
    print("1. New Client")
    print("2. New Order")
    print("3. Back")
    print()
    choice = input("Select an option: ")
    if choice == "1":
        create_client()
    elif choice == "2":
        create_order()
    input("Press Enter to continue...")

def view_menu():
    clear()
    print("=== VIEW MENU ===")
    print("1. View Clients")
    print("2. View Orders")
    print("3. Back")
    print()
    choice = input("Select an option: ")
    if choice == "1":
        view_clients()
    elif choice == "2":
        view_orders()
    input("Press Enter to continue...")

def update_menu():
    clear()
    print("=== UPDATE MENU ===")
    print("1. Update Client")
    print("2. Update Order")
    print("3. Back")
    print()
    choice = input("Select an option: ")
    if choice == "1":
        update_client()
    elif choice == "2":
        update_order()
    input("Press Enter to continue...")

def delete_menu():
    clear()
    print("=== DELETE MENU ===")
    print("1. Delete Client")
    print("2. Delete Order")
    print("3. Back")
    print()
    choice = input("Select an option: ")
    if choice == "1":
        delete_client()
    elif choice == "2":
        delete_order()
    input("Press Enter to continue...")

def main():
    login()
    menu()

if __name__ == "__main__":
    main()
