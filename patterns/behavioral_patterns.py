from jsonpickle import dumps, loads
from young_framework.templator import render
from abc import ABCMeta, abstractmethod


# поведенческий паттерн - Наблюдатель
class Subject:  # следим за появлением новых товаров
    """
    класс-предмет наблюдения
    """
    def __init__(self):
        self.observers = []  # наблюдатели/нотифаеры

    def notify(self):
        for item in self.observers:
            item.update(self)


class Observer(metaclass=ABCMeta):
    """
    класс-интерфейс
    наблюдателя
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


# поведенческий паттерн Хранитель:
class BaseSerializer:
    """
    хранение данных в формате json-строки,
    загрузка данных в словарь для работы
    """
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        """
        консерва json-строка
        """
        return dumps(self.obj)

    @staticmethod
    def load(data):
        """
        загрузка в словарь
        """
        return loads(data)


# поведенческий паттерн Стратегия:
class ConsoleWriter:
    """
    логгирование в консоль
    """
    def write(self, text):
        print(text)
        
        
class FileWriter:
    """
    логгирование в файл
    """
    def __init__(self):
        self.file_name = 'log'
    
    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


# поведенческий паттерн Шаблонный метод:
class TemplateView:
    """
    рендеринг шаблона с передачей контекста
    """
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)

