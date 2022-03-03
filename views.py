from young_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier

site = Engine()
logger = Logger('main')
routes = {}  # декоратор AppRoute заполняет словарь
# при запуске, еще до вызова контроллеров
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


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
                    # добавим нотификаторы для покупателей о появлении нового товара:
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
