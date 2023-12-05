# ViewRoom
#################################################################################
class ViewRoom:
    def show_rooms(self, rooms):
        print("Rooms:")
        for room in rooms:
            print(f"Room Number: {room[0]}, Room Type: {room[1]}")

    def get_room_input(self):
        room_type = input("Enter room type: ")
        return room_type

    def get_room_number(self):
        return int(input("Enter room number: "))

    def show_room_message(self, message):
        print(message)


