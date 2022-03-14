from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject
from patterns.architectural_system_pattern_unit_of_work import DomainObject
from sqlite3 import connect


connection = connect('patterns.sqlite')  # открывает соединение с файлом бд


class User:
    """
    класс - абстрактный пользователь
    """
    def __init__(self, name):
        self.name = name


class Seller(User):
    pass


class Buyer(User, DomainObject):
    """
    класс - покупатель
    """
    def __init__(self, name):
        super().__init__(name)
        self.products = []


class UserFactory:
    types = {
        'buyer': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class PrototipeProduct:
    """
    класс-прототип продукта
    создает копию объекта
    """
    def clone(self):
        return deepcopy(self)


class Product(PrototipeProduct, Subject):
    """
    класс товара
    у любого товара есть:
    название, фирма произвадитель,
    страна производства, цвет, цена, артикул,
    категория к которой он относится
    """
    def __init__(self, name, category):  # firm, country, color, price, vendorcode,
        super().__init__()
        self.name = name
        self.category = category
        self.category.products.append(self)

        # состояние о товарах на которые подписан пользователь(на все):
        self.buyers = []

    def __getitem__(self, item):
        return self.buyers[item]

    def add_buyer(self, buyer: Buyer):  # кто купил товар
        self.buyers.append(buyer)
        self.notify()


class Skiing(Product):
    pass


class Skates(Product):
    pass


class ProductFactory:
    types = {
        'skiing': Skiing,
        'skates': Skates,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class BegginersProduct(Product):
    """
    класс товара для ночинающих и любителей
    """
    pass


class ExpertProduct(Product):
    """
    класс товара для профи и спортсменов
    """
    pass


class ProductLevelFactory:
    """
    класс - фабрика товара
    передает создание инстанса классам
    BegginersProduct или ExpertProduct
    """
    types = {
        'begginer': BegginersProduct,
        'expert': ExpertProduct
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)  # вызов соотв класса


class Category:
    id = 0

    def __init__(self, name, parent_category):
        self.id = Category.id
        Category.id += 1
        self.name = name
        self.parent_category = parent_category
        self.products = []  # продукты категории

    def count_products(self):
        """
        считает количество товаров в категориях
        """
        # подсчет кол-ва товаров в этой категории:
        amount = len(self.products)
        # подсчет кол-ва товаров в родительской категории:
        if self.parent_category:
            amount += self.parent_category.count_products()
        return amount


class Engine:
    def __init__(self):
        self.products = []
        self.categories = []
        self.buyers = []

    # создаем продукт:
    @staticmethod
    def create_product(type_, name, category):
        return ProductLevelFactory.create(type_, name, category)

    # выбираем продукт:
    def get_product(self, name) -> Product:
        for item in self.products:
            if item.name == name:
                return item

    # выбираем покупателя:
    def get_buyer(self, name) -> Buyer:
        for item in self.buyers:
            if item.name == name:
                return item

    # создаем пользователя:
    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    # создаем категорию:
    @staticmethod
    def create_category(name, parent_category):
        return Category(name, parent_category)

    # найти категорию по id:
    def find_category_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
            raise Exception(f'No category with id = {id}')

    # найти товар по имени:
    def find_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# паттерн синглтон:
# «Гарантирует, что класс может иметь только один экземпляр,
# и предоставляет глобальную точку доступа к нему»
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        else:  # kwargs
            name = kwargs['name']
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        """
        логгирование в файл и в консоль
        """
        self.writer.write(text)
        print('log--->', text)


# паттерн Преобразователь данных - Data Mapper
# транслирует команды в SQL
# методы этого класса принимают объект модели и
# через него выполняют операции по изменению БД
# Слой преобразования данных:
class BuyerMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'buyer'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            buyer = Buyer(name)
            buyer.id = id
            result.append(buyer)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id, ))
        result = self.cursor.fetcheall()
        if result:
            return Buyer(*result)
        else:
            raise RecordNotFoundExeption(f'record with id={id}'
                                         f'not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitExeption(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateExeption(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteExeption(e.args)


class MapperRegistry:
    """
    класс-реестр всех мапперов
    """
    mappers = {
        'buyer': BuyerMapper,
        # 'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        """
        определяет к какому классу принадлежит объект
        и соединяет соотв маппер с бд
        """
        if isinstance(obj, Buyer):
            return BuyerMapper(connection)  # соединение маппера с бд

    @staticmethod
    def get_current_mapper(name):
        """
        определяет маппер по ключу
        из словаря мапперов,
        и соединяет его с бд
        """
        return MapperRegistry.mappers[name](connection)


# классы - вывод сообщений при исключениях:
class DbCommitExeption(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateExeption(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteExeption(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundExeption(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found error: {message}')



