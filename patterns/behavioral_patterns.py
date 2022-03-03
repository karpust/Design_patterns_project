from jsonpickle import dumps, loads
from young_framework.templator import render
from abc import ABCMeta, abstractmethod


# поведенческий паттерн - Наблюдатель
class Subject:  # товары за которыми следят покупатели
    """
    класс-предмет наблюдения
    """
    def __init__(self):
        # список покупателей, которые будут уведомлены
        # при появлении нового товара:
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)  # It automatically converts into a set and adds to the set.


class Observer(metaclass=ABCMeta):
    """
    класс-интерфейс
    уведомитель
    """
    @abstractmethod
    def update(self, subject):  # уведомление
        pass


class SmsNotifier(Observer):
    """
    класс-уведомитель
    покупателя смс-сообщением
    о появлении нового товара
    """
    def update(self, subject):
        print('SMS: появился новый товар', subject.products[-1].name)


class EmailNotifier(Observer):
    """
    класс-уведомитель
    покупателя email-сообщением
    о появлении нового товара
    """
    def update(self, subject):
        print('Email: появился новый товар', subject.products[-1].name)