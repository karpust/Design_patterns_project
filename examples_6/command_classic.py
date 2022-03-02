from abc import ABCMeta, abstractmethod


# позволяет не выполнять каждую задачу в отдельности
# а составить из них список и выполнить потом все
"""
Команда:
Действие как объект(Команда инкапсулирует запрос в объект)
Это позволит:  
Передавать как объект. 
Логировать действия. 
Ставить в очередь. 
Откатывать операции.

Благодаря представлению действия как объекта мы можем составить и сохранить 
последовательность операций, на каждом шаге определить обратную операцию 
или сохранить состояние.
"""


class CommandsInvoker:
    """
    класс - хранение команд
    """
    def __init__(self):
        self._commands_list = []

    def store_command(self, command):
        """
        сохранение команд в список
        """
        self._commands_list.append(command)

    def execute_commands(self):
        """
        поочередное выполнение каждой
        команды из списка
        """
        for command in self._commands_list:
            command.execute()


class Command(metaclass=ABCMeta):
    """
    интерфейс команды:
    ссылка на исполнителя(получателя команды),
    метод-выполнить
    """
    def __init__(self, receiver):
        self._receiver = receiver

    @abstractmethod
    def execute(self):
        pass


# различные команды без реализации:
class ActionCommand(Command):
    def execute(self):
        self._receiver.action()


class PauseCommand(Command):
    def execute(self):
        self._receiver.pause()


class CommandsReceiver:  # чьи команды исполняем
    """
    класс - исполнитель(получатель команды)
    с реализацией конкретных команд
    """
    def action(self):
        print('action in receiver')

    def pause(self):
        print('pause in receiver')


# пульт
commands_invoker = CommandsInvoker()  # список для задач(пока пустой)

# внутренняя логика работа кнопок
commands_receiver = CommandsReceiver()  # что конкретно делать

# кнопки
action_command = ActionCommand(commands_receiver)  # задача + что конкретно делать
pause_command = PauseCommand(commands_receiver)

# добавляем  кнопки на пульт
commands_invoker.store_command(action_command)  # добавление задач с конкретикой в список
commands_invoker.store_command(pause_command)

commands_invoker.execute_commands()  # выполнение всех задач в списке
