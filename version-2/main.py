from constants import Files
import solution


def main():
    room_data_base = solution.RoomDataBase()
    reports = solution.Reports()
    with open(Files.REQUESTS_FILE_NAME, encoding = 'utf-8') as requests:
        previous_request = requests.readline()
        previous_request_data = solution.RequestHandler(previous_request.split())
        report = solution.Report(room_data_base, previous_request_data.get_booking_date())
        room_searcher = solution.RoomSearcher(previous_request_data, room_data_base)
        room_searcher.search_suitable_room(report)

        for request in requests.readlines():
            request_data = solution.RequestHandler(request.split())

            if request_data.get_booking_date() == previous_request_data.get_booking_date():
                room_searcher = solution.RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data
                reports.add(report)
            else:
                reports.print_all_reports()
                reports = solution.Reports()
                report = solution.Report(room_data_base, request_data.get_booking_date())
                room_searcher = solution.RoomSearcher(request_data, room_data_base)
                room_searcher.search_suitable_room(report)
                previous_request_data = request_data

        reports.add(report)
        reports.print_all_reports()


if __name__ == "__main__":
    main()
