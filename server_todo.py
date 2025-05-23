import socket
import json

HOST = "127.0.0.1"  # Localhost
PORT =  8888       # Porta livre

# This class represents a single todo item
class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

# This class represents a list of TodoItems
class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description):
        item = TodoItem(title, description)
        self.items.append(item)

    def complete_item(self, index):
        if (index < 0 or index >= len(self.items)):
            raise IndexError("Invalid index")
        item = self.items[index]
        item.completed = True

    def count_items(self):
        return len(self.items)

    def display_items(self):
        result = ""
        for i, item in enumerate(self.items):
            status = "[ ]"
            if item.completed:
                status = "[x]"
            result += f"{i}. {status} {item.title}: {item.description}\n"
        return result

host = "127.0.0.1"
port = 8888 # port number to listen on

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

todo_list = TodoList()

# Loop forever, waiting for client commands
while True:
    try:
        print("Waiting for connection...")
        client_socket, address = server_socket.accept()
        print(f"Connected to {address}")
        command = client_socket.recv(1024).decode()
        print(f"Received command: {command}")
        choice, data = command.split("-")
        if choice == "1":
            title, description = data.split(",")
            todo_list.add_item(title, description)
            result = "Todo added."
        elif choice == "2":
            result = todo_list.display_items()
        elif choice == "3":
            index = int(data)
            todo_list.complete_item(index)
            result = "Todo completed."
        elif choice == "4":
            result = f"Number of incomplete todos: {todo_list.count_incomplete_items()}"
        else:
            result = "Invalid command."
        print("Logging: " + result)
        client_socket.send(result.encode())
    except ValueError as e:
        result = "Error: Invalid command format."
        print(result)
        if 'client_socket' in locals():
            client_socket.send(result.encode())
    except IndexError as e:
        result = f"Error: {str(e)}"
        print(result)
        if 'client_socket' in locals():
            client_socket.send(result.encode())
    except Exception as e:
        result = f"Error: {str(e)}"
        print(result)
    finally:
        if 'client_socket' in locals():
            client_socket.close()
