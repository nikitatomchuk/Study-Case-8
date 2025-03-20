from handler.RequestHandler import RequestHandler


def main():
    with open("handler/requests_data.txt", encoding='utf-8') as requests:
        for request in requests.readlines():
            request_data = RequestHandler(request.split())
            print(request_data)

if __name__ == "__main__":
    main()