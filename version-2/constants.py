class Files:
    DATA_FILE_NAME = "version-2/rooms_data.txt"
    REQUESTS_FILE_NAME = "version-2/requests_data.txt"


class RoomTariffs:
    STANDARD = "стандарт"
    STANDARD_UP = "стандарт_улучшенный"
    APARTMENT = "аппартамент"

    STANDARD_RATIO = 1
    STANDARD_UP_RATIO = 1.2
    APARTMENT_RATIO = 1.5



class RoomTypes:
    ONE_PERSON = "одноместный"
    TWO_PERSON = "двухместный"
    HALF_LUXE = "полулюкс"
    LUXE = "люкс"

    ONE_PERSON_PRICE = 2900
    TWO_PERSON_PRICE = 2300
    HALF_LUXE_PRICE = 3200
    LUXE_PRICE = 4100


class FoodTariffs:
    NO_FOOD = "без питания"
    BREAKFAST = "завтрак"
    FULL = "полупансион"

    NO_FOOD_PRICE = 0
    BREAKFAST_PRICE = 280
    FULL_PRICE = 1000
