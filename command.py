
class CommandError(ValueError):
    pass

def null_func(*args, **kwargs):
    pass

class Command:
    def __init__(self, name=None, func=None, *args, **kwargs):
        if name:
            self._name = name
        else:
            self._name = __class_.name

        if func:
            self._func = func
        else:
            self._func = null_func

    def __call__(self, *args, **kwargs):
        return self._func(*args,**kwargs)

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, value):
        self._func = value

    @property
    def name(self):
        return self._name

class EchoCommand(Command):

    def __init__(self) :
        self._name = __class__.name
        self._func = null_func

    def __call__(self, *args, **kwargs):
        print(f"Running: {self._name}( {*args}, {**kwargs})")



class CommandRunner:

    def __init__(self, command):
        self._commands ={}


    def add_command(self, command):
        if isinstance(command, Command):
            self._commands[command.name] = command
        else:
            raise CommandError(f"{command} is not an instance of Command")

    def file_command_generator(self, files, *args, **kwargs):
        for i in files:
            for name,cmd in self._commands:
                yield cmd.execute(i, *args, **kwargs)
