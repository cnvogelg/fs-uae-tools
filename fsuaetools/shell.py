import os
import sys
import termios
import tty
import select


class Shell(object):

  def __init__(self, conio, first_line_cb=None):
    self.conio = conio
    self.first_line_cb = first_line_cb
    self.in_fd = sys.stdin.fileno()
    self.old_settings = termios.tcgetattr(self.in_fd)
    tty.setraw(self.in_fd)

  def close(self):
    termios.tcsetattr(self.in_fd, termios.TCSADRAIN, self.old_settings)

  def _handle_line(self, s):
    ch = ord(s)
    if (ch & 0x7f) >= 32 and ch != 127:
      self.line += s
    elif ch == 8: # backspace
      self.line = self.line[:-1]
    if s == '\n':
      # handle first line
      if self.first_line:
        self.first_line = False
        # call callback?
        if self.first_line_cb is not None:
          self.first_line_cb()
      # end shell mode?
      if "endcli" in self.line or "endshell" in self.line:
        return True
      self.line = ""

  def run_loop(self):
    self.line = ""
    self.first_line = True
    conio_fd = self.conio.fileno()
    stay = True
    out = sys.stdout
    while stay:
      rl = select.select([self.in_fd, conio_fd],[],[])[0]
      # shell output
      if conio_fd in rl:
        s = self.conio.read(1)
        # write to
        out.write(s)
        out.flush()
        if self._handle_line(s):
          stay = False
      # user input from stdin
      if self.in_fd in rl:
        c = sys.stdin.read(1)
        if ord(c[0]) == 127: # DEL
          c = chr(8) # Backspace
        self.conio.write(c)
    out.write("\rdone\r")
