from strategies.strategy import Strategy
import random
from trace import Trace
from helpers.utils import Util
import defs
class RandomTaintStrategy(Strategy):
#This class applies random char insertion, random char deletion and random bitflip to the input a random amount between 1 and 10


    def search(self, trace: Trace, index:int):
        #apply random number of random bitflips to bytes in offset
        condition = trace.getCondition(index)
        cur_input = trace.getInput()
        if len(condition.offsets) == 0:
            self.handler.logger.wrong(condition, defs.COMMENT_NO_OFFSETS)
            return None

        #We know the offset info, randomize first only the bytes in the offset
        while True:
            for cur_offset in range(len(condition.offsets)):
                begin = condition.offsets[cur_offset]['begin']
                end = condition.offsets[cur_offset]['end']
                for i in range(random.randrange(defs.MIN_RANDOM_MUTATIONS, defs.MAX_RANDOM_MUTATIONS)):
                    cur_input = cur_input[:begin] + Util.insert_random_character(bytes([])) + cur_input[end:]
            self.handler.run(condition, cur_input)
        self.handler.logger.wrong(condition, defs.COMMENT_TRIED_EVERYTHING)
        return None
        