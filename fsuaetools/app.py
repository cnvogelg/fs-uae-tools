import argparse
import logging

from .config import Config
from .run import Runner

class App(object):

  FORMAT='%(asctime)-15s  %(levelname)-6s  %(message)s'

  def __init__(self, description):
    self.parser = argparse.ArgumentParser(description)
    self.args = None
    self._add_logging_options()
    self._add_runner_options()
    self.cfg = Config()
    self.runner = None

  def _add_logging_options(self):
    """add logging options (-v, -q, -L) to an argparse"""
    grp = self.parser.add_argument_group("logging")
    grp.add_argument('-v', '--verbose', action='count', default=0,
                     help="be more verbose")
    grp.add_argument('-q', '--quiet', action='store_true', default=False,
                     help="be totally quiet")
    grp.add_argument('-L', '--log-file', default=None,
                     help="write tool output to log file")

  def _add_runner_options(self):
    grp = self.parser.add_argument_group("runner")
    grp.add_argument('-C', '--config-file', default=None,
                     help='path of the configuration file')
    grp.add_argument('-b', '--bin-name', default=None,
                     help='overwrite name of FS-UAE binary')
    grp.add_argument('-V', '--fs-uae-version', default=None,
                     help='Select FS-UAE version to run if bin-dir contains multiple')
    grp.add_argument('-F', '--data-dir', default=None,
                     help='FS-UAE data directory, e.g. ~/Documents/FS-UAE')
    grp.add_argument('-B', '--bin-dir', default=None,
                     help='overwrite FS-UAE binary directory')

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
    self.cfg.set_bin_dir(self.args.bin_dir)
    self.cfg.set_bin_name(self.args.bin_name)

  def get_args(self):
    return self.args

  def get_config(self):
    return self.cfg

  def setup(self, bin_dir=None, data_dir=None):
    cfg = self.cfg
    args = self.args
    runner = Runner()
    # pick binary dir
    if bin_dir is None:
      # try to find binary first
      bin_dir = runner.find_bin_dir(cfg.get_bin_dir(), ver=args.fs_uae_version)
      # fallback to default dir
      if bin_dir is None:
        bin_dir = runner.get_default_bin_dir()
    # pick data dir
    if data_dir is None:
      data_dir = cfg.get_data_dir()
    # setup runner
    runner.setup(bin_dir, data_dir, cfg.get_bin_name())
    self.runner = runner

  def get_fs_uae_bin(self):
    return self.runner.get_fs_uae_bin()

  def run(self, *args, cfg_file=None, log_stdout=False):
    self.runner.run(*args, cfg_file=cfg_file, log_stdout=log_stdout)

  def start(self, *args, cfg_file=None, log_stdout=False):
    self.runner.start(*args, cfg_file=cfg_file, log_stdout=log_stdout)

  def stop(self):
    self.runner.stop()

  def is_running(self):
    return self.runner.is_running()
