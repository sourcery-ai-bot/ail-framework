#!/usr/bin/python3

"""
The ``Domain``
===================


"""

import os
import sys
import time
import redis
import configparser

# Get Config file
config_dir = os.path.join(os.environ['AIL_HOME'], 'configs')
default_config_file = os.path.join(config_dir, 'core.cfg')
if not os.path.exists(default_config_file):
    raise Exception('Unable to find the configuration file. \
                    Did you set environment variables? \
                    Or activate the virtualenv.')

 # # TODO: create sphinx doc

 # # TODO: add config_field to reload

class ConfigLoader(object):
    """docstring for Config_Loader."""

    def __init__(self, config_file=None):
        self.cfg = configparser.ConfigParser()
        if config_file:
            self.cfg.read(os.path.join(config_dir, config_file))
        else:
            self.cfg.read(default_config_file)

    def get_redis_conn(self, redis_name, decode_responses=True): ## TODO: verify redis name
        return redis.StrictRedis( host=self.cfg.get(redis_name, "host"),
                                  port=self.cfg.getint(redis_name, "port"),
                                  db=self.cfg.getint(redis_name, "db"),
                                  decode_responses=decode_responses )

    def get_files_directory(self, key_name):
        directory_path = self.cfg.get('Directories', key_name)
        # full path
        if directory_path[0] != '/':
            directory_path = os.path.join(os.environ['AIL_HOME'], directory_path)
        return directory_path

    def get_config_str(self, section, key_name):
        return self.cfg.get(section, key_name)

    def get_config_int(self, section, key_name):
        return self.cfg.getint(section, key_name)

    def get_config_boolean(self, section, key_name):
        return self.cfg.getboolean(section, key_name)

    def has_option(self, section, key_name):
        return self.cfg.has_option(section, key_name)

    def has_section(self, section):
        return self.cfg.has_section(section)

    def get_all_keys_values_from_section(self, section):
        if section in self.cfg:
            return [
                (key_name, self.cfg.get(section, key_name))
                for key_name in self.cfg[section]
            ]

        else:
            return []
