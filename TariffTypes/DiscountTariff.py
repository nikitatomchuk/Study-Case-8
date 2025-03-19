from data.Room import Room


class Discount:

    def __init__(self, room: Room):
        self.__discount_price = room.get_room_price() * 0.7

    def get_discount_price(self):
        return self.__discount_price

