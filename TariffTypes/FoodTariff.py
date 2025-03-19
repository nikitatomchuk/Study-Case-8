class FoodTariff:

    def __init__(self, food_tariff: str, people_count: str):
        self.__food_tariff = food_tariff

        try:
            self.__people_count = int(people_count)

            try:
                if self.__food_tariff == "no":
                    self.__price = 0
                elif self.__food_tariff == "breakfast":
                    self.__price = 280 * people_count
                elif self.__food_tariff == "full":
                    self.__price = 1000 * people_count
                else:
                    raise TypeError
            except TypeError:
                print("Wrong operation. No such food tariff.")

        except ValueError:
            print("Arguments Error. Can not convert people count into number.")

    def __repr__(self):
        return self.__food_tariff

    def get_price(self):
        return self.__price