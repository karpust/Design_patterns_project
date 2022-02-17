import os
import sys
from young_framework.requests import GetRequests, Postrequests
from quopri import decodestring

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
            # определяем метод GET или POST:
            method = environ['REQUEST_METHOD']
            # добавляем в словарь method: 'GET' если get:
            request['method'] = method

            if method == 'POST':
                data = Postrequests().get_request_params(environ)
                request['data'] = Framework.decode_value(data)
                print(f'поступил post-запрос: {Framework.decode_value(data)}')
            elif method == 'GET':
                request_params = GetRequests().get_request_params(environ)
                request['request_params'] = Framework.decode_value(request_params)
                print(f'поступили get-параметры: '
                      f'{Framework.decode_value(request_params)}')

            for front in self.fronts:
                front(request)

            # передаем в контроллер request
            code, body = view(request)
            start_response(code, [('Content-Type', self.content_type)])
            return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

