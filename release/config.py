import json
import os

import yaml


_DEFAULT_CONFIG = {
    "SECRET_KEY": os.urandom(24),
    "DEBUG": True,
}
APP_NAME = "release"

class Config:
    def __init__(self):
        config_path = os.environ.get(f"{APP_NAME}_CONFIG_PATH")
        config_json = os.environ.get(f"{APP_NAME}_CONFIG_JSON")
        for key in _DEFAULT_CONFIG:
            self.set(key, _DEFAULT_CONFIG[key])
        print("Preloaded default config")
        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf8") as f:
                entries = yaml.load(f, Loader=yaml.FullLoader)
                self.__dict__.update(entries)
            print(f"Loaded config from file: {self.__dict__}")
        elif config_json:
            self.__dict__.update(json.loads(config_json))
            print(f"Loaded config from json: {self.__dict__}")

    def get(self, key, defalut=None):
        return self.__dict__.get(key, defalut)

    def set(self, key, value):
        self.__dict__[key] = value


config = Config()
