from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType
from datetime import date


class Room:

    def __init__(self, room_type: RoomType, room_tariff: RoomTariff, room_number: int, max_people_count: int):
        self.__room_type = room_type.__repr__()
        self.__busy_dates = {}
        self.__room_number = room_number
        self.__max_people_count = max_people_count
        self.__room_price_per_day = room_tariff.get_price_scale() * room_type.get_size_price_per_day()
        self.__discount_price = self.__room_price_per_day * 0.7

    def __repr__(self):
        return str([self.__room_number, self.__max_people_count, self.__room_price_per_day])

    def get_type(self):
        return self.__room_type

    def get_busy_dates(self):
        return self.__busy_dates

    def set_busy_date(self, busy_date_start: date, busy_date_end: date):
        self.__busy_dates.update({busy_date_start: busy_date_end})

    def get_number(self):
        return self.__room_number

    def get_price(self):
        return self.__room_price_per_day

    def get_max_people_count(self):
        return self.__max_people_count

    def is_free(self, book_start_date: date, book_end_date: date):
        if len(self.__busy_dates) == 0:
            return True

        for book_start in self.__busy_dates.keys():
            if book_start <= book_start_date <= self.__busy_dates[book_start]:
                return False
            elif book_start <= book_end_date <= self.__busy_dates[book_start]:
                return False
            elif book_start_date < book_start and self.__busy_dates[book_start] < book_end_date:
                return False
        return True

    def get_discount_price(self):
        return self.__discount_price