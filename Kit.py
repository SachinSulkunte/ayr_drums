import json
import logging

from Instrument import Instrument
import Logger

SAMPLES_DIR = './samples/'
CONFIG_DIR = './configs/'

class Kit:
    def __init__(self, config_file):
        self.name = ""
        self.config = config_file
        self.instruments = []
        self.logger = Logger.MyLogger("Kit", log_level=logging.DEBUG)

    # create Instruments() from config
    def setup_instruments(self):
        with open(self.config, 'r') as file:
            kit_data = json.load(file)
        file.close()
        
        self.name = kit_data["name"]
        for name, params in kit_data["instruments"].items():
            filepath = SAMPLES_DIR + params["file"]
            component = Instrument(params["name"], filepath, params["position"], params["volume"])

            # add to list of instruments
            self.instruments.append(component)

    def print_kit_list(self):
        for instr in self.instruments:
            self.logger.info(instr.name)

    # return Instrument object by name
    def get_instrument_by_name(self, name):
        for instr in self.instruments:
            if name == instr.name:
                self.logger.info(instr)
                return instr    

# Example Usage:

# kit = Kit(CONFIG_DIR + "jazz_kit.json")
# kit.setup_instruments()
# kit.print_kit_list()
# ins = kit.get_instrument_by_name('snare')