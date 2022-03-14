from threading import local


# архитектурный системный паттерн unit of work
# Паттерн Единица работы отслеживает изменения в модели,
# которые нужно применить и в БД. Для поддержания
# непротиворечивости данных. БД применит их одной транзакцией.
# :
class UnitOfWork:
    current = local()  # локальное хранилище для потока со своим пространством имен,
    # даже если потоков будет несколько каждый будет видеть только свое
    # все операции делаем в одном потоке

    def __init__(self):
        # храним наборы изменений в списках:
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, mapperregistry):
        self.MapperRegistry = mapperregistry

    # функции добавления новых, измененных, удаленных объектов
    # в соответствующие списки:
    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    # методы достают из реестра мапперов нужный и вызывают его методы:
    def insert_new(self):
        for obj in self.new_objects:
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    # применяем изменения в бд:
    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    # операции с потоками:
    @staticmethod
    def new_current():  # создание нового потока
        print(__class__)  # <class 'patterns.architectural_system_pattern_unit_of_work.UnitOfWork'> ??????????????
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):  # сделать поток текущим
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):  # получить текущий поток
        return cls.current.unit_of_work


class DomainObject:
    """
    маркирует объекты текущего потока
    """
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)

