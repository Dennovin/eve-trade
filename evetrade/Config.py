import argparse
import logging
import os
import pkg_resources
import simplejson

class Config(object):
    settings = None
    base_dir = "/opt/evetrade"
    config_file = os.path.join(base_dir, "etc", "settings.json")

    args = {
        "--config-file": {"dest": "config_file", "help": "Specify location of configuration file."},
        "--debug": {"dest": "debug", "action": "store_true", "help": "Display debugging information."},
        "--logfile": {"dest": "logfile", "help": "Output to log file instead of STDOUT."},
        }

    @classmethod
    def add_argument(cls, argname, **opts):
        cls.args[argname] = opts

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser()

        for k, v in cls.args.items():
            parser.add_argument(k, **v)

        args = parser.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        if args.logfile:
            logging.basicConfig(filename=args.logfile)

        if args.config_file:
            cls.config_file = args.config_file

        return args

    @classmethod
    def get(cls, item):
        cls.parse()
        if item in cls.settings:
            return cls.settings[item]

    @classmethod
    def parse(cls):
        if cls.settings is not None:
            return

        with open(cls.config_file, "r") as fh:
            contents = fh.read()
            cls.settings = simplejson.loads(contents)

    @classmethod
    def resource_filename(cls, fn):
        return pkg_resources.resource_filename(__name__, fn)
