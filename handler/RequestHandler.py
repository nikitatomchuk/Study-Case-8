from datetime import date


class RequestHandler:

    def __init__(self, request: list[str]):
        self.__full_request = request
        self.__full_name = request[1:4]
        self.__booking_date = "-".join(request[0].split(".")[::-1])
        self.__booked_date = "-".join(request[5].split(".")[::-1])
        self.__people_count = request[4]
        self.__days_count = request[6]
        self.__costs_by_one = request[7].strip("\n")

    def __repr__(self):
        return str(self.__full_request)

    def get_full_name(self):
        return self.__full_name

    def get_booking_date(self):
        return date.fromisoformat(self.__booking_date)

    def get_booked_date(self):
        return date.fromisoformat(self.__booked_date)

    def get_people_count(self):
        return self.__people_count

    def get_days_count(self):
        return self.__days_count

    def get_costs_by_one(self):
        return self.__costs_by_one
