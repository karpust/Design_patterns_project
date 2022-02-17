# здесь:
# GET-запрос это то что пишем в адресную строку (берем)
# POST-запрос это то что вводим в форму (отправляем)

class GetRequests:
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        # находим какую строку ввели:
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class Postrequests:
    @staticmethod
    def parse_input_data(data: str) -> dict:
        """
        обработка введенных данных,
        создание словаря из них
        """
        result = {}
        if data:
            # создаем из строки список параметров с их значениями:
            params = data.split('&')
            for item in params:
                # ключ-параметр, значение-его значение добавляем в словарь:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """
        обрабатывает и возвращает
        введенные данные в байтах
        """
        content_length_data = env.get('CONTENT_LENGTH')
        # определяем длину строки:
        content_length = int(content_length_data) if \
            content_length_data else 0  # зачем if ?
        # введенная строка в байтах:
        data = env['wsgi.input'].read(content_length) if \
            content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """
        декодирует и
        """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'сторока после декодирования - {data_str}')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        """
        принимает словарь с параметрами запроса
        """
        # в байты:
        data = self.get_wsgi_input_data(environ)
        # в словарь
        data = self.parse_wsgi_input_data(data)
        return data


