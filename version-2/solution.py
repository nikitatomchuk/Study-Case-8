from datetime import date, timedelta
from random import randint
from constants import RoomTariffs, RoomTypes, FoodTariffs, Files
import ru_local as ru


def format_date(some_date: date):
    return ".".join(some_date.isoformat().split("-")[::-1])


def answer_is_positive():
    number = randint(1, 4)
    if number == 2:
        return True
    return False


class FoodTariff:

    def __init__(self, food_tariff: str, people_count: int):
        self.__food_tariff = food_tariff

        match food_tariff:
            case FoodTariffs.NO_FOOD:
                self.__price_per_day = FoodTariffs.NO_FOOD_PRICE
            case FoodTariffs.BREAKFAST:
                self.__price_per_day = FoodTariffs.BREAKFAST_PRICE * people_count
            case FoodTariffs.FULL:
                self.__price_per_day = FoodTariffs.FULL_PRICE * people_count
            case _:
                print(ru.NO_TARIFF)

    def __repr__(self) -> str:
        return self.__food_tariff

    def get_price_per_day(self) -> int:
        return self.__price_per_day


class RoomType:

    def __init__(self, type: str, people_count: int):
        self.__type = type

        match type:
            case RoomTypes.ONE_PERSON:
                self.__price_per_day = RoomTypes.ONE_PERSON_PRICE
            case RoomTypes.TWO_PERSON:
                self.__price_per_day = RoomTypes.TWO_PERSON_PRICE * people_count
            case RoomTypes.HALF_LUXE:
                self.__price_per_day = RoomTypes.HALF_LUXE_PRICE * people_count
            case RoomTypes.LUXE:
                self.__price_per_day = RoomTypes.LUXE_PRICE * people_count
            case _:
                print(ru.NO_TARIFF)

    def __repr__(self) -> str:
        return self.__type

    def get_price_per_day(self) -> int:
        return self.__price_per_day


class RoomTariff:

    def __init__(self, tariff: str):

        match tariff:
            case RoomTariffs.STANDARD:
                self.__price_scale = RoomTariffs.STANDARD_RATIO
            case RoomTariffs.STANDARD_UP:
                self.__price_scale = RoomTariffs.STANDARD_UP_RATIO
            case RoomTariffs.APARTMENT:
                self.__price_scale = RoomTariffs.APARTMENT_RATIO
            case _:
                print(ru.NO_TARIFF)

    def get_price_scale(self) -> int:
        return self.__price_scale


class Room:

    def __init__(self, room_type: RoomType, room_tariff: RoomTariff, room_number: int, max_people_count: int):
        self.__type = room_type.__repr__()
        self.__busy_dates = {}
        self.__number = room_number
        self.__max_people_count = max_people_count
        self.__price_per_day = room_tariff.get_price_scale() * room_type.get_price_per_day()
        self.__discount_price = self.__price_per_day * 0.7

    def __repr__(self) -> str:
        return str([self.__number, self.__max_people_count, self.__price_per_day])

    def get_type(self) -> str:
        return self.__type

    def get_busy_dates(self) -> dict:
        return self.__busy_dates

    def set_busy_date(self, busy_date_start: date, busy_date_end: date):
        self.__busy_dates.update({busy_date_start: busy_date_end})

    def get_number(self) -> int:
        return self.__number

    def get_price(self) -> int:
        return self.__price_per_day

    def get_max_people_count(self) -> int:
        return self.__max_people_count

    def get_discount_price(self) -> float:
        return self.__discount_price

    def is_free(self, book_start_date: date, book_end_date: date) -> bool:
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


class RoomDataBase:

    def __init__(self, rooms_data_path: str = Files.DATA_FILE_NAME):
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

    def get_all_rooms(self) -> list:
        return self.__all_rooms

    def change_room_busy_date(self, room_number, book_start_day: date, book_end_day: date):
        self.__all_rooms[room_number - 1].set_busy_date(book_start_day, book_end_day)

    def get_room_by_number(self, room_number: int) -> Room:
        return self.__all_rooms[room_number - 1]

    def get_free_rooms(self, book_start_date: date, book_end_date: date) -> list:
        self.__free_rooms = []

        for room in self.__all_rooms:
            if room.is_free(book_start_date, book_end_date):
                self.__free_rooms.append(room)

        return self.__free_rooms


def convert_to_room_type(room: Room):
    return room.get_type()


class Report:

    def __init__(self, room_data_base: RoomDataBase, report_date: date):
        self.__report_date = report_date
        self.__room_data_base = room_data_base
        all_room_types = list(map(convert_to_room_type, room_data_base.get_all_rooms()))
        room_types = set(all_room_types)
        self.__busy_room_types = {room_type: [all_room_types.count(room_type), 0] for room_type in room_types}
        self.__busy_rooms_count = 0
        self.__free_rooms_count = len(room_data_base.get_all_rooms())
        self.__busy_hotel_percent = 0
        self.__alternative_costs = 0
        self.__revenue = 0

    def __str__(self):
        return (f"{ru.REPORT_DATE} {self.get_report_date()}\n\n" +
                f"--{ru.BUSY_ROOMS}: {self.__busy_rooms_count}\n" +
                f"--{ru.FREE_ROOMS}: {self.__free_rooms_count}\n" +
                f"--{ru.WORKLOAD_ROOMS}: {self.get_busy_room_types_percent()}\n" +
                f"--{ru.WORKLOAD_HOTEL}: {self.get_busy_hotel_percent()}%\n" +
                f"--{ru.DAILY_INCOME}: {self.__alternative_costs}\n" +
                f"--{ru.ALTERNATIVE_COSTS}: {self.__revenue}\n\n" +
                f"{ru.REPORT_END}\n" +
                "-" * 30)

    def get_report_date(self) -> str:
        return ".".join(self.__report_date.__str__().split("-")[::-1])

    def change_busy_rooms_count(self, room_number: int):
        self.__busy_rooms_count += 1
        room_type = convert_to_room_type(self.__room_data_base.get_room_by_number(room_number))
        self.__busy_room_types[room_type][1] += 1
        self.__busy_room_types[room_type][0] -= 1

    def change_free_rooms_count(self):
        self.__free_rooms_count -= 1

    def get_busy_room_types_percent(self) -> dict:
        busy_room_types_percent = {room_type: round(self.__busy_room_types[room_type][1]
                                              / (self.__busy_room_types[room_type][1]
                                                 + self.__busy_room_types[room_type][0]), 2)
                                   for room_type in self.__busy_room_types.keys()}
        return busy_room_types_percent

    def get_busy_hotel_percent(self) -> float:
        return round(self.__busy_rooms_count / self.__free_rooms_count, 2)

    def change_revenue(self, revenue: float):
        self.__revenue += revenue

    def change_alternative_costs(self, costs: float):
        self.__alternative_costs += costs


class Reports:

    def __init__(self):
        self.__reports = {}

    def add(self, report: Report):
        self.__reports.update({report.get_report_date(): report})

    def get_all_reports(self) -> list:
        return list(self.__reports.values())

    def print_all_reports(self):
        for report in self.get_all_reports():
            print(report)


class RequestHandler:

    def __init__(self, request: list[str]):
        self.__full_request = request
        self.__full_name = request[1] + " " + request[2] + " " + request[3]
        self.__booking_date = "-".join(request[0].split(".")[::-1])
        self.__booked_date = "-".join(request[5].split(".")[::-1])
        self.__people_count = int(request[4])
        self.__days_count = int(request[6])
        self.__costs_by_one = int(request[7].strip("\n"))

    def __repr__(self) -> str:
        return str(self.__full_request)

    def get_costs_by_one(self) -> int:
        return self.__costs_by_one

    def get_full_available_costs(self) -> int:
        return self.__costs_by_one * self.__days_count

    def get_full_name(self) -> str:
        return self.__full_name

    def get_booking_date(self) -> date:
        return date.fromisoformat(self.__booking_date)

    def get_book_start_date(self) -> date:
        return date.fromisoformat(self.__booked_date)

    def get_book_end_data(self) -> date:
        return self.get_book_start_date() + timedelta(days = self.__days_count)

    def get_people_count(self) -> int:
        return self.__people_count

    def get_days_count(self) -> int:
        return self.__days_count


class RoomSearcher:

    def __init__(self, request: RequestHandler, room_data_base: RoomDataBase):
        self.__min_room_price = Room(RoomType(ru.ONE_PERSON, 1),
                                     RoomTariff(ru.STANDARD),
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
                        for food_tariff in FoodTariffs.NO_FOOD, FoodTariffs.BREAKFAST, FoodTariffs.FULL:
                            total_food_price = FoodTariff(food_tariff,
                                                          people_count).get_price_per_day() * days_count

                            self.__room_data_base.change_room_busy_date(self.__suitable_room,
                                                                        self.__request.get_book_start_date(),
                                                                        self.__request.get_book_end_data())

                            if self.__request.get_full_available_costs() - self.__min_possible_price >= total_food_price:
                                report.change_revenue(self.__min_possible_price + total_food_price)
                                self.__food_tariff = food_tariff
                                self.print_success_booking()
                                report.change_busy_rooms_count(self.__suitable_room)
                                report.change_free_rooms_count()
                                return self.__suitable_room
                    else:
                        report.change_alternative_costs(self.__request.get_full_available_costs())
                        self.print_failed_booking(True)
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
        print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
              f"{ru.SUCCESS_BOOK} {ru.ROOM_NUMBER}{self.__suitable_room} {ru.FROM} "
              f"{format_date(self.__request.get_book_start_date())} {ru.TO} " +
              f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()} {ru.GUESTS} " +
              f"{ru.FOOD_TARIFF} '{self.__food_tariff}'. {ru.REVENUE} {self.__max_possible_price} {ru.CURRENCY}")

    def print_failed_booking(self, answer_is_negative: bool = False):
        if answer_is_negative:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.FAIL}{self.__suitable_room} {ru.FROM} {format_date(self.__request.get_book_start_date())} {ru.TO} " +
                  f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()} {ru.GUESTS}. " +
                  f"{ru.REVENUE} {self.__request.get_full_available_costs()} {ru.CURRENCY}")
        else:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.CANNOT_BOOK} {ru.FROM} {format_date(self.__request.get_book_start_date())} {ru.TO} " +
                  f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()} {ru.GUESTS}. " +
                  f"{ru.LOST_REVENUE} {self.__request.get_full_available_costs()} {ru.CURRENCY}")

    def __compare_people_count(self, days_count, people_count, extra, room):
        if room.get_max_people_count() == people_count + extra:
            room_prices = {}

            for food_tariff in FoodTariffs.NO_FOOD, FoodTariffs.BREAKFAST, FoodTariffs.FULL:
                food = FoodTariff(food_tariff, people_count)

                if extra == 0:
                    final_room_price = room.get_price()
                else:
                    final_room_price = room.get_discount_price()

                room_prices.update({food_tariff: (final_room_price + food.get_price_per_day()) * days_count})

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