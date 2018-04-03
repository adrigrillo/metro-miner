"""
Metro Miner
==================================
metro-miner is an twitter miner that search for information related to the madrid metro
and saves it to a database
"""
# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '0.1.dev'

import configparser
import json
import logging.config
import os

auth_config = configparser.ConfigParser()
auth_config.read('authentication.ini')
config = configparser.ConfigParser()
config.read('config.ini')


def setup_logging(config_file_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    :param config_file_path: logging configuration file path
    :param default_level: default logging level
    :param env_key: environment key that contain the logging configuration file path
    :return:
    """
    path = config_file_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            log_config = json.load(f)
        logging.config.dictConfig(log_config)
    else:
        logging.basicConfig(level=default_level)
