
"""
Фасад
«Определяет интерфейс более высокого уровня,
который упрощает использование подсистемы»

Предоставляет унифицированный интерфейс вместо набора
интерфейсов некоторой подсистемы.

Яркий пример – кэширование.
Мы обращаемся не к объекту, а к его кэшу.

Во фреймворке может быть 1000 классов,
но сам класс Application – он фасад и пользователю
не нужно знать о всех внутренних реализованных классах.
"""


# сайт-агрегатор с объявлениями о продаже авто
# парсит цены на русские и иномарки:
class Site1Checker:
    def russian_auto(self):
        print('prices of russian cars on site 1')

    def foreign_auto(self):
        print('prices of foreign cars on site 1')


# сайт-агрегатор-2:
class Site2Checker:
    def russian_auto(self):
        print('prices of russian cars on site 2')

    def foreign_auto(self):
        print('prices of foreign cars on site 2')


# сайт-агрегатор-3:
class Site3Checker:
    def russian_auto(self):
        print('prices of russian cars on site 2')

    def foreign_auto(self):
        print('prices of foreign cars on site 2')


# Здесь Фасад выполняет задачи:
# 1. Создаёт объекты доступа к сайтам.
# 2. Выполняет методы этих объектов — заменяет рутинные операции.
# т е сами сайты не важны, важна только информация кот получаем
# клиенты будут пользоваться только методами класса-фасада:
class FacadeSiteChecker:
    def __init__(self):
        self._subsys_1 = Site1Checker()  # это объекты доступа к сайтам
        self._subsys_2 = Site2Checker()  # какие это сайты - не важно
        self._subsys_3 = Site3Checker()

    def russian_auto(self):  # методы этих объектов
        self._subsys_1.russian_auto()
        self._subsys_2.russian_auto()
        self._subsys_3.russian_auto()

    def foreign_auto(self):
        self._subsys_1.foreign_auto()
        self._subsys_2.foreign_auto()
        self._subsys_3.russian_auto()


facade_site_checker = FacadeSiteChecker()
facade_site_checker.russian_auto()
facade_site_checker.foreign_auto()

