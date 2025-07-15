from abc import ABC


class ETLTask(ABC):
    def __init__(self, config: dict):
        self.config = config

    def run(self):
        raise NotImplementedError
    


class Parser(ABC):
    def __init__(self, config: dict):
        self.config = config

    def parse(self):
        raise NotImplementedError