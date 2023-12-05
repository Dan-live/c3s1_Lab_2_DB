# ControllerBooking
############################################################################
class ControllerBooking:
    def __init__(self, model_booking_ticket, view_booking_ticket):
        self.model_booking_ticket = model_booking_ticket
        self.view_booking_ticket = view_booking_ticket

    def add_booking_ticket(self):
        # Request the ID of the reservation to be updated
        booking_id = self.view_booking_ticket.get_booking_id()

        client_id, room_number, booking_start_date, booking_end_date, price = (
            self.view_booking_ticket.get_booking_ticket_input())
        # Call a method from the Model class to add a reservation
        success = (self.model_booking_ticket.add_booking_ticket
                   (booking_id, client_id, room_number, booking_start_date, booking_end_date, price))

        # Display a message about the result of the operation
        if success:
            self.view_booking_ticket.show_booking_ticket_message("Booking added successfully!")
        else:
            self.view_booking_ticket.show_booking_ticket_message("Failed to add booking.")

    def view_booking_tickets(self):
        # Call a method from the Model class to retrieve all reservations
        booking_tickets = self.model_booking_ticket.get_all_booking_tickets()

        # Display reservations via a method from the View class
        self.view_booking_ticket.show_booking_tickets(booking_tickets)

    def update_booking_ticket(self):
        # Request the ID of the reservation to be updated
        booking_id = self.view_booking_ticket.get_booking_id()

        # Check if there is a reservation with the specified ID
        booking_exists = self.model_booking_ticket.check_booking_existence(booking_id)

        if booking_exists:
            # Request updated booking details from the user
            client_id, room_number, booking_start_date, booking_end_date, price = (
                self.view_booking_ticket.get_booking_ticket_input())
            # Call a method from the Model class to update the reservation
            success = (self.model_booking_ticket.update_booking_ticket
                       (booking_id, client_id, room_number, booking_start_date, booking_end_date, price))

            # Display a message about the result of the operation
            if success:
                self.view_booking_ticket.show_booking_ticket_message("Booking updated successfully!")
            else:
                self.view_booking_ticket.show_booking_ticket_message("Failed to update booking.")
        else:
            self.view_booking_ticket.show_booking_ticket_message("Booking with the specified ID does not exist.")

    def delete_booking_ticket(self):
        # Request the ID of the reservation to be deleted
        booking_id = self.view_booking_ticket.get_booking_id()

        # Check if there is a reservation with the specified ID
        booking_exists = self.model_booking_ticket.check_booking_existence(booking_id)

        if booking_exists:
            # Call a method from the Model class to delete a reservation
            success = self.model_booking_ticket.delete_booking_ticket(booking_id)

            # Display a message about the result of the operation
            if success:
                self.view_booking_ticket.show_booking_ticket_message("Booking deleted successfully!")
            else:
                self.view_booking_ticket.show_booking_ticket_message("Failed to delete booking.")
        else:
            self.view_booking_ticket.show_booking_ticket_message("Booking with the specified ID does not exist.")

    def create_booking_sequence(self):
        # Call method create_booking_sequence from class ModelBookingTicket
        self.model_booking_ticket.create_booking_sequence()
        self.view_booking_ticket.show_booking_ticket_message("Booking sequence created successfully!")

    def generate_rand_booking_ticket_data(self, number_of_operations):
        # Call method generate_rand_booking_ticket_data from class ModelBookingTicket
        success = self.model_booking_ticket.generate_rand_booking_ticket_data(number_of_operations)

        if success:
            self.view_booking_ticket.show_booking_ticket_message(
                f"{number_of_operations} booking tickets generated successfully!")
        else:
            self.view_booking_ticket.show_booking_ticket_message("Failed to generate booking tickets.")

    def truncate_booking_table(self):
        # Call the method of the corresponding model
        success = self.model_booking_ticket.truncate_booking_table()

        if success:
            self.view_booking_ticket.show_booking_ticket_message("All booking tickets truncated successfully!")
        else:
            self.view_booking_ticket.show_booking_ticket_message("Failed to truncate booking tickets data.")