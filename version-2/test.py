from constants import Files
import solution as s


def main():
    room_data_base = s.RoomDataBase()
    reports = s.Reports()
    with open(Files.REQUESTS_FILE_NAME, encoding = 'utf-8') as requests:
        previous_request = requests.readline()
        previous_request_data = s.RequestHandler(previous_request.split())
        report = s.Report(room_data_base, previous_request_data.get_booking_date())
        room_searcher = s.RoomSearcher(previous_request_data, room_data_base)
        room_searcher.search_suitable_room(report)

        for request in requests.readlines():
            request_data = s.RequestHandler(request.split())

            if request_data.get_booking_date() == previous_request_data.get_booking_date():
                room_searcher = s.RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data
            else:
                reports.add(report)
                report = s.Report(room_data_base, request_data.get_booking_date())
                room_searcher = s.RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data

        reports.add(report)
        print()
        reports.print_all_reports()


if __name__ == "__main__":
    main()