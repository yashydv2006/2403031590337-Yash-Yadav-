#Chat Message History Manager

import time
from collections import deque

# ---------------- Message Class ----------------
class Message:
    def __init__(self, text):
        self.text = text
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"[{self.timestamp}] {self.text}"


# ---------------- Chat Manager ----------------
class ChatManager:
    def __init__(self):
        self.messages = deque()     # queue for sent messages
        self.undo_stack = []        # stack for undone messages
        self.redo_stack = []        # stack for redo messages

    # Send (enqueue) a message
    def send_message(self, text):
        msg = Message(text)
        self.messages.append(msg)
        self.undo_stack.append(("send", msg))
        self.redo_stack.clear()  # clear redo history on new action
        print(f"Sent: {msg}")

    # Undo last action (send or delete)
    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        action, msg = self.undo_stack.pop()
        if action == "send":
            if msg in self.messages:
                self.messages.remove(msg)
            self.redo_stack.append(("send", msg))
            print(f"Undo send: {msg}")
        elif action == "delete":
            self.messages.append(msg)
            self.redo_stack.append(("delete", msg))
            print(f"Undo delete: {msg}")

    # Redo last undone action
    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        action, msg = self.redo_stack.pop()
        if action == "send":
            self.messages.append(msg)
            self.undo_stack.append(("send", msg))
            print(f"Redo send: {msg}")
        elif action == "delete":
            if msg in self.messages:
                self.messages.remove(msg)
            self.undo_stack.append(("delete", msg))
            print(f"Redo delete: {msg}")

    # Delete a message (simulate recall)
    def delete_message(self, index):
        if 0 <= index < len(self.messages):
            msg = list(self.messages)[index]
            self.messages.remove(msg)
            self.undo_stack.append(("delete", msg))
            self.redo_stack.clear()
            print(f"Deleted: {msg}")
        else:
            print("Invalid message index.")

    # Show chat history
    def show_messages(self):
        if not self.messages:
            print("No messages in chat.")
            return
        print("\n--- Chat History ---")
        for i, msg in enumerate(self.messages):
            print(f"{i}. {msg}")
        print("-------------------\n")


# ---------------- CLI Menu ----------------
def menu():
    chat = ChatManager()
    while True:
        print("1. Send Message")
        print("2. Show Messages")
        print("3. Delete Message")
        print("4. Undo")
        print("5. Redo")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            text = input("Enter message: ")
            chat.send_message(text)
        elif choice == "2":
            chat.show_messages()
        elif choice == "3":
            chat.show_messages()
            idx = int(input("Enter message index to delete: "))
            chat.delete_message(idx)
        elif choice == "4":
            chat.undo()
        elif choice == "5":
            chat.redo()
        elif choice == "6":
            print("Exiting Chat Manager.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()
