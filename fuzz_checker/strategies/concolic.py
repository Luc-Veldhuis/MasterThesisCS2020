from strategies.strategy import Strategy
from trace import Trace
from cond_stmt import CondStmt
import os, subprocess, defs

class ConcolicStrategy(Strategy):
    

    def run_concolic(self, cur_input: bytes, condition: CondStmt):
        new_env = os.environ.copy()
        new_env['SYMCC_INPUT_FILE'] = defs.CONCOLIC_TMP_FOLDER + 'input'
        new_env['SYMCC_OUTPUT_DIR'] = defs.CONCOLIC_TMP_FOLDER + 'output/'
        with open(new_env['SYMCC_INPUT_FILE'], 'wb') as input_file:
            input_file.write(cur_input)
        if len(condition.offsets) > 0:
            symbolic_bytes = list(set([byte for o in condition.offsets for byte in range(o['begin'], o['end'])]))
            new_env['SYMCC_SYMBOLIC_BYTES'] = ",".join(map(str,symbolic_bytes))
            print(new_env['SYMCC_SYMBOLIC_BYTES'])
        client = subprocess.Popen([defs.CONCOLIC_BINARY, new_env['SYMCC_INPUT_FILE']], env=new_env)
        result = client.wait(30)

    def remove_old_files(self):
        for old_file in os.listdir(defs.CONCOLIC_TMP_FOLDER + 'output/'):
            if os.path.isfile(defs.CONCOLIC_TMP_FOLDER + 'output/' + old_file):
                os.remove(defs.CONCOLIC_TMP_FOLDER + 'output/' + old_file)
        if os.path.isfile(defs.CONCOLIC_TMP_FOLDER + 'input'):
            os.remove(defs.CONCOLIC_TMP_FOLDER + 'input')


    def search(self, trace: Trace):
        cur_input = trace.getInput()
        condition = trace.getCurrentCondition()
        self.remove_old_files()
        self.run_concolic(cur_input, condition)
        concolic_files = os.listdir(defs.CONCOLIC_TMP_FOLDER + 'output/')
        print("Generated: %d new inputs" % len(concolic_files))
        concolic_files.reverse()
        for new_input_file in concolic_files:
            if os.path.isfile(defs.CONCOLIC_TMP_FOLDER + 'output/' + new_input_file):
                with open(defs.CONCOLIC_TMP_FOLDER + 'output/' + new_input_file, 'rb') as new_input:
                    self.handler.run(condition, new_input.read())
        self.handler.logger.wrong(condition, "No flips found")
        return None