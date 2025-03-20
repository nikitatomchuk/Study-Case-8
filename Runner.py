from data.RoomsDataBase import RoomDataBase
from handler.RequestHandler import RequestHandler


def main():
    rooms_data_base = RoomDataBase()
    print(rooms_data_base.get_all_rooms())
    with open("handler/requests_data.txt", encoding='utf-8') as requests:
        for request in requests.readlines():
            request_data = RequestHandler(request.split())
            print(request_data)

if __name__ == "__main__":
    main()