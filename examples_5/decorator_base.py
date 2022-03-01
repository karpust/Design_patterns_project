from abc import ABCMeta, abstractmethod

"""
Базовый вариант - без сахара
Декоратор 
«Динамически добавляет объекту новые обязанности»

Выступает в роли динамического наследования.
Альтернатива порождению подклассов с целью расширения 
функциональности.
Decorator — обычно абстрактный класс, задача которого — 
хранение ссылки на декорируемый объект.
"""


# класс абстрактного писателя Writer и его реализация:
class Writer(metaclass=ABCMeta):
    @abstractmethod
    def write_message(self):
        pass


class ConcreteWriter(Writer):
    def write_message(self):
        print('writing message')


# Пусть понадобились дополнительные действия перед записью:
# проверка длины сообщения и его сжатие.
# Реализуем их в виде декораторов на базе некоторого
# абстрактного WriterDecorator:
class WriterDecorator(Writer, metaclass=ABCMeta):
    def __init__(self, component):  # это композиция
        self._component = component

    @abstractmethod
    def write_message(self):
        pass


class CheckLengthDecorator(WriterDecorator):
    def write_message(self):
        print('checking message length')
        self._component.write_message()


class CompressDecorator(WriterDecorator):
    def write_message(self):
        print('compressing message')
        self._component.write_message()
        print('check compressed length')


concrete_writer = ConcreteWriter()
# поочереди обертываем:
check_length_decorator = CheckLengthDecorator(concrete_writer)
compress_decorator = CompressDecorator(check_length_decorator)
compress_decorator.write_message()

"""
print('compressing message')
print('checking message length')
print('writing message')
print('check compressed length')
"""
