from data.Report import Report
from data.Reports import Reports
from data.RoomsDataBase import RoomDataBase
from handler.RequestHandler import RequestHandler
from handler.RoomSearcher import RoomSearcher


def main():
    room_data_base = RoomDataBase()
    reports = Reports()
    with open("handler/requests_data.txt", encoding='utf-8') as requests:
        previous_request = requests.readline()
        previous_request_data = RequestHandler(previous_request.split())
        report = Report(room_data_base, previous_request_data.get_booking_date())
        room_searcher = RoomSearcher(previous_request_data, room_data_base)
        room_number = room_searcher.search_suitable_room(report)
        if room_number == 0:
            print("Client has gone...")

        for request in requests.readlines():
            request_data = RequestHandler(request.split())

            if request_data.get_booking_date() == previous_request_data.get_booking_date():
                room_searcher = RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data
            else:
                reports.add(report)
                report = Report(room_data_base, request_data.get_booking_date())
                room_searcher = RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data

        reports.add(report)
        reports.print_all_reports()


if __name__ == "__main__":
    main()