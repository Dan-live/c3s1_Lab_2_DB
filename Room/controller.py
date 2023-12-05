# ControllerRoom
############################################################################
class ControllerRoom:
    def __init__(self, model_room, view_room):
        self.model_room = model_room
        self.view_room = view_room

    def add_room(self):
        # Requesting room data from the user

        room_number = self.view_room.get_room_number()
        room_type = self.view_room.get_room_input()

        if self.model_room.add_room(room_number, room_type):
            self.view_room.show_room_message("Room added successfully!")
        else:
            self.view_room.show_room_message("Failed to add room.")

    def view_rooms(self):
        # Call a method from the Model class to get all the rooms
        rooms = self.model_room.get_all_rooms()

        # Display rooms via a method from the ViewRoom class (assuming you have such a class)
        self.view_room.show_rooms(rooms)

    def update_room(self):
        # Request the number of the room to be updated
        room_number = self.view_room.get_room_number()

        # Check if there is a room with the specified number
        room_exists = self.model_room.check_room_existence(room_number)

        if room_exists:
            # Request updated room data from the user
            room_type = self.view_room.get_room_input()

            # Call a method from the Model class to update the room
            success = self.model_room.update_room(room_number, room_type)

            # Display a message about the result of the operation
            if success:
                self.view_room.show_room_message("Room updated successfully!")
            else:
                self.view_room.show_room_message("Failed to update room.")
        else:
            self.view_room.show_room_message("Room with the specified number does not exist.")

    def delete_room(self):
        # Request the number of the room to be deleted
        room_number = self.view_room.get_room_number()

        # Check if there is a room with the specified number
        room_exists = self.model_room.check_room_existence(room_number)

        if room_exists:
            # Call a method from the Model class to delete a room
            success = self.model_room.delete_room(room_number)

            # Display a message about the result of the operation
            if success:
                self.view_room.show_room_message("Room deleted successfully!")
            else:
                self.view_room.show_room_message("Failed to delete room.")
        else:
            self.view_room.show_room_message("Room with the specified number does not exist.")

    def create_room_sequence(self):
        # Call method create_room_sequence from class ModelRoom
        self.model_room.create_room_sequence()
        self.view_room.show_room_message("Room sequence created successfully!")

    def generate_rand_room_data(self, number_of_operations):
        # Call the generate_rand_room_data method from the ModelRoom class
        success = self.model_room.generate_rand_room_data(number_of_operations)

        if success:
            self.view_room.show_room_message(f"{number_of_operations} rooms generated successfully!")
        else:
            self.view_room.show_room_message("Failed to generate rooms.")

    def truncate_room_table(self):
        # Call the method of the corresponding model
        success = self.model_room.truncate_room_table()

        if success:
            self.view_room.show_room_message("All rooms data truncated successfully!")
        else:
            self.view_room.show_room_message("Failed to truncate room data.")