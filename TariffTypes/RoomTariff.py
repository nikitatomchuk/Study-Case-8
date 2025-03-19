class RoomTariff:

    def __init__(self, room_type: str):
        self.__room_type = room_type
        try:
            if room_type == "standart":
                self.__price_scale = 1
            elif room_type == "up_standart":
                self.__price_scale = 1.2
            elif room_type == "apartments":
                self.__price_scale = 1.5
            else:
                raise TypeError
        except TypeError:
            print("Wrong operation. No such room type.")

    def __repr__(self):
        return self.__room_type

    def get_price_scale(self):
        return self.__price_scale