from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType


class Room:

    def __init__(self, room_type: RoomType, room_tariff: RoomTariff, room_number: int, max_people_count: int):
        self.__room_number = room_number
        self.__max_people_count = max_people_count
        self.__room_price_per_day = room_tariff.get_price_scale() * room_type.get_size_price_per_day()

    def get_room_number(self):
        return self.__room_number

    def get_room_price(self):
        return self.__room_price_per_day

    def get_max_people_count(self):
        return self.__max_people_count
