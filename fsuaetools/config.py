import os
import configparser
import logging

class Config(object):

  def __init__(self):
    self.cfg = configparser.ConfigParser()
    self.cfg.add_section("fs-uae")
    self.cfg.set("fs-uae", "data-dir", "~/Documents/FS-UAE")
    self.cfg.set("fs-uae", "bin-dir", "")
    self.cfg.set("fs-uae", "bin-name", "")
    self.cfg.add_section("cli")
    self.cfg.set("cli", "work-dir", "~/.fs-uae-cli")
    self.cfg.set("cli", "wb-root", "~/amiga/Workbench3.1")

  def read(self, cfg_path=None):
    if cfg_path is None:
      cfg_path = os.path.expanduser("~/.fs-uae.cfg")
    logging.info("reading config file '%s'", cfg_path)
    self.cfg.read(cfg_path)

  def set_data_dir(self, data_dir):
    if data_dir is not None:
      self.cfg.set("fs-uae", "data-dir", data_dir)

  def get_data_dir(self):
    return os.path.expanduser(self.cfg.get('fs-uae', 'data-dir'))

  def set_bin_dir(self, bin_dir):
    if bin_dir is not None:
      self.cfg.set("fs-uae", "bin-dir", bin_dir)

  def get_bin_dir(self):
    return os.path.expanduser(self.cfg.get('fs-uae', 'bin-dir'))

  def set_bin_name(self, bin_name):
    if bin_name is not None:
      self.cfg.set("fs-uae", "bin-name", bin_name)

  def get_bin_name(self):
    return self.cfg.get('fs-uae', 'bin-name')

  # cli

  def set_cli_work_dir(self, work_dir):
    if work_dir is not None:
      self.cfg.set("cli", "work-dir", work_dir)

  def get_cli_work_dir(self):
    return os.path.expanduser(self.cfg.get('cli', 'work-dir'))

  def set_cli_wb_root(self, work_dir):
    if work_dir is not None:
      self.cfg.set("cli", "wb-root", work_dir)

  def get_cli_wb_root(self):
    return os.path.expanduser(self.cfg.get('cli', 'wb-root'))
