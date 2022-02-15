import os
import sys
sys.path.append('../')

# имя папки статики:
static_name = '/static/'
file_types = {
    '.css': 'text/css',
    '.scss': 'text/scss',
    '.js': 'text/javascript',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
}


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 - Page not found'  # WHAT


class Framework:
    """
    основной класс фреймворка,
    распределяет адреса соответствующим контроллерам
    """
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts
        self.content_type = None

    def __call__(self, environ, start_response):
        # адрес по которому перешли:
        path = environ['PATH_INFO']

        # если это ссылка на статику:
        if static_name in path:
            file_path = f'{os.getcwd()}' + path

            # определяем тип файла:
            for file_type in file_types:
                if file_type in path:
                    self.content_type = file_types[file_type]
                    break

            # считываем данные из файла
            with open(file_path, 'rb') as f:
                data = f.read()

            response_headers = [('Content-type', self.content_type),
                                ('Content-Length', str(len(data)))]
            start_response('200 OK', response_headers)
            return [data]

        # если это ссылка на страницу:
        else:
            # проверим слэш в конце, добавим:
            if not path.endswith('/'):
                path = f'{path}/'
            self.content_type = 'text/html'

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

            # передаем в контроллер request
            code, body = view(request)
            start_response(code, [('Content-Type', self.content_type)])
            return [body.encode('utf-8')]

