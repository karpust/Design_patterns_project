# Одна часть кода написана с учетом ошибки в другой части кода


def cities():
    result = ['gelendzik', 'piter', 'tula', 1, 'perm', 'samara']
    return result


def double():
    city_list = cities()
    return [item * 2 for item in city_list]


print(double())
