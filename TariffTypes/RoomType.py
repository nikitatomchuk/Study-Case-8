class RoomType:

    def __init__(self, room_type: str, people_count: int):
        self.__room_type = room_type

        if self.__room_type == "alone":
            self.__size_price_per_day = 2900
        elif self.__room_type == "duo":
            self.__size_price_per_day = 2300 * people_count
        elif self.__room_type == "half-luxe":
            self.__size_price_per_day = 3200 * people_count
        elif self.__room_type == "luxe":
            self.__size_price_per_day = 4100 * people_count
        else:
            print("Wrong operation. No such room size.")

    def __repr__(self):
        return self.__room_type

    def get_size_price_per_day(self):
        return self.__size_price_per_day

