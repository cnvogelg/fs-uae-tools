import os
import shutil
import logging


class WorkDir(object):

  def __init__(self, work_dir):
    self.work_dir = work_dir
    self.cfg_file = os.path.join(self.work_dir, "cfg.fs-uae")
    # create work dir
    self.fs_root = os.path.join(work_dir, "root")
    if not os.path.isdir(self.fs_root):
      logging.info("creating root dir: %s", self.fs_root)
      os.makedirs(self.fs_root)
    else:
      logging.info("found root dir: %s", self.fs_root)

  def get_fs_root(self):
    return self.fs_root

  def get_cfg_file_name(self):
    return self.cfg_file

  def create_dirs(self, dirs):
    # setup dirs
    for d in dirs:
      dp = os.path.join(self.fs_root, d)
      if not os.path.isdir(dp):
        logging.info("create sub dir: %s", d)
        os.makedirs(dp)
      else:
        logging.info("found sub dir: %s", d)

  def copy_files(self, src_dir, files, force=False):
    # setup files from wb root
    for f in files:
      src = os.path.join(src_dir, f)
      dst = os.path.join(self.fs_root, f)
      dst_dir = os.path.dirname(dst)
      if not os.path.isdir(dst_dir):
        logging.info("create sub dir: %s", dst_dir)
        os.makedirs(dst_dir)
      if not os.path.isfile(dst) or force:
        if os.path.exists(dst):
          os.remove(dst)
        shutil.copy(src, dst)
        logging.info("copy: %s -> %s", src, dst)

  def copy_file(self, src_file, dst_path, force=False):
    name = os.path.basename(src_file)
    dst_dir = os.path.join(self.fs_root, dst_path)
    dst = os.path.join(dst_dir, name)
    if not os.path.isdir(dst_dir):
      logging.info("create sub dir: %s", dst_dir)
      os.makedirs(dst_dir)
    if not os.path.isfile(dst) or force:
      if os.path.exists(dst):
        os.remove(dst)
      shutil.copy(src_file, dst)
      logging.info("copy: %s -> %s", src_file, dst)

  def create_mountlist(self, lines):
    ml_path = os.path.join(self.fs_root, "Devs", "MountList")
    logging.info("creating mountlist")
    with open(ml_path, "w") as fh:
      for l in lines:
        fh.write(l + "\n")

  def create_startup_sequence(self, lines):
    ss_path = os.path.join(self.fs_root, "S", "Startup-Sequence")
    logging.info("creating startup-sequence")
    with open(ss_path, "w") as fh:
      for l in lines:
        fh.write(l + "\n")

  def create_shell_startup(self, lines):
    ss_path = os.path.join(self.fs_root, "S", "Shell-Startup")
    logging.info("creating shell-startup")
    with open(ss_path, "w") as fh:
      for l in lines:
        fh.write(l + "\n")

  def create_fsuae_config(self, lines):
    logging.info("creating fsuae config")
    with open(self.cfg_file, "w") as fh:
      fh.write("[config]\n")
      for l in lines:
        fh.write(l + "\n")
