import os
import configparser
import logging

class Config(object):

  def __init__(self):
    self.cfg = configparser.ConfigParser()
    self.cfg.add_section("fs-uae")
    self.cfg.set("fs-uae", "data-dir", "~/Documents/FS-UAE")
    self.cfg.set("fs-uae", "bin-dev-dir", "~/fs-uae-dev")
    self.cfg.set("fs-uae", "bin-rel-dir", "~/fs-uae-dev")

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

  def set_bin_dev_dir(self, bin_dir):
    if bin_dir is not None:
      self.cfg.set("fs-uae", "bin-dev-dir", bin_dir)

  def get_bin_dev_dir(self):
    return os.path.expanduser(self.cfg.get('fs-uae', 'bin-dev-dir'))

  def set_bin_rel_dir(self, bin_dir):
    if bin_dir is not None:
      self.cfg.set("fs-uae", "bin-rel-dir", bin_dir)

  def get_bin_rel_dir(self):
    return os.path.expanduser(self.cfg.get('fs-uae', 'bin-rel-dir'))
