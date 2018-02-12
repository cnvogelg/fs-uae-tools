import argparse
import logging

from .config import Config

class App(object):

  FORMAT='%(asctime)-15s  %(levelname)-6s  %(message)s'

  def __init__(self, description):
    self.parser = argparse.ArgumentParser(description)
    self.args = None
    self._add_logging_options()
    self._add_runner_options()
    self.cfg = Config()

  def _add_logging_options(self):
    """add logging options (-v, -q, -L) to an argparse"""
    self.parser.add_argument('-v', '--verbose', action='count', default=0,
                             help="be more verbose")
    self.parser.add_argument('-q', '--quiet', action='store_true', default=False,
                             help="be totally quiet")
    self.parser.add_argument('-L', '--log-file', default=None,
                             help="write tool output to log file")

  def _add_runner_options(self):
    self.parser.add_argument('-C', '--config-file', default=None,
                        help='path of the configuration file')
    self.parser.add_argument('-d', '--dev-binary', default=False, action='store_true',
                        help='use development binary (otherwise release)')
    self.parser.add_argument('-s', '--sys-binary', default=False, action='store_true',
                        help='use system binary')
    self.parser.add_argument('-V', '--fs-uae-version', default=None,
                        help='Select FS-UAE version to run')
    self.parser.add_argument('-F', '--data-dir', default=None,
                        help='FS-UAE data directory, e.g. ~/Documents/FS-UAE')
    self.parser.add_argument('-D', '--bin-dev-dir', default=None,
                        help='FS-UAE binary directory of development builds')
    self.parser.add_argument('-R', '--bin-rel-dir', default=None,
                        help='FS-UAE binary directory of release builds')

  def _setup_logging(self):
    # setup level
    if self.args.quiet:
      level = 100
    elif self.args.log_file is not None:
      level = logging.DEBUG
    else:
      v = self.args.verbose
      if v == 0:
        level = logging.WARN
      elif v == 1:
        level = logging.INFO
      else:
        level = logging.DEBUG
    # setup logging
    logging.basicConfig(format=self.FORMAT, filename=self.args.log_file, level=level)

  def get_parser(self):
    return self.parser

  def parse_args(self):
    # parse
    self.args = self.parser.parse_args()
    # setup logging
    self._setup_logging()
    # read config
    self.cfg.read(self.args.config_file)
    # overwrite values given by args
    self.cfg.set_data_dir(self.args.data_dir)
    self.cfg.set_bin_dev_dir(self.args.bin_dev_dir)
    self.cfg.set_bin_rel_dir(self.args.bin_rel_dir)

  def get_args(self):
    return self.args

  def get_config(self):
    return self.cfg
