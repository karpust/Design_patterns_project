from abc import ABC, abstractmethod
"""
избавимся от условий используя словарь
т е скажем методу о том какой класс
создает какое животное
"""


class Animal(ABC):

    @abstractmethod
    def say(self):
        pass

    @staticmethod
    def create_animal(animal_type):
        ANIMALS = {
            'dog': Dog,
            'cat': Cat,
            'bear': Bear
        }
        return ANIMALS[animal_type]()


class Dog(Animal):

    def say(self):
        print('wow-wow')


class Cat(Animal):

    def say(self):
        print('мяу-мяу')


class Bear(Animal):

    def say(self):
        print('мяу-мяу')


# т о используя абстрактный класс
# мы получили экземпляр нужного класса
rotveler = Animal.create_animal('dog')
print(type(rotveler))  # <class '__main__.Dog'>
rotveler.say()  # wow-wow
"""
Фабричный метод:
«Определяет интерфейс для создания объектов, 
при этом выбранный класс 
инстанцируется подклассами»
"""
