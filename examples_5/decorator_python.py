

"""
Декоратор
«Динамически добавляет объекту новые обязанности»

декораторы выполняются на этапе импорта !!
"""

# На функциях
def decorator(old_f):
    # если бы здесь был код он бы выполнился при импорте
    def inner(*args, **kwargs):
        print('two')
        return old_f(*args, **kwargs)

    return inner


@decorator
def old():
    print('one')


old = decorator(old)
old()
