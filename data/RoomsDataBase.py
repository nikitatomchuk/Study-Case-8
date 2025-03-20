from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType
from data.Room import Room
from datetime import date


class RoomDataBase:

    def __init__(self, rooms_data_path: str):
        self.__free_rooms = []
        self.__all_rooms = []
        with open("rooms_data.txt", encoding='utf-8') as lines:
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

    def get_free_rooms(self, target_date: date):
        self.__free_rooms = []

        for room in self.__all_rooms:
            if room.is_free(target_date):
                self.__free_rooms.append(room)

        return self.__free_rooms

    def get_free_room_by_number(self, room_number: int):
        for room in self.__free_rooms:
            if room.get_room_number() == room_number:
                return room

        print("No rooms with such number are free.")
