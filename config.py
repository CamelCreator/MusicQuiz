import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('config.default.ini')
    config.read('config.ini')
    return config
