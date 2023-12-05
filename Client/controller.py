# ControllerClient
############################################################################
class ControllerClient:
    def __init__(self, model_client, view_client):
        self.model_client = model_client
        self.view_client = view_client

    def add_client(self):
        client_id = self.view_client.get_client_id()
        name, surname, email = self.view_client.get_client_input()
        if self.model_client.add_client(client_id, name, surname, email):
            self.view_client.show_client_message("Client added successfully!")
        else:
            self.view_client.show_client_message("Failed to add client.")

    def view_clients(self):
        clients = self.model_client.get_all_clients()
        self.view_client.show_clients(clients)

    def update_client(self):
        # Request the ID of the reservation to be updated
        client_id = self.view_client.get_client_id()

        # Check if there is a reservation with the specified ID
        client_exists = self.model_client.check_client_existence(client_id)

        if client_exists:
            # Request updated client data from the user
            name, surname, email = self.view_client.get_client_input()
            # Call a method from the Model class to update the client
            success = (self.model_client.update_client(client_id, name, surname, email))

            # Display a message about the result of the operation
            if success:
                self.view_client.show_client_message("Client updated successfully!")
            else:
                self.view_client.show_client_message("Failed to update client.")
        else:
            self.view_client.show_client_message("Client with the specified ID does not exist.")

    def delete_client(self):
        client_id = self.view_client.get_client_id()

        # Check if there is a reservation with the specified ID
        client_exists = self.model_client.check_client_existence(client_id)

        if client_exists:
            if self.model_client.delete_client(client_id):
                self.view_client.show_client_message("Client deleted successfully!")
            else:
                self.view_client.show_client_message("Failed to delete client.")
        else:
            self.view_client.show_client_message("Client with the specified ID does not exist.")

    def create_client_sequence(self):
        # Call the create_client_sequence method from the ModelClient class
        self.model_client.create_client_sequence()
        self.view_client.show_client_message("Client sequence created successfully!")

    def generate_rand_client_data(self, number_of_operations):
        # Call the generate_rand_client_data method from the ModelClient class
        success = self.model_client.generate_rand_client_data(number_of_operations)

        if success:
            self.view_client.show_client_message(f"{number_of_operations} clients generated successfully!")
        else:
            self.view_client.show_client_message("Failed to generate clients.")

    def truncate_client_table(self):
        # Call the method of the corresponding model
        success = self.model_client.truncate_client_table()

        if success:
            self.view_client.show_client_message("All client data truncated successfully!")
        else:
            self.view_client.show_client_message("Failed to truncate client data.")