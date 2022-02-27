from datetime import date
from views import Index, About, Contact, \
    CreateCategory, CreateProduct, ProductList, \
    CategoryList, CopyProduct


# front controller -
def front_1(request):
    request['date'] = date.today()


def front_2(request):
    request['date'] = date.today()


fronts = [front_1, front_2]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/create_category/': CreateCategory(),
    '/create_product/': CreateProduct(),
    '/category_list/': CategoryList(),
    '/product_list/': ProductList(),
    '/copy_product/': CopyProduct()
}


