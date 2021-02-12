import os
import io
import time
import yaml

import xlsxwriter


def get_config():
    with open("config.yaml") as f:
        result = yaml.safe_load(f)

    return result


config = get_config()
