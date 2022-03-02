from abc import ABC, abstractmethod
"""
сделаем так чтобы класс Animal
сам создавал своих потомков
"""


class Animal(ABC):

    @abstractmethod
    def say(self):
        pass

    @staticmethod
    def create_animal(animal_type):
        if animal_type == 'dog':
            return Dog()
        elif animal_type == 'cat':
            return Cat()


class Dog(Animal):

    def say(self):
        print('wow-wow')


class Cat(Animal):

    def say(self):
        print('мяу-мяу')
