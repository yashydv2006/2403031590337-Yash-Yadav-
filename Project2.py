#Contact Book

import json
import os

# ---------------- Node Class (Linked List) ----------------
class ContactNode:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.next = None  # self-referential pointer to next node


# ---------------- Contact Book Class ----------------
class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.head = None
        self.filename = filename
        self.load_from_file()

    # Insert contact alphabetically
    def add_contact(self, name, phone, email=""):
        new_node = ContactNode(name, phone, email)
        if self.head is None or name.lower() < self.head.name.lower():
            new_node.next = self.head
            self.head = new_node
        else:
            prev = None
            curr = self.head
            while curr and name.lower() > curr.name.lower():
                prev = curr
                curr = curr.next
            new_node.next = curr
            prev.next = new_node
        self.save_to_file()

    # Display all contacts
    def display_contacts(self):
        if not self.head:
            print("No contacts found.")
            return
        curr = self.head
        while curr:
            print(f"Name: {curr.name}, Phone: {curr.phone}, Email: {curr.email}")
            curr = curr.next

    # Search contact by name
    def search_contact(self, name):
        curr = self.head
        while curr:
            if curr.name.lower() == name.lower():
                return curr
            curr = curr.next
        return None

    # Update a contact
    def update_contact(self, name, new_phone=None, new_email=None):
        node = self.search_contact(name)
        if node:
            if new_phone:
                node.phone = new_phone
            if new_email:
                node.email = new_email
            self.save_to_file()
            return True
        return False

    # Delete a contact
    def delete_contact(self, name):
        curr = self.head
        prev = None
        while curr:
            if curr.name.lower() == name.lower():
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.save_to_file()
                return True
            prev = curr
            curr = curr.next
        return False

    # Save to file (JSON)
    def save_to_file(self):
        data = []
        curr = self.head
        while curr:
            data.append({"name": curr.name, "phone": curr.phone, "email": curr.email})
            curr = curr.next
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    # Load from file
    def load_from_file(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            try:
                data = json.load(f)
                for contact in sorted(data, key=lambda x: x["name"].lower(), reverse=True):
                    self.add_contact(contact["name"], contact["phone"], contact.get("email", ""))
            except json.JSONDecodeError:
                pass


# ---------------- CLI Menu ----------------
def menu():
    book = ContactBook()
    while True:
        print("\n--- Contact Book ---")
        print("1. Add Contact")
        print("2. Display Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email (optional): ")
            book.add_contact(name, phone, email)
            print("Contact added successfully!")

        elif choice == "2":
            book.display_contacts()

        elif choice == "3":
            name = input("Enter name to search: ")
            contact = book.search_contact(name)
            if contact:
                print(f"Found -> Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")
            else:
                print("Contact not found.")

        elif choice == "4":
            name = input("Enter name to update: ")
            phone = input("New Phone (leave blank to skip): ")
            email = input("New Email (leave blank to skip): ")
            updated = book.update_contact(name, phone if phone else None, email if email else None)
            if updated:
                print("Contact updated successfully!")
            else:
                print("Contact not found.")

        elif choice == "5":
            name = input("Enter name to delete: ")
            deleted = book.delete_contact(name)
            if deleted:
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")

        elif choice == "6":
            print("Exiting Contact Book. Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()
