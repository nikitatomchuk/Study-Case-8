from datetime import date
from random import randint
from TariffTypes.FoodTariff import FoodTariff
from TariffTypes.RoomTariff import RoomTariff
from TariffTypes.RoomType import RoomType
from data import Report
from data.Room import Room
from data.RoomsDataBase import RoomDataBase
from handler.RequestHandler import RequestHandler


def format_date(some_date: date):
    return ".".join(some_date.isoformat().split("-")[::-1])


def answer_is_positive():
    number = randint(1, 4)
    if number == 2:
        return True
    return False


class RoomSearcher:

    def __init__(self, request: RequestHandler, room_data_base: RoomDataBase):
        self.__min_room_price = Room(RoomType("одноместный", 1),
                                     RoomTariff("стандарт"),
                                     0,
                                     1).get_price()
        self.__suitable_room = 0
        self.__purchase_price = 0
        self.__food_tariff = ""
        self.__max_possible_price = 0
        self.__min_possible_price = 10**10
        self.__request = request
        self.__room_data_base = room_data_base

    def search_suitable_room(self, report: Report):
        free_rooms = self.__room_data_base.get_free_rooms(self.__request.get_book_start_date(),
                                                          self.__request.get_book_end_data())
        days_count = self.__request.get_days_count()
        people_count = self.__request.get_people_count()

        if self.__request.get_full_available_costs() < self.__min_room_price:
            self.__suitable_room = 0
            self.print_failed_booking()
            return 0

        extra = 0
        while people_count + extra <= 6:
            for room in free_rooms:
                self.__compare_people_count(days_count, people_count, extra, room)

            if self.__suitable_room != 0:
                if extra != 0:
                    if answer_is_positive():
                        for food_tariff in "full", "breakfast", "no":
                            total_food_price = FoodTariff(food_tariff,
                                                          people_count).get_food_price_per_day() * days_count

                            self.__room_data_base.change_room_busy_date(self.__suitable_room,
                                                                        self.__request.get_book_start_date(),
                                                                        self.__request.get_book_end_data())

                            if self.__request.get_full_available_costs() - self.__min_possible_price >= total_food_price:
                                report.change_revenue(self.__min_possible_price + total_food_price)
                                self.__food_tariff = food_tariff
                                self.print_success_booking()
                                report.change_busy_rooms_count()
                                report.change_free_rooms_count()
                                return self.__suitable_room
                    else:
                        report.change_alternative_costs(self.__request.get_full_available_costs())
                        print("Client relay from booking.", end = " ")
                        self.print_failed_booking()
                        return 0
                else:
                    self.__room_data_base.change_room_busy_date(self.__suitable_room,
                                                                self.__request.get_book_start_date(),
                                                                self.__request.get_book_end_data())
                    report.change_revenue(self.__max_possible_price)
                    self.print_success_booking()
                    report.change_busy_rooms_count(self.__suitable_room)
                    report.change_free_rooms_count()
                    return self.__suitable_room
            else:
                extra += 1
        report.change_alternative_costs(self.__request.get_full_available_costs())
        self.print_failed_booking()
        return 0

    def print_success_booking(self):
        print(f"{format_date(self.__request.get_booking_date())}: {self.__request.get_full_name()} " +
              f"booked room №{self.__suitable_room} from {format_date(self.__request.get_book_start_date())} to " +
              f"{format_date(self.__request.get_book_end_data())} for {self.__request.get_people_count()} people " +
              f"with food tariff: '{self.__food_tariff}'. Sum paid: {self.__max_possible_price}.")

    def print_failed_booking(self):
        print(f"{format_date(self.__request.get_booking_date())}: {self.__request.get_full_name()} " +
              f"couldn't book a room from {format_date(self.__request.get_book_start_date())} to " +
              f"{format_date(self.__request.get_book_end_data())} for {self.__request.get_people_count()} people. " +
              f"Potential revenue lost: {self.__request.get_full_available_costs()}.")

    def __compare_people_count(self, days_count, people_count, extra, room):
        if room.get_max_people_count() == people_count + extra:
            room_prices = {}

            for food_tariff in "no", "breakfast", "full":
                food = FoodTariff(food_tariff, people_count)

                if extra == 0:
                    final_room_price = room.get_price()
                else:
                    final_room_price = room.get_discount_price()

                room_prices.update({food_tariff: (final_room_price + food.get_food_price_per_day()) * days_count})

            for food_tariff in room_prices.keys():
                price = room_prices[food_tariff]

                if extra == 0:
                    if price <= self.__request.get_full_available_costs():

                        if self.__max_possible_price < price:
                            self.__suitable_room = room.get_number()
                            self.__max_possible_price = price
                            self.__food_tariff = food_tariff
                else:
                    if price <= self.__request.get_full_available_costs():

                        if self.__min_possible_price > price:
                            self.__suitable_room = room.get_number()
                            self.__max_possible_price = price
                            self.__food_tariff = food_tariff




