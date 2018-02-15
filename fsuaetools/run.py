import os
import sys
import platform
import logging
import glob
import subprocess

class Runner(object):

  def __init__(self):
    self.data_dir = None
    self.fs_uae_bin = None
    self.proc = None

  def get_os_dir(self):
    """get os directory of FS-UAE"""
      # get os
    if sys.platform.startswith('darwin'):
      return "macos"
    elif sys.platform.startswith('linux'):
      return "linux"
    elif sys.platform.startswith('win32'):
      return "windows"
    else:
      return None

  def get_arch(self):
    """return arch string for current machine"""
    machine = platform.machine().lower()
    bits = platform.architecture()[0]
    if machine in ["x86_64", "amd64", "i386", "i486", "i585", "i686"]:
      if bits == "32bit":
        return "x86"
      elif bits == "64bit":
        return "x86-64"
    elif machine.startswith("power"):
      if bits == "32bit":
        return "ppc"

  def get_default_bin_dir(self):
    if sys.platform.startswith('darwin'):
      return "/Applications"
    elif sys.platform.startswith('linux'):
      return "/usr/bin"
    elif sys.platform.startswith('win32'):
      return os.path.join(os.environ['ProgramFiles'],"FS-UAE")

  def get_default_bin_name(self):
    if sys.platform.startswith('win32'):
      return "fs-uae.exe"
    elif sys.platform.startswith('darwin'):
      return "FS-UAE.app/Contents/MacOS/fs-uae"
    else:
      return "fs-uae"

  def find_bin_dir(self, base_dir, os_name=None, arch=None, ver=None):
    """find the binary file in the given bin dir"""
    ver_glob = ver + "*" if ver is not None else "*"
    if base_dir is None:
      raise ValueError("invalid base_dir: " + base_dir)
    if os_name is None:
      os_name = self.get_os_dir()
      if os_name is None:
        raise ValueError("invalid os_name: " + os_name)
    if arch is None:
      arch = self.get_arch()
      if arch is None:
        raise ValueError("invalid arch: " + arch)

    # auto add 'dist'/os_name
    bd = os.path.join(base_dir, "dist", os_name)
    if os.path.isdir(bd):
      base_dir = bd

    glob_name = "fs-uae_" + ver_glob + "_" + os_name + "_" + arch
    logging.debug("globbing: pattern='%s'", glob_name)
    glob_path = os.path.join(base_dir, glob_name)
    files = glob.glob(glob_path)
    logging.debug("globbing: path='%s' -> %s", glob_path, files)
    n = len(files)
    if n == 0:
      return None
    elif n == 1:
      return files[0]
    else:
      # sort by age
      files = sorted(files, key=lambda x: os.stat(x).st_mtime)
      return files[-1]

  def setup(self, bin_dir, data_dir=None, bin_name=None):
    # check data dir
    if data_dir is None:
      data_dir = os.path.expanduser("~/Documents/FS-UAE")
    logging.info("data directory: '%s'", data_dir)
    if not os.path.isdir(data_dir):
      logging.error("FS-UAE data directory not found: %s", data_dir)
      raise IOError("data directory not found!")

    # check bin dir
    logging.info("binary directory: '%s'", bin_dir)
    if bin_dir is None or not os.path.isdir(bin_dir):
      logging.error("FS-UAE binary directory not found: %s", bin_dir)
      raise IOError("bin dir not found!")

    # binary name
    if bin_name is None:
      bin_name = self.get_default_bin_name()
    logging.info("binary name: '%s'", bin_name)

    # final binary
    fs_uae_bin = os.path.join(bin_dir, bin_name)
    logging.info("FS-UAE binary: '%s'", fs_uae_bin)
    if not os.path.isfile(fs_uae_bin) or not os.access(fs_uae_bin, os.X_OK):
      logging.error("FS-UAE binary not found: %s", fs_uae_bin)
      raise IOError("fs-uae binary not found!")

    # store binary
    self.data_dir = data_dir
    self.fs_uae_bin = fs_uae_bin

  def get_fs_uae_bin(self):
    return self.fs_uae_bin

  def _get_cfg_path(self, cfg_file):
    # launch with config?
    if cfg_file is not None:
      if not cfg_file.endswith(".fs-uae"):
        cfg_file = cfg_file + ".fs-uae"
      if not os.path.isabs(cfg_file) or not os.path.exists(cfg_file):
        cfg_file = os.path.join(self.data_dir, "Configurations", cfg_file)
      logging.info("config file: '%s'", cfg_file)
      if not os.path.isfile(cfg_file):
        logging.error("Can't find config file: '%s'", cfg_file)
        raise IOError("can't find config file!")
    return cfg_file

  def _get_cmd_line(self, args, cfg_file, log_stdout):
    # build command line
    cmd = [self.fs_uae_bin]
    # log to stdout
    if log_stdout:
      cmd.append('--stdout')
    # extra options
    cmd += args
    # config file
    if cfg_file is not None:
      cmd.append(self._get_cfg_path(cfg_file))
    return cmd

  def run(self, *args, cfg_file=None, log_stdout=False):
    cmd = self._get_cmd_line(args, cfg_file, log_stdout)
    logging.info("run cmd: %r", cmd)
    # launch fs-uae
    try:
      return subprocess.call(cmd)
    except KeyboardInterrupt:
      print("*** Abort")

  def start(self, *args, cfg_file=None, log_stdout=False):
    cmd = self._get_cmd_line(args, cfg_file, log_stdout)
    logging.info("start cmd: %r", cmd)
    self.proc = subprocess.Popen(cmd)

  def stop(self):
    if self.proc is None:
      return
    logging.info("stop proc")
    # still running?
    if self.proc.poll() is None:
      logging.info("terminate proc")
      self.proc.terminate()
    self.proc = None
