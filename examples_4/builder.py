from abc import ABCMeta, abstractmethod

"""
Строитель:
«Отделяет конструирование сложного объекта от его представления, 
позволяя использовать один и тот же процесс конструирования 
для создания различных представлений»

у нас есть сложный объект. Который мы хотим строить по частям 
и не зависеть от представлений
процесс не меняется а элементы используются разные
"""


class TableDirector:
    """
    класс - Директор
    говорит что делать
    и в какой последовательности
    """
    def __init__(self):
        self._builder = None

    def construct(self, builder):
        """
        процесс конструирования и в нем
        четко определена очередность действий
        все методы вызываются отсюда
        """
        self._builder = builder  # кто строитель (какой вариант стола строит)
        self._builder._build_legs()  # сделать ножки
        self._builder._build_tabletop()  # сделать столешницу
        self._builder._build_coverage()  # покрасить


class Table:
    """
    класс - Строитель
    знает как делать конкретную часть
    """
    tabletop = 0
    legs = 0
    coverage = ''


class AbstractTableBuilder(metaclass=ABCMeta):
    """
    абстрактный класс - строитель
    """
    def __init__(self):
        self.product = Table()

    @abstractmethod
    def _build_tabletop(self):
        pass

    @abstractmethod
    def _build_legs(self):
        pass

    @abstractmethod
    def _build_coverage(self):
        pass


class BigTableBuilder(AbstractTableBuilder):
    """
    класс - строитель большого стола
    """
    def _build_tabletop(self):
        self.product.tabletop = 120

    def _build_legs(self):
        self.product.legs = 4

    def _build_coverage(self):
        self.product.coverage = 'vanish'


class SmallTableBuilder(AbstractTableBuilder):
    """
    класс - строитель маленького стола
    """
    def _build_tabletop(self):
        self.product.tabletop = 80

    def _build_legs(self):
        self.product.legs = 3

    def _build_coverage(self):
        self.product.coverage = 'yacht lacquer'


big_table__builder = BigTableBuilder()  # это строитель большого стола
small_table__builder = SmallTableBuilder()  # это строитель маленького стола

# запуск процесса конструирования
director = TableDirector()
director.construct(big_table__builder)
director.construct(small_table__builder)

# берем сконструированное изделие
big_table_1 = big_table__builder.product
small_table_1 = small_table__builder.product

print(big_table_1.coverage)
print(small_table_1.coverage)

print(big_table_1.legs)
print(small_table_1.legs)
