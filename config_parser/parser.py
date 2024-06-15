import configparser


class ConfigParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get(self, section, key):
        return self.config.get(section, key)
