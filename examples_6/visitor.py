from abc import ABCMeta, abstractmethod


"""
Visitor // Посетитель

Описывает операцию, выполняемую с каждым объектом 
из некоторой структуры. позволяет определить новую 
операцию, не изменяя классы этих объектов.

пример: программист и адвокат не умеют чинить, 
но могут нанять ремонтника чтобы починить

"""


class Human(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass


# программист и адвокат не умеют чинить,
# но могут нанять ремонтника:
class Programmer(Human):

    def accept(self, visitor):  # принять реомнтника
        visitor.repair(self)


class Lawyer(Human):
    def accept(self, visitor):
        visitor.repair(self)


class ConstructionElementVisitor(metaclass=ABCMeta):
    """
    интерфейс ремонтника:
    должен уметь чинить
    """

    @abstractmethod
    def repair(self):
        pass


# неважно какой ремонтник, главное что умеет чинить:
class Cool(ConstructionElementVisitor):

    @abstractmethod
    def repair(self):
        print('Дорого', 'Круто')


class NotCool(ConstructionElementVisitor):

    @abstractmethod
    def repair(self):
        print('Дешево', 'Не Круто')
