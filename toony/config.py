import configparser


__config_file = 'config.ini'

__config = configparser.ConfigParser()
__config.optionxform = str

__config.read(__config_file)


def get(section: str, option: str):
    return __config.get(section, option, fallback=None)


def write(section: str, option: str, value: str):
    with open(__config_file, 'w') as file:
        __config.set(section, option, value)
        __config.write(file)
