from young_framework.templator import render
from patterns.creational_patterns import Engine, Logger, MapperRegistry
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


@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    """
    контроллер - список категорий
    """
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories,
                                date=request.get('date', None))


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    """
    контроллер - создание категории
    """
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            # category_id = data.get('category_id')

            parent_category = None
            # if category_id:
            #     site.find_category_id(int(category_id))

            # если категория с таким именем уже есть, не дублируем:
            if name in [item.name for item in site.categories]:
                pass
            # если нет - создаем новую:
            else:
                new_category = site.create_category(name, parent_category)
                site.categories.append(new_category)
            return '200 OK', render('index.html',
                                    objects_list=site.categories,
                                    date=request.get('date', None))

        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories,
                                    date=request.get('date', None))


@AppRoute(routes=routes, url='/product_list/')
class ProductList:
    def __call__(self, request):
        logger.log('Список товаров')
        try:
            category = site.find_category_id(int(request['request_params']['id']))
            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name, id=category.id,
                                    date=request.get('date', None))
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/create_buyer/')
class CreateBuyer:
    """
    контроллер - создание покупателя
    """
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            new_buyer = site.create_user('buyer', name)
            site.buyers.append(new_buyer)


@AppRoute(routes=routes, url='/create_product/')
class CreateProduct:
    """
    контроллер - создание продукта
    """
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_id(int(self.category_id))

                # если товар с таким именем уже есть, не дублируем:
                if name in [item.name for item in site.products]:
                    pass
                # если нет - создаем:
                else:
                    new_product = site.create_product('begginer', name, category)

                    # добавим нотификаторы о покупке товара:
                    new_product.observers.append(email_notifier)
                    new_product.observers.append(sms_notifier)

                    site.products.append(new_product)
            return '200 OK', render('product_list.html',
                                    objects_list=site.products,
                                    name=category.name,
                                    id=category.id,
                                    date=request.get('date', None))

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_id(int(self.category_id))

                return '200 OK', render('create_product.html',
                                        name=category.name,
                                        id=category.id,
                                        date=request.get('date', None))
            except KeyError:
                return '200 OK', 'No categories have been added yet'


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
                                    name=new_product.category.name,
                                    date=request.get('date', None))
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/api/')
class ProductApi:
    @Debug(name='ProductApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.products).save()


@AppRoute(routes=routes, url='/create_buyer/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyer.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('buyer', name)
        site.buyers.append(new_obj)
        # внесение изменений в бд:
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/buyers_list/')
class BuyersListView(ListView):
    # queryset = site.buyers
    template_name = 'buyers_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('buyer')
        return mapper.all()


@AppRoute(routes=routes, url='/add_buyer/')
class AddBuyerCreateView(CreateView):
    template_name = 'add_buyer.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['buyers'] = site.buyers
        return context

    def create_obj(self, data: dict):
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)
        buyer_name = data['buyer_name']
        buyer_name = site.decode_value(buyer_name)
        buyer = site.get_buyer(buyer_name)
        product.add_buyer(buyer)



