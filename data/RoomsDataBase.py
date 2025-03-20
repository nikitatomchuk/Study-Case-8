from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType
from data.Room import Room
from datetime import date


class RoomDataBase:

    def __init__(self, rooms_data_path: str = "data/rooms_data.txt"):
        self.__free_rooms = []
        self.__all_rooms = []
        with open(rooms_data_path, encoding='utf-8') as lines:
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

    def change_room_busy_date(self, room_number, book_start_day: date, book_end_day: date):
        self.__all_rooms[room_number - 1].set_busy_date(book_start_day, book_end_day)

    def get_room_by_number(self, room_number: int):
        return self.__all_rooms[room_number - 1]

    def get_free_rooms(self, book_start_date: date, book_end_date: date):
        self.__free_rooms = []

        for room in self.__all_rooms:
            if room.is_free(book_start_date, book_end_date):
                self.__free_rooms.append(room)

        return self.__free_rooms

    def get_free_room_by_number(self, room_number: int):
        for room in self.__free_rooms:
            if room.get_number() == room_number:
                return room

        print("No rooms with such number are free.")
