import argparse
class ArgParse_Base:
    def __init__(self, text=''):
        self.parser = argparse.ArgumentParser(description=text)

    def add_argument(self):        
        args = self.parser.parse_args()
        return args
