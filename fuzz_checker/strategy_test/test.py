from strategies.concolic import ConcolicStrategy
from strategies.gradient_descent import GradientDescentStrategy
from strategies.length import LengthStrategy
from strategies.length_taint import LengthTaintStrategy
from strategies.magic_byte import MagicByteStrategy
from strategies.one_byte import OneByteStrategy
from strategies.random import RandomStrategy
from strategies.random_taint import RandomTaintStrategy
from trace import Trace
from importer import Importer

class Test:

    subfolder = 'strategy_test/'

    def check_one_byte(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        one_byte = OneByteStrategy()
        for i in range(256):
            output = one_byte.search(trace)
            assert(output[3] == i)
        output = one_byte.search(trace)
        assert(output == None)

    def check_random_taint(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        random = RandomTaintStrategy()
        output = random.search(trace)
        assert(output == None)
        trace.increaseConditionCounter()
        output = random.search(trace)
        assert(output[3] != trace.getInput()[3])

    def check_random(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        random = RandomStrategy()
        output = random.search(trace)
        assert(output != trace.getInput())

    def check_magic_byte_1(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        mb = MagicByteStrategy()
        output = mb.search(trace)
        assert(output == b'test\xde\xad\xbe\xef')

    def check_magic_byte_2(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        mb = MagicByteStrategy()
        output = mb.search(trace)
        assert(output != b'test\xde\xad\xbe\xef')

    def check_length_1(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        length = LengthTaintStrategy()
        output = length.search(trace)
        assert(len(output) > len(trace.getInput()))

    def check_length_2(self, folder: str):
        importer = Importer(folder)
        trace = importer.get_file_contents()[0]
        length = LengthStrategy()
        output = length.search(trace)
        assert(len(output) == 0)
        output = length.search(trace)
        assert(len(output) == 100)

    def run_all(self):
        self.check_length_1(self.subfolder + 'length_1/')
        self.check_length_2(self.subfolder + 'length_2/')
        self.check_magic_byte_1(self.subfolder + 'magic_1/')
        self.check_one_byte(self.subfolder + 'one_byte/')
        self.check_random_taint(self.subfolder + 'random_taint/')
        self.check_random(self.subfolder + 'random/')