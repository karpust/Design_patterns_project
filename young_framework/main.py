
class PageNotFound404:
    def __call__(self, request):
        return '404', '404 - Page not found'


class Framework:
    """
    основной класс фреймворка,
    распределяет адреса соответствующим контроллерам
    """
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        # адрес по которому перешли:
        path = environ['PATH_INFO']

        # добавление слэша в конце:
        if not path.endswith('/'):
            path = f'{path}/'

        # паттерн Page Controller:
        # находим соответствующий контроллер:
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # паттерн Front Controller:
        # словарь который получают все контроллеры:
        request = {}
        for front in self.fronts:
            front(request)

        #
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

