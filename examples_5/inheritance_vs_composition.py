"""
Наследование vs Композиция
если кошка является животным - то это наследование
если двигатель является не машиной, а частью машины - то это композиция
"""


# Наследование
class Animal:
    def say(self):
        pass


class Cat(Animal):
    def say(self):
        pass


class Engine:
    def move(self):
        print('Move')


# Машина не является двигателем?
class Car(Engine):
    pass


car = Car()
car.move()


# Композиция
# Двигатель это часть машины
class Car:

    def __init__(self, engine):  # Класс-Composite содержит объект класса-Component.
        self.engine = engine

    def change_engine(self, engine):
        self.engine = engine


engine = Engine()
car = Car(engine)

car.engine.move()
