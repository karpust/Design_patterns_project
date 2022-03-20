from young_framework.templator import render
from patterns.creational_patterns import Engine, Logger, MapperRegistry, Mapper
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    BaseSerializer, FileWriter, ConsoleWriter, CreateView, TemplateView, \
    ListView
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork


site = Engine()
# стратегия: взаимозаменяемые алгоритмы FileWriter() или ConsoleWriter():
logger = Logger('main', FileWriter())
routes = {}  # декоратор AppRoute заполняет словарь
# при запуске, еще до вызова контроллеров
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()  # создаем сессию работы с БД
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Index:
    """
    контроллер - главная
    """
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render(
            'index.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/contact/')
class Contact:
    """
    контроллер - контакты
    """
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render(
            'contact.html',
            date=request.get('date', None))


@AppRoute(routes=routes, url='/about/')
class About:
    """
    контроллер - о проекте
    """
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render(
            'about.html', date=request.get('date', None))


class NotFound404:
    """
    контроллер - страница не найдена
    """
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'


@AppRoute(routes=routes, url='/create_category/')
class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_category(name)

        # внесение в список:
        site.categories.append(new_obj)
        # внесение в бд:
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/category_list/')
class CategoryListView(ListView):
    template_name = 'category_list.html'

    def get_mapper(self, name):  # ф отправить родителю
        mapper = MapperRegistry.get_current_mapper(name)
        return mapper

    def get_queryset(self):
        return self.get_mapper('category').all()


@AppRoute(routes=routes, url='/create_product/')
class ProductCreateView(CreateView):
    template_name = 'create_product.html'

    def get_mapper(self, name):  # ф отправить родителю
        mapper = MapperRegistry.get_current_mapper(name)
        return mapper

    def get_context_data(self):
        context = {}
        category_name = self.get_mapper('product').find_name_by_id(self.category_id)  # получили имя категории по id
        context['category_name'] = category_name
        return context

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_product = site.create_product('begginer', name, self.category_id)

        # внесение в список:
        site.products.append(new_product)
        # внесение в бд:
        new_product.mark_new()
        UnitOfWork.get_current().commit()

    def __call__(self, request):
        print(f'request = {request}')
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            self.category_id = int(request['request_params']['id'])
            return super().__call__(request)


@AppRoute(routes=routes, url='/product_list/')
class ProductsListView(ListView):  # здесь из реквеста нужно достать id категории
    template_name = 'product_list.html'

    def __call__(self, request):
        self.category_id = int(request['request_params']['id'])
        return self.render_template_with_context()

    def get_mapper(self, name):  # ф отправить родителю
        mapper = MapperRegistry.get_current_mapper(name)
        return mapper

    def get_queryset(self):
        mapper = self.get_mapper('product')
        return mapper.find_by_category_id(self.category_id)  # [(1, 'горные лыжи', 1), (2, 'скоростные лыжи', 1)]

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        category_name = self.get_mapper('product').find_name_by_id(self.category_id)  # получили имя категории по id
        context['category_name'] = category_name
        return context


@AppRoute(routes=routes, url='/add_product/')
class AddProductCreateView(CreateView):  # добавление товара покупателю:
    template_name = 'add_product.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['buyers'] = site.buyers
        return context

    def create_obj(self, data: dict):
        buyer_name = data['buyer_name']
        buyer_name = site.decode_value(buyer_name)
        buyer = site.get_buyer(buyer_name)
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)
        buyer.add_product(product)


@AppRoute(routes=routes, url='/copy_product/')
class CopyProduct:
    """
    контроллер - копирование товара
    """
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_product = site.find_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render('product_list.html',
                                    objects_list=site.products,
                                    name=new_product.name,
                                    date=request.get('date', None))
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/create_buyer/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyer.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('buyer', name)
        # добавим нотификаторы о покупках пользователя:
        new_obj.observers.append(email_notifier)
        new_obj.observers.append(sms_notifier)

        # внесение в список:
        site.buyers.append(new_obj)
        # внесение в бд:
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/buyers_list/')
class BuyersListView(ListView):
    template_name = 'buyers_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('buyer')
        return mapper.all()


@AppRoute(routes=routes, url='/api/')
class ProductApi:
    @Debug(name='ProductApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.products).save()
