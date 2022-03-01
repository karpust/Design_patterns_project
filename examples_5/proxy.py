from abc import ABCMeta, abstractmethod

"""
Заместитель (прокси)
«Позволяет сослаться на объект более изощрённо, 
чем это возможно с простым указателем»

Класс-прокси подменяет реальный класс.
"""

# Есть сервис, предоставляющий текущий курс валюты по ЦБ.
# Информацией о курсе валюты владеет ЦБ, но она меняется редко(раз в день),
# а в приложении может быть запрошена часто(сотни раз в день).
# Решение — кешировать информацию о курсе, полученную от ЦБ.

class CurrencyRateService(metaclass=ABCMeta):
    """
    абстрактный класс - интерфейс сервиса
    """
    @abstractmethod
    def get_currency_rate(self, currency):
        pass


class CbrCurrencyRateService(CurrencyRateService):
    """
    Реальный (медленный) сервис, запрашивающий курс
    валюты у истинного владельца информации:
    """
    def get_currency_rate(self, currency):
        # ... особенности реализации опущены
        return 0.57


class ProxyCurrencyRateService(CurrencyRateService):
    """
    Кеширующий прокси:
    это зам - решает сделать самому
    или передать медленному сервису
    """
    def __init__(self):
        # ссылка на реальный сервис
        self.currencyRateService = CbrCurrencyRateService()  # чей мы зам

        # кэш курсов
        self.rates = dict()

    def get_currency_rate(self, currency):
        if currency in self.rates.keys():
            # если курс уже имеется в кэше, выдать из кэша
            print(f'{currency}: from cache')
            return self.rates[currency]
        else:
            # если еще нет, то запросить реальный (медленный) сервис
            print(f'{currency}: from service')
            rate = self.currencyRateService.get_currency_rate(currency)
            self.rates.update({currency: rate})
            return rate


# создаем прокси сервис:
currency_rate_service = ProxyCurrencyRateService()

# получаем курс из кэша или от цб - это решает прокси
yen_rate_request_1 = currency_rate_service.get_currency_rate('yen')
print(yen_rate_request_1)

yen_rate_request_2 = currency_rate_service.get_currency_rate('yen')
print(yen_rate_request_2)
