from abc import ABC, abstractmethod
"""
Чтобы избежать этого создадим для каждого 
семейства свою фабрику.
создадим абстрактную фабрику - класс AbstractFactory
которая укажет какие методы должны быть
у фабрик-наследников
Но и здесь абстракции недостаточно
т к все равно придется вызывать какую-то фабрику
"""

# Семейство классов для VK
class VkParser:
    pass


class VkAnalizer:
    pass


class VkSender:
    pass


# Семейство классов для одноклассников
class OdParser:
    pass


class OdAnalizer:
    pass


class OdSender:
    pass


class AbstractFactory(ABC):
    @abstractmethod
    def create_parser(self):
        pass

    @abstractmethod
    def create_analizer(self):
        pass

    @abstractmethod
    def create_sender(self):
        pass


class VkFactory(AbstractFactory):
    def create_parser(self):
        return VkParser()

    def create_analizer(self):
        return VkAnalizer()

    def create_sender(self):
        return VkSender()


class OdFactory(AbstractFactory):
    def create_parser(self):
        return OdParser()

    def create_analizer(self):
        return OdAnalizer()

    def create_sender(self):
        return OdSender()
