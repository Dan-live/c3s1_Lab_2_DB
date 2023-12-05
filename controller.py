from model import Model

from Booking.view import ViewBookingTicket
from Booking.model import ModelBookingTicket
from Booking.controller import ControllerBooking

from Client.view import ViewClient
from Client.model import ModelClient
from Client.controller import ControllerClient

from Room.view import ViewRoom
from Room.model import ModelRoom
from Room.controller import ControllerRoom

from Analytics.view import ViewAnalytics
from Analytics.model import ModelAnalytics
from Analytics.controller import ControllerAnalytics


class Controller:
    def __init__(self):
        self.model = Model()
        self.view_booking_ticket = ViewBookingTicket()
        self.view_client = ViewClient()
        self.view_room = ViewRoom()
        self.view_analytics = ViewAnalytics()

        self.model_booking_ticket = ModelBookingTicket(self.model)
        self.model_client = ModelClient(self.model)
        self.model_room = ModelRoom(self.model)
        self.model_analytics = ModelAnalytics(self.model)

        self.controller_booking = ControllerBooking(self.model_booking_ticket, self.view_booking_ticket)
        self.controller_client = ControllerClient(self.model_client, self.view_client)
        self.controller_room = ControllerRoom(self.model_room, self.view_room)
        self.controller_analytics = ControllerAnalytics(self.model_analytics, self.view_analytics)
    def run(self):
        methods = {
            '1': self.controller_booking.add_booking_ticket,
            '2': self.controller_booking.view_booking_tickets,
            '3': self.controller_booking.update_booking_ticket,
            '4': self.controller_booking.delete_booking_ticket,
            '5': self.controller_client.add_client,
            '6': self.controller_client.view_clients,
            '7': self.controller_client.update_client,
            '8': self.controller_client.delete_client,
            '9': self.controller_room.add_room,
            '10': self.controller_room.view_rooms,
            '11': self.controller_room.update_room,
            '12': self.controller_room.delete_room,
            '13': self.generate_rand_data,
            '14': self.truncate_all_tables,
            '15': self.display_analytics
        }

        while True:
            choice = self.show_menu()

            if choice in methods:
                methods[choice]()
            elif choice == '16':
                break

    MENU_OPTIONS = [
        "Add Booking Ticket",
        "View Booking Tickets",
        "Update Booking Ticket",
        "Delete Booking Ticket",
        "Add Client",
        "View Clients",
        "Update Client",
        "Delete Client",
        "Add Room",
        "View Rooms",
        "Update Room",
        "Delete Room",
        "Generate Random Data",
        "Truncate All Tables",
        "Display Analytics",
        "Quit"
    ]

    def show_menu(self):
        self.view_booking_ticket.show_booking_ticket_message("\nMenu:")
        for idx, option in enumerate(self.MENU_OPTIONS, start=1):
            self.view_booking_ticket.show_booking_ticket_message(f"{idx}. {option}")
        return input("Enter your choice: ")

    def create_room_sequence(self):
        self.controller_room.create_room_sequence()

    def generate_rand_room_data(self, number_of_operations):
        self.controller_room.generate_rand_room_data(number_of_operations)

    def create_client_sequence(self):
        self.controller_client.create_client_sequence()

    def generate_rand_client_data(self, number_of_operations):
        self.controller_client.generate_rand_client_data(number_of_operations)

    def create_booking_sequence(self):
        self.controller_booking.create_booking_sequence()

    def generate_rand_booking_ticket_data(self, number_of_operations):
        self.controller_booking.generate_rand_booking_ticket_data(number_of_operations)

    def generate_rand_data(self):
        number_of_operations = int(input("Enter number of operations: "))
        self.create_room_sequence()
        self.generate_rand_room_data(number_of_operations)
        self.create_client_sequence()
        self.generate_rand_client_data(number_of_operations)
        self.create_booking_sequence()
        self.generate_rand_booking_ticket_data(number_of_operations)

    def truncate_all_tables(self):
        if input("Are you sure? Type Yes or No: ") == "Yes":
            self.controller_booking.truncate_booking_table()
            self.controller_client.truncate_client_table()
            self.controller_room.truncate_room_table()
        else:
            print("Ok")

    def display_analytics(self):
        self.controller_analytics.room_occupancy()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.controller_analytics.number_of_orders()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.controller_analytics.client_analytics()