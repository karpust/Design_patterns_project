from abc import ABCMeta, abstractmethod
from random import choice, random

"""
Цепочка ответственности:
Дать шанс обработать запрос нескольким участникам, 
связанным последовательно

Пример: звонок в коллцентр, передают звонок операторам,
пока не найдется свободный чтобы ответить
если так и не найдется вернет что все заняты
"""


class Handler(metaclass=ABCMeta):
    """
    интерфейс обработчика:
    (оператор сети)
    обработает запрос сам или
    отдаст дальше по цепочке
    """
    @abstractmethod
    def handle(self, request):
        # след звено цепи есть, то передать на обработку ему:
        if self.next is not None:
            self.next.handle(request)

    def link(self, next):  # ссылка на след звено цепи
        self.next = next
        return self.next


class Request:
    data = [
        'вопрос по возврату товара',
        'вопрос по скидке',
        'вопрос по стоимости товара',
        'вопрос по дефекту',
        'вопрос по новинке',
    ]

    def get_data(self):
        # return random.sample(__class__.data, 1)[0]
        return choice(__class__.data)  # Choose a random element from a non-empty sequence


# можно собрать цепочку из таких операторов:
class Operator(Handler):
    # вероятность занятости оператора:
    probability = 0.99

    def __init__(self, name):
        self.name = name

    def handle(self, request):
        if self.is_busy():
            print(f'Оператор {self.name} занят')
            super().handle(request)
        else:
            print(f'Оператор {self.name} обрабатывает: "{request.get_data()}"')

    def is_busy(self):
        return random() < __class__.probability


class BusyHandler(Handler):
    """
    класс - обработчик если
    все операторы заняты
    """
    def __init__(self):
        self.request = None

    def handle(self, request):
        if self.request == request:
            print('Все операторы заняты, пожалуйста подождите')
        else:
            self.request = request

        super().handle(request)


handler = BusyHandler()

handler.link(Operator("#1")).link(Operator("#2")). \
    link(Operator("#3")).link(Operator("#4")). \
    link(handler)

# генерируем поток из 1 запроса:
for _ in range(1):
    handler.handle(Request())
