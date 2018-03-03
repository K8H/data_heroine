import unittest
import sys

sys.path.append("..")
import core   # noqa
from in_memory import in_memory_computations   # noqa
from sqlite import sqlite_computations     # noqa


class InMemoryComputationsTestCase(unittest.TestCase):
    def setUp(self):
        self.core = core
        self.in_memory = in_memory_computations
        self.sqlite = sqlite_computations

    def test_get_computation_mode_object_in_memory_instance(self):
        self.assertIsInstance(self.core.get_computation_mode_object('in_memory'), type(self.in_memory.InMemory()))

    def test_get_computation_mode_object_sqlite_instance(self):
        self.assertIsInstance(self.core.get_computation_mode_object('sqlite'), type(self.sqlite.Sqlite()))

    def test_get_computation_mode_object_wrong_arg_input(self):
        with self.in_memory.InMemory().captured_output() as (out, err):
            self.core.get_computation_mode_object('something_wrong')
        output = out.getvalue().strip()
        self.assertEqual(output, 'You must run the software with parameter \'--feature span\' or \'--feature avg\'')
