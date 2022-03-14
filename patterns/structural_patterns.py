from time import time


# структурный паттерн - Декоратор:
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        # сам декоратор
        self.routes[self.url] = cls()


# структурный паттерн - Декоратор:
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # сам декоратор:
        # ф-ция декорирует каждый метод класса:
        def timeit(method):
            # нужен чтобы декоратор класса wrapper обернул
            # в timeit каждый отдельный метод класса:
            def timed(*args, **kwargs):
                start = time()
                res = method(*args, **kwargs)
                end = time()
                lead_time = end - start
                print(f'debug --> {self.name} completed in time {lead_time:2.2f} ms')
                return res
            return timed
        return timeit(cls)

