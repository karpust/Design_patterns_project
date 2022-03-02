from abc import ABCMeta, abstractmethod


"""
Observer // Наблюдатель
Определяет зависимость типа «один ко многим» между объектами таким образом, 
что при изменении состояния одного объекта все зависящие от него оповещаются 
об этом и автоматически обновляются

пример: отслеживание появления нового участника курса
"""


class Subject:  # группа вк
    """
    группа вк
    """
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):  # добавить в группу
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):  # убрать из группы
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):  # уведомление о новости
        for observer in self._observers:
            observer.update(self._subject_state)


class Observer(metaclass=ABCMeta):  # подписчики группы вк
    """

    """
    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abstractmethod
    def update(self, arg):  # обновления в группе
        pass


class Sensor(Subject):  # градусник
    @property
    def t(self):
        return self._subject_state

    @t.setter
    def t(self, t):  # как только меняется t
        self._subject_state = t  # изменяется состояние
        self._notify()  # оповещение для всех


class SmsNotifier(Observer):  # смс оповещение если температура выше нормы

    def update(self, arg):
        if arg > 50:
            print('send sms', 'куда так горячо!')


class DisplayObserver(Observer):  # оповещение на дисплее
    def update(self, arg):
        print(f'{self.__class__.__name__} temperature {arg}')


class HeaterObserver(Observer):  # оповещение сиреной
    def __init__(self, low_threshold, step):
        super().__init__()
        self.low_threshold = low_threshold
        self.step = step

    def update(self, arg):
        if isinstance(self._subject, Sensor):
            sensor = self._subject

            t = sensor.t
            delta_low = t - self.low_threshold

            if delta_low < 0:
                t += self.step
                print(f'{self.__class__.__name__} heat impulse +{self.step}')
                sensor.t = t


# сенсором
sensor = Sensor()  # это как группа вк

# подключаем наблюдателей за сенсором
# это как подписчики группы вк:
sensor.attach(DisplayObserver())
sensor.attach(HeaterObserver(40, 20))
sensor.attach(SmsNotifier())

# изменяем состояние сенсора
sensor.t = 20
