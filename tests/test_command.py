import unittest
from semvermanager import command


class TestCommand(unittest.TestCase):
    def test_command(self):
        cmd = command.EchoCommand()
        cmd(1, 2, 3, 4, this="that", these="those")
        self.assertEqual(cmd.q.get(), "1, 2, 3, 4")


if __name__ == '__main__':
    unittest.main()
