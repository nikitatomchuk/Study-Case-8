class RoomTariff:

    def __init__(self, room_tariff: str):
        self.__room_tariff = room_tariff

        if room_tariff == "standart":
            self.__price_scale = 1
        elif room_tariff == "up_standart":
            self.__price_scale = 1.2
        elif room_tariff == "apartments":
            self.__price_scale = 1.5
        else:
            print("Wrong operation. No such room type.")

    def __repr__(self):
        return self.__room_tariff

    def get_price_scale(self):
        return self.__price_scale