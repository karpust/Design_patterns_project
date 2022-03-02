from copy import deepcopy

"""
Прототип:
«Описывает виды создаваемых объектов с помощью прототипа 
и создаёт новые объекты путём копирования».

есть некоторый большой объект, который уже наполнен данными 
и нам быстрее его скопировать, нежели создать новый.

Задаёт виды создаваемых объектов с помощью экземпляра Прототипа 
и новые объекты путём копирования этого Прототипа.
"""


class PrototypeMixin:
    # прототип

    def clone(self):
        print('создана копию экземпляра класса')
        return deepcopy(self)


class Original(PrototypeMixin):
    pass


class OriginalClass(PrototypeMixin):
    pass


original = Original()
original.clone()

original_2 = OriginalClass()
original_2.clone()


class ModernPrototypeMixin(PrototypeMixin):

    def clone(self):
        print('что то еще')
        return deepcopy(self)


class Original(ModernPrototypeMixin):
    pass


# Смысл в том, чтобы объект сам себя копировал
original = Original()
original.clone()

# счетчик экземпляров класса:
# class InstanceCounter(object):
#     count = 0
#
#     def __init__(self):
#         self.__class__.count += 1
#
#     @classmethod
#     def instances_count(cls):
#         return cls.count

