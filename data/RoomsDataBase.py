from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType
from data.Room import Room


class RoomDataBase:

    def __init__(self, rooms_data_path: str):
        self.__all_rooms = []
        with open("rooms_data.txt") as lines:
            for line in lines:
                room_data = line.split()
                room_number = int(room_data[0])
                room_max_people_count = int(room_data[2])
                room_type = RoomType(room_data[1], room_max_people_count)
                room_tariff = RoomTariff(room_data[3].strip('\n'))
                room = Room(room_type, room_tariff, room_number, room_max_people_count)
                self.__all_rooms.append(room)

    def get_all_rooms(self):
        return self.__all_rooms

    def get_room_by_number(self, room_number: int):
        return self.__all_rooms[room_number - 1]

    def get_free_rooms(self, date):
        for room in self.__all_rooms:
            pass

