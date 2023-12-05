# booking_ticket
#################################################################################
class ViewBookingTicket:

    def show_booking_tickets(self, booking_tickets):
        print("Booking Tickets:")
        for booking_ticket in booking_tickets:
            print(
                f"Booking ID: {booking_ticket[0]}, Client ID: {booking_ticket[1]}, Room Number: {booking_ticket[2]}, "
                f"Start Date: {booking_ticket[3]}, End Date: {booking_ticket[4]}, Price: {booking_ticket[5]}")

    def get_booking_ticket_input(self):
        client_id = int(input("Enter client ID: "))
        room_number = int(input("Enter room number: "))
        booking_start_date = input("Enter booking start date (YYYY-MM-DD): ")
        booking_end_date = input("Enter booking end date (YYYY-MM-DD): ")
        price = float(input("Enter booking price: "))
        return client_id, room_number, booking_start_date, booking_end_date, price

    def get_booking_id(self):
        return int(input("Enter booking ID: "))

    def show_booking_ticket_message(self, message):
        print(message)


