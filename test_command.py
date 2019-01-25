import unittest
from command import EchoCommand


class TestCommand(unittest.TestCase):
    def test_command(self):
        cmd = EchoCommand()
        self.cmd()


if __name__ == '__main__':
    unittest.main()
