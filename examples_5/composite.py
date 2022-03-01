from abc import ABCMeta, abstractmethod


"""
Компоновщик
«Компонует объекты в древовидные иерархические 
структуры для представления иерархий часть—целое»

Он позволяет клиентам единообразно трактовать 
индивидуальные и составные объекты.
Смысл паттерна — предоставить клиентскому коду общий 
интерфейс для контейнера и одиночного элемента.

Применяется к рекурсивным объектам, т.е. к древовидным объектам.
"""

# Главное, чтобы реализация действия (операции) была и
# в классе листа, и в классе компоновщика.

class Component(metaclass=ABCMeta):
    """
    Абстракция компонента, который
    должен выполнять определённую операцию
    независимо папка это или файл
    """
    # это абстрактный класс - интерфейс
    @abstractmethod
    def operation(self):
        pass


class MachineOperation(Component):
    # это класс - Файл,
    # машинная операция
    def __init__(self, name):
        self.name = name

    def operation(self):
        print(self.name)


class CompositeOperation(Component):
    # это класс - Папка,
    # композитная операция
    # класс - компоновщик
    def __init__(self):
        self._child = set()

    def operation(self):
        print('folder')
        for child in self._child:
            child.operation()  # если это файл то MachineOperation

    def append(self, component):
        self._child.add(component)

    def remove(self, component):
        self._child.discard(component)


# инициализация операций
operation_1 = MachineOperation('drill 5 mm')
operation_2 = MachineOperation('drill 15 mm')
composite_1 = CompositeOperation()
composite_1.append(operation_1)
composite_1.append(operation_2)

operation_3 = MachineOperation('assemble')
operation_4 = MachineOperation('paint')
composite_2 = CompositeOperation()
composite_2.append(composite_1)
composite_2.append(operation_3)
composite_2.append(operation_4)
print(composite_2._child)

# использование разных по структуре операций идентично
composite_2.operation()
# operation_1.operation()
