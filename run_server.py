from wsgiref.simple_server import make_server
from young_framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

with make_server('', 8000, application) as httpd:
    print('Server is running on a port 8080...')
    httpd.serve_forever()
