from wsgiref.simple_server import make_server
from young_framework.main import Framework
from urls import fronts
from views import routes

application = Framework(routes, fronts)
# port = int(input("Укажите порт: "))
port = 8000

with make_server('', port, application) as httpd:
    print(f'Server is running on a port {port}...')
    httpd.serve_forever()
