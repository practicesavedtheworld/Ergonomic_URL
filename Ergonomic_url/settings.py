import yaml
import pathlib

CONFIG_PATH = pathlib.Path(__file__).parent.parent / 'config' / 'configuration.yaml'


def load_config():
    with open(CONFIG_PATH) as config_file:
        data = yaml.safe_load(config_file)
    return data

