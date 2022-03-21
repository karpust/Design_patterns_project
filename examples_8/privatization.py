class A:

    def __init__(self):
        # модификаторы доступа: private, protected, public
        self.__a = 0  # приватные атрибуты не доступны наследникам
        self._a = 0  # лучше использовать защищенные атрибуты
        self.a = 0
