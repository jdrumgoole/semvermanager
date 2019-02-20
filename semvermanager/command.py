
import os
import queue


class CommandError(ValueError):
    pass

class OperationError(ValueError):
    pass

class Operation:
    def __init__(self, name=None, q=None):
        if name:
            self._name = name
        else:
            self._name = __class__.__qualname__

        if q:
            self._q = q
        else:
            self._q = queue.Queue()

    @property
    def q(self):
        return self._q

    def print_queue(self):
        for item in self.q.items():
            print(item)

    def items(self):
        while not self.q.empty():
            item = self.q.get()
            yield item


class QueryError(ValueError):
    pass


class Query(Operation):

    def __init__(self, name=None, q=None):
        if name:
            self._name = name
        else:
            self._name = __class__.name

        if q:
            self._q = q
        else:
            self._q = queue.SimpleQueue()

    def __call__(self, *args, **kwargs):
        return self


class Command(Operation):

    @staticmethod
    def null_func(*args, **kwargs):
        pass

    def __init__(self, name=None, q=None):
        super().__init__(q)


    def __call__(self, *args, **kwargs):
        """
        Either returns changed value based on args
        :param args: args
        :param kwargs: keyword args
        :return: self
        """
        return self

    @property
    def name(self):
        return self._name


class EchoCommand(Command):

    def __init__(self, name=None, q=None):
        super().__init__(q)
        if name:
            self._name = name
        else:
            self._name = self.__class__.__qualname__

    def __call__(self, *args, **kwargs):
        arg_string = ", ".join([str(x) for x in args])
        kw_string = ", ".join([f"{k}='{v}'" for k, v in kwargs.items()])
        self.q.put(arg_string)
        self.q.put(kw_string)
        return self


class StatCommand(Command):

    def __call__(self, filename):
        try:
            self.q.put(os.stat(filename))
        except FileNotFoundError as e:
            raise CommandError(e)

        return self


class OperationRunner:

    def __init__(self, op):
        self._commands = {}
        self.add(op)

    def add(self, op):
        if isinstance(op, Operation):
            self._commands[op.name] = op
        else:
            raise OperationError(f"{op} is not an instance of Operation")

    def __call__(self, files, *args, **kwargs):
        for i in files:
            for name, cmd in self._commands.items():
                try:
                    yield cmd(i, *args, **kwargs)
                except CommandError as e:
                    print(f"ERROR: command '{name}' : {e}")
