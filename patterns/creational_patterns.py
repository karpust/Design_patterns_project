from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject
#


# """
# в магазине представлены следующие виды товаров:
# лыжи (размер ноги, ростовка, тип катания, жесткость)
# коньки (размер ноги, тип катания, заводская заточка)
#
# снегокаты (кол-во мест, вес, размер)
# ватрушки (кол-во мест)
# ледянки
#
# сноуборды (технология, тип катания)
#
# кальсоны с начесом(размер)
# маска медведя(размер головы)
# валенки(материал, размер ноги)
# """


class User:
    """
    класс - абстрактный пользователь
    """
    def __init__(self, name):
        self.name = name


class Customer(User):
    """
    класс - покупатель
    """
    def __init__(self, name):
        super().__init__(name)
        self.new_products = []


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
        # self.firm = firm
        # self.country = country
        # self.color = color
        # self.price = price
        # self.vendorcode = vendorcode
        self.category = category
        self.category.products.append(self)

        # состояние о товарах на которые подписан пользователь(на все):
        self.sub_products = []

    def __getitem__(self, item):
        return self.sub_products[item]

    def add_product(self, product):  # появление нового товара
        self.sub_products.append(product)
        self.notify()


# курс фиксирует появление нового студента
# покупатель фиксирует появление нового товара


class Skiing(Product):
    pass
    # def __init__(self, foot_size, type_rid, height, hardness,
    #              name, firm, country, color,
    #              price, vendorcode, category
    #              ):
    #     super().__init__(name, firm, country, color,
    #                      price, vendorcode,  category)
    #     self.foot_size = foot_size
    #     self.type_rid = type_rid
    #     self.height = height
    #     self.hardness = hardness


class Skates(Product):
    pass


class SnowScooters(Product):
    pass


class Tubing(Product):
    pass


class Sledge(Product):
    pass


class Snowboards(Product):
    pass


class Pants(Product):
    pass


class BearMask(Product):
    pass


class ProductFactory:
    types = {
        'skiing': Skiing,
        'skates': Skates,
        'snow scooters': SnowScooters,
        'tubing': Tubing,
        'sledge': Sledge,
        'snowboards': Snowboards,
        'pants': Pants,
        'bear mask': BearMask
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

    # создаем продукт:
    @staticmethod
    def create_product(type_, name, category):
        return ProductLevelFactory.create(type_, name, category)

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
