from random import randint
from TariffTypes.FoodTariff import FoodTariff
from data import Report
from data.RoomsDataBase import RoomDataBase
from handler.RequestHandler import RequestHandler


def answer_is_positive():
    number = randint(1, 4)
    if number == 2:
        return True
    return False


class RoomSearcher:

    def __init__(self, request: RequestHandler, room_data_base: RoomDataBase):
        self.__suitable_room = 0
        self.__food_tariff = ""
        self.__max_possible_price = 0
        self.__min_possible_price = 10**100
        self.__request = request
        self.__room_data_base = room_data_base

    def search_suitable_room(self, report: Report):
        free_rooms = self.__room_data_base.get_free_rooms(self.__request.get_book_start_date(),
                                                          self.__request.get_book_end_data())
        days_count = self.__request.get_days_count()
        people_count = self.__request.get_people_count()

        extra = 0
        while people_count + extra <= 6:
            for room in free_rooms:
                self.__compare_people_count(days_count, people_count, extra, room)

            if self.__suitable_room != 0:
                if extra != 0:
                    if answer_is_positive():
                        self.__room_data_base.change_room_busy_date(self.__suitable_room,
                                                                    self.__request.get_book_start_date(),
                                                                    self.__request.get_book_end_data())
                        if (self.__request.get_full_available_costs() - self.__min_possible_price
                                >= FoodTariff("full", people_count).get_food_price_per_day() * days_count):
                            report.change_revenue(self.__min_possible_price +
                                                  FoodTariff("full",
                                                             people_count).get_food_price_per_day() * days_count)
                            self.__food_tariff = "full"
                            return self.__suitable_room

                        elif (self.__request.get_full_available_costs() - self.__min_possible_price
                                >= FoodTariff("breakfast", people_count).get_food_price_per_day() * days_count):
                            report.change_revenue(self.__min_possible_price +
                                                  FoodTariff("breakfast",
                                                             people_count).get_food_price_per_day() * days_count)
                            self.__food_tariff = "breakfast"
                            return self.__suitable_room

                        else:
                            report.change_revenue(self.__min_possible_price)
                            self.__food_tariff = "no"
                            return self.__suitable_room
                    else:
                        report.change_alternative_costs(self.__request.get_full_available_costs())
                        return 0
                else:
                    self.__room_data_base.change_room_busy_date(self.__suitable_room,
                                                                self.__request.get_book_start_date(),
                                                                self.__request.get_book_end_data())
                    report.change_revenue(self.__max_possible_price)
                    return self.__suitable_room

        report.change_alternative_costs(self.__request.get_full_available_costs())
        return 0

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




