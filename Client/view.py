
# client
#################################################################################
class ViewClient:
    def show_clients(self, clients):
        print("Clients:")
        for client in clients:
            print(f"ID: {client[0]}, Name: {client[1]}, Surname: {client[2]}, Email: {client[3]}")

    def get_client_input(self):
        name = input("Enter client name: ")
        surname = input("Enter client surname: ")
        email = input("Enter client email: ")
        return name, surname, email

    def get_client_id(self):
        return int(input("Enter client id: "))

    def show_client_message(self, message):
        print(message)
