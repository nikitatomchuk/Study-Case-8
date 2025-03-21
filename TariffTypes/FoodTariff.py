class FoodTariff:

    def __init__(self, food_tariff: str, people_count: int):
        self.__food_tariff = food_tariff

        try:
            if self.__food_tariff == "no":
                self.__food_price_per_day = 0
            elif self.__food_tariff == "breakfast":
                self.__food_price_per_day = 280 * people_count
            elif self.__food_tariff == "full":
                self.__food_price_per_day = 1000 * people_count
            else:
                print("Wrong operation. No such food tariff.")

    def __repr__(self):
        return self.__food_tariff

    def get_food_price_per_day(self):
        return self.__food_price_per_day
