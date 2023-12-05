# booking_ticket
#################################################################################
class ViewAnalytics:
    def display_room_occupancy(self, room_occupancy_data):
        print("Найбільша зайнятість номерів:")
        for row in room_occupancy_data:
            max, room_number, occupancy_count = row
            print(f"Max: {max}, Номер {room_number}: {occupancy_count} бронювань")

    def display_number_of_orders(self, number_of_orders_data):
        print("Кількість замовлень на номери:")
        for row in number_of_orders_data:
            room_number, orders_count = row
            print(f"Номер {room_number}: {orders_count} замовлень")

    def display_client_analytics(self, client_analytics_data):
        print("Аналітика найбільш активних клієнтів :")
        for row in client_analytics_data:
            max, client_id, name, surname, email, booking_count = row
            print(
                f"Max: {max} ,Клієнт ID: {client_id}, Ім'я: {name}, Прізвище: {surname}, Email: {email}, Кількість бронювань: {booking_count}")