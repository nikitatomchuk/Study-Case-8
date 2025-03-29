from datetime import date, timedelta
from random import randint

import ru_local as ru
from constants import RoomTariffs, RoomTypes, FoodTariffs, Files


def format_date(some_date: date):
    """
    This function helps present any date in a familiar format.
    :param some_date: date
    :return: string format of date
    """
    return ".".join(some_date.isoformat().split("-")[::-1])


def answer_is_positive():
    """
    This function realise a principe of 0,25% probabilities get approval
    :return: True or False
    """
    number = randint(1, 4)
    if number == 2:
        return False
    return True


class FoodTariff:
    """
    This class calculates the cost with meals for all people

    Attributes:
        __food_tariff: The protected attribute responsible for the pricing plan
        __price_per_day: The protected attribute responsible for calculate the day cost

    Methods:
        get_price_per_day: Allows you to get information about the cost of meals per day
        __repr__: A magic method for string representation
    """
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
    """
    This class calculates the cost with room type for all people

    Attributes:
        __r_type: The protected attribute responsible for room type
        __price_per_day: The protected attribute responsible for calculate the day cost

    Methods:
        get_price_per_day: Allows you to get information about the cost of living per day
        __repr__: A magic method for string representation
    """

    def __init__(self, r_type: str, people_count: int):
        self.__r_type = r_type

        match r_type:
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
        return self.__r_type

    def get_price_per_day(self) -> int:
        return self.__price_per_day


class RoomTariff:
    """
    This class calculates the cost with upgrade for all people

    Attributes:
        __tariff: The protected attribute responsible for upgrade level
        __price_scale: The protected attribute responsible for calculate the margin ratio

    Methods:
        get_price_scale: Allows you to get information about the margin ratio
        __repr__: A magic method for string representation
    """

    def __init__(self, tariff: str):
        self.__tariff = tariff

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

    def __repr__(self) -> str:
        return self.__tariff


class Room:
    """
    This class represented information about room

    Attributes:
        __type: The protected attribute responsible for room type
        __busy_dates: The protected attribute responsible for busy dates for room
        __number: The protected attribute responsible for room number
        __max_people_count: The protected attribute responsible for maximum placement of people
        __price_per_day: The protected attribute responsible for total room price
        __discount_price: The protected attribute responsible for total room price with sale

    Methods:
        get_type: Allows get information about type
        get_busy_dates: Allows get information about busy dates
        set_busy_date: Setting busy day for this room
        get_number: Allows get information about number
        get_price: Allows get information about price
        get_max_people_count: Allows get information about maximum placement of people
        get_discount_price: Allows get information about discount price
        is_free: Checking available of room for date period
        __repr__: A magic method for string representation
    """

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
    """
    This class represents a database of hotel rooms

    Attributes:
    __free_rooms: Represent information of free rooms
    __all_rooms: Represent information of all rooms in the database

    Methods:
    get_all_rooms: Returns a list of all rooms
    change_room_busy_date: Changes the busy dates for a specified room
    get_room_by_number: Retrieves a room by its number
    get_free_rooms: Returns a list of free rooms for a specified date range
    """

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
    """
    This function convert to room type
    :return: string information about room
    """
    return room.get_type()


class Report:
    """
    This class represents a report for the hotel room database

    Attributes:
    __report_date: The date the report is generated
    __room_data_base: An instance of the RoomDataBase class
    __busy_room_types: A dictionary of room types and their busy status
    __busy_rooms_count: Count of currently busy rooms
    __free_rooms_count: Count of currently free rooms
    __busy_hotel_percent: Percentage of the hotel that is busy
    __alternative_costs: Costs that can be considered as alternate income
    __revenue: Total revenue from bookings

    Methods:
    __str__: Returns a string representation of the report
    get_report_date: Formats and returns the report date
    change_busy_rooms_count: Updates the count of busy rooms for a specific room number
    change_free_rooms_count: Decrements the count of free rooms
    get_busy_room_types_percent: Returns the percentage of busy rooms for each room type
    get_busy_hotel_percent: Calculates and returns the busy percentage of the hotel
    change_revenue: Increases the total revenue by a specified amount
    change_alternative_costs: Increases the alternative costs by a specified amount
    """

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
                "-" * 100)

    def get_report_date(self) -> str:
        return ".".join(self.__report_date.__str__().split("-")[::-1])

    def change_busy_rooms_count(self, room_number: int):
        self.__busy_rooms_count += 1
        room_type = convert_to_room_type(self.__room_data_base.get_room_by_number(room_number))
        self.__busy_room_types[room_type][1] += 1
        self.__busy_room_types[room_type][0] -= 1

    def change_free_rooms_count(self):
        self.__free_rooms_count -= 1

    def get_busy_room_types_percent(self) -> str:
        busy_room_types_percent = [f'{room_type}: {round(self.__busy_room_types[room_type][1]
                                                         / (self.__busy_room_types[room_type][1]
                                                            + self.__busy_room_types[room_type][0]), 2)}%'
                                   for room_type in self.__busy_room_types.keys()]
        return ', '.join(busy_room_types_percent)

    def get_busy_hotel_percent(self) -> float:
        return round(self.__busy_rooms_count / self.__free_rooms_count, 2)

    def change_revenue(self, revenue: float):
        self.__revenue += revenue

    def change_alternative_costs(self, costs: float):
        self.__alternative_costs += costs


class Reports:
    """
    This class manages multiple reports for the hotel room database

    Attributes:
    __reports: A dictionary to store reports with report dates as keys

    Methods:
    add: Adds a new report to the collection
    get_all_reports: Returns a list of all reports
    print_all_reports: Prints all reports in the collection
    """
    def __init__(self):
        self.__reports = {}

    def add(self, report: Report):
        self.__reports.update({report.get_report_date(): report})

    def get_all_reports(self) -> list:
        return list(self.__reports.values())

    def print_all_reports(self):
        print("-" * 100)
        for report in self.get_all_reports():
            print(report)


class RequestHandler:
    """
    This class processes booking requests for hotel rooms.

    Attributes:
    full_request: The complete booking request as a list of strings.
    __full_name: The full name of the person making the request.
    __booking_date: The date of booking in a formatted string.
    __booked_date: The date when the booking starts, formatted.
    __people_count: The number of people to accommodate.
    __days_count: The number of days for the booking.
    __costs_by_one: The cost per person or room.

    Methods:
    __repr__:  A magic method for string representation
    get_costs_by_one: Returns the cost per person or room
    get_full_avlble_costs: Returns the total costs for all days based on the per-person cost
    get_full_name: Returns the full name of the person making the request.
    get_booking_date: Returns the booking date as a date object.
    get_book_start_date: Returns the starting date of the booking as a date object.
    get_book_end_data: Calculates and returns the end date of the booking as a date object.
    get_people_count: Returns the number of people to accommodate.
    get_days_count: Returns the number of days for the booking.
    """

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

    def get_full_avlble_costs(self) -> int:
        return self.__costs_by_one * self.__days_count

    def get_full_name(self) -> str:
        return self.__full_name

    def get_booking_date(self) -> date:
        return date.fromisoformat(self.__booking_date)

    def get_book_start_date(self) -> date:
        return date.fromisoformat(self.__booked_date)

    def get_book_end_data(self) -> date:
        return self.get_book_start_date() + timedelta(days=self.__days_count)

    def get_people_count(self) -> int:
        return self.__people_count

    def get_days_count(self) -> int:
        return self.__days_count


class RoomSearcher:
    """
    This class searches for suitable hotel rooms based on booking requests

    Attributes:
    __min_room_price: The minimum price for a room based on room type and tariff
    __suitable_room: The number of the suitable room found
    __purchase_price: The final purchase price for the booking
    __food_tariff: The food service option selected for the booking
    __max_possible_price: The maximum price that meets the booking request
    __min_possible_price: The minimum price set to a very high value initially
    __request: The booking request to be processed
    __room_data_base: The database containing information about rooms

    Methods:
    search_suitable_room: Looks for free rooms that match the booking criteria and checks for food options
    print_success_booking: Outputs a success message with booking details, including discounts if applicable
    print_failed_booking: Outputs a failure message with booking details
    __compare_people_count: Compares the number of people with the room's capacity and determines suitable pricing
    """

    def __init__(self, request: RequestHandler, room_data_base: RoomDataBase):
        self.__min_room_price = Room(RoomType(ru.ONE_PERSON, 1),
                                     RoomTariff(ru.STANDARD),
                                     0,
                                     1).get_price()
        self.__suitable_room = 0
        self.__purchase_price = 0
        self.__food_tariff = ""
        self.__max_possible_price = 0
        self.__min_possible_price = 10 ** 10
        self.__request = request
        self.__room_data_base = room_data_base

    def search_suitable_room(self, report: Report):
        free_rooms = self.__room_data_base.get_free_rooms(self.__request.get_book_start_date(),
                                                          self.__request.get_book_end_data())
        days_count = self.__request.get_days_count()
        people_count = self.__request.get_people_count()

        if self.__request.get_full_avlble_costs() < self.__min_room_price:
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

                            if self.__request.get_full_avlble_costs() - self.__min_possible_price >= total_food_price:
                                report.change_revenue(self.__min_possible_price + total_food_price)
                                self.__food_tariff = food_tariff
                                self.print_success_booking(True)
                                report.change_busy_rooms_count(self.__suitable_room)
                                report.change_free_rooms_count()
                                return self.__suitable_room
                    else:
                        report.change_alternative_costs(self.__request.get_full_avlble_costs())
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
        report.change_alternative_costs(self.__request.get_full_avlble_costs())
        self.print_failed_booking()
        return 0

    def print_success_booking(self, discount: bool = False):
        if discount:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.DISCOUNT_BOOK} {ru.ROOM_NUMBER}{self.__suitable_room} {ru.FROM} "
                  f"{format_date(self.__request.get_book_start_date())} {ru.TO} " +
                  f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()}" +
                  f"{ru.GUESTS} {ru.FOOD_TARIFF} '{self.__food_tariff}'. {ru.REVENUE} {self.__max_possible_price} " +
                  f"{ru.CURRENCY}")
        else:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.SUCCESS_BOOK} {ru.ROOM_NUMBER}{self.__suitable_room} {ru.FROM} "
                  f"{format_date(self.__request.get_book_start_date())} {ru.TO} " +
                  f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()}" +
                  f"{ru.GUESTS} {ru.FOOD_TARIFF} '{self.__food_tariff}'. {ru.REVENUE} {self.__max_possible_price} " +
                  f" {ru.CURRENCY}")
        print("-" * 180)

    def print_failed_booking(self, answer_is_negative: bool = False):
        if answer_is_negative:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.FAIL} {self.__suitable_room} {ru.FROM} {format_date(self.__request.get_book_start_date())}" +
                  f"{ru.TO} {format_date(self.__request.get_book_end_data())} " +
                  f"{ru.ON} {self.__request.get_people_count()} {ru.GUESTS}. " +
                  f"{ru.REVENUE} {self.__request.get_full_avlble_costs()} {ru.CURRENCY}")
        else:
            print(f"{format_date(self.__request.get_booking_date())}: {ru.CLIENT} '{self.__request.get_full_name()}' " +
                  f"{ru.CANNOT_BOOK} {ru.FROM} {format_date(self.__request.get_book_start_date())} {ru.TO} " +
                  f"{format_date(self.__request.get_book_end_data())} {ru.ON} {self.__request.get_people_count()} " +
                  f" {ru.GUESTS}. {ru.LOST_REVENUE} {self.__request.get_full_avlble_costs()} {ru.CURRENCY}")
        print("-" * 180)

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
                    if price <= self.__request.get_full_avlble_costs():

                        if self.__max_possible_price < price:
                            self.__suitable_room = room.get_number()
                            self.__max_possible_price = price
                            self.__food_tariff = food_tariff
                else:
                    if price <= self.__request.get_full_avlble_costs():

                        if self.__min_possible_price > price:
                            self.__suitable_room = room.get_number()
                            self.__max_possible_price = price
                            self.__food_tariff = food_tariff
