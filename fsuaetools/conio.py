import os
import tty
import pty


class ConIOPty(object):

  def __init__(self):
    master, slave = pty.openpty()
    if master == -1 or slave == -1:
      raise IOError("no pty!")
    tty.setraw(slave)
    self.master = master
    self.slave = slave

  def close(self):
    os.close(self.master)
    os.close(self.slave)

  def ttyname(self):
    return os.ttyname(self.slave)

  def fileno(self):
    return self.master

  def read(self, size=1):
    buf = os.read(self.master, size)
    return buf.decode("ISO-8859-1")

  def write(self, s):
    buf = s.encode("ISO-8859-1")
    os.write(self.master, buf)
