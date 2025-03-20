from datetime import date

from data.RoomsDataBase import RoomDataBase


class Report:

    def __init__(self, room_data_base: RoomDataBase, report_date: date):
        self.__report_date = report_date
        self.__busy_rooms_count = 0
        self.__free_rooms_count = len(room_data_base.get_all_rooms())
        self.__busy_room_types_percent = {"одноместный": 0,
                                          "двухместный": 0,
                                          "полулюкс": 0,
                                          "люкс": 0}
        self.__busy_hotel_percent = 0
        self.__alternative_costs = 0
        self.__revenue = 0

    def __repr__(self):
        return (f"Дата отчета: {self.__busy_rooms_count}\n\n" +
                f"--количество занятых номеров: {self.__busy_rooms_count}\n" +
                f"--количество свободных номеров: {self.__free_rooms_count}\n" +
                f"--процент загруженности отдельных категорий номеров: {self.__busy_room_types_percent}\n" +
                f"--процент загруженности гостинницы в целом: {self.get_busy_hotel_percent()}%\n" +
                f"--полученный доход за день: {self.__alternative_costs}\n" +
                f"--упущенный доход: {self.__revenue}\n\n" +
                "Конец отчета.")

    def set_report_date(self, report_date: date):
        self.__report_date = report_date

    def change_busy_rooms_count(self):
        self.__busy_rooms_count += 1

    def change_free_rooms_count(self):
        self.__busy_rooms_count += 1

    def get_busy_room_types_percent(self):
        return self.__busy_room_types_percent

    def get_busy_hotel_percent(self):
        return round(self.__busy_rooms_count / self.__free_rooms_count, 2)

    def change_revenue(self, revenue: float):
        self.__revenue += revenue

    def change_alternative_costs(self, costs: float):
        self.__alternative_costs += costs

