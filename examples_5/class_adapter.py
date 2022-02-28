from abc import ABCMeta, abstractmethod
from math import sqrt

"""
Структурный паттерн - Адаптер:
«Преобразует интерфейс одного класса в 
интерфейс другого, который ожидают клиенты»

Адаптеры бывают двух типов: адаптер класса и адаптер объекта.
Минус адаптера класса: если много классов-придется много адаптировать
(повторять код, зависимы от конкретики)
поэтому чаще используется адаптер объекта
(т е передача ссылки на абстрактный объект класса)
"""

# Адаптер класса:
# классы круг и квадрат с разными интерфейсами
# нужно ссоздать класс-адаптер который адаптирует интерфейс
# одного класса(Square) под другой(Roundable)
# используем наследование


# нечто круглое, имеющее радиус
class Roundable(metaclass=ABCMeta):
    @abstractmethod
    def get_radius(self):
        pass


# конкретный класс - окружность - имеет радиус
class Circle(Roundable):
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius


# квадрат со стороной side
class Square:
    def __init__(self, side):
        self._side = side

    def get_side(self):
        return self._side


# круглый квадрат (вписанная окружность)
class RoundableSquare(Square, Roundable):
    """
    это класс-адаптер.
    Square – то, что адаптируем
    Roundable – то, к чему адаптируем
    не удобно - писать адаптер к каждому адаптируемому
    """
    def get_radius(self):
        return self.get_side() * sqrt(2) / 2


circle_1 = Circle(5)
roundable_square_1 = RoundableSquare(5)

print(circle_1.get_radius())
print(roundable_square_1.get_radius())

print(issubclass(circle_1.__class__, Roundable))
print(issubclass(roundable_square_1.__class__, Roundable))
