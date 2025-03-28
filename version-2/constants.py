import ru_local as ru


class Files:
    DATA_FILE_NAME = "version-2/datafiles/rooms_data.txt"
    REQUESTS_FILE_NAME = "version-2/datafiles/requests_data.txt"


class RoomTariffs:
    STANDARD = ru.STANDARD
    STANDARD_UP = ru.STANDARD_UP
    APARTMENT = ru.APARTMENT

    STANDARD_RATIO = 1
    STANDARD_UP_RATIO = 1.2
    APARTMENT_RATIO = 1.5


class RoomTypes:
    ONE_PERSON = ru.ONE_PERSON
    TWO_PERSON = ru.TWO_PERSON
    HALF_LUXE = ru.HALF_LUXE
    LUXE = ru.LUXE

    ONE_PERSON_PRICE = 2900
    TWO_PERSON_PRICE = 2300
    HALF_LUXE_PRICE = 3200
    LUXE_PRICE = 4100


class FoodTariffs:
    NO_FOOD = ru.NO_FOOD
    BREAKFAST = ru.BREAKFAST
    FULL = ru.FULL

    NO_FOOD_PRICE = 0
    BREAKFAST_PRICE = 280
    FULL_PRICE = 1000
