import os
import sys
import termios
import tty
import select


class Shell(object):

  header = "New Shell process"
  footer = "Process {} ending"

  def __init__(self, conio, first_line_cb=None, check_exit_cb=None):
    self.conio = conio
    self.first_line_cb = first_line_cb
    self.check_exit_cb = check_exit_cb
    self.in_fd = sys.stdin.fileno()
    self.shell_num = None
    self.exit = False

  def start(self):
    self.old_settings = termios.tcgetattr(self.in_fd)
    tty.setraw(self.in_fd)

  def close(self):
    termios.tcsetattr(self.in_fd, termios.TCSADRAIN, self.old_settings)

  def _handle_line(self, s):
    keep_first = False
    first_line = None
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
          keep_first = self.first_line_cb()
        # shell header?
        if self.line.startswith(self.header):
          self.shell_num = int(self.line[-1])
        first_line = self.line + "\n"
      self.line = ""
    # check for shell exit
    if self.line == self.footer.format(self.shell_num):
      return False, False, first_line
    else:
      return True, keep_first, first_line

  def run(self, add_final_nl=True):
    self.line = ""
    self.first_line = True
    conio_fd = self.conio.fileno()
    stay = True
    show = False
    out = sys.stdout
    while stay:
      rl = select.select([self.in_fd, conio_fd],[],[], 0.5)[0]
      # shell output
      if conio_fd in rl:
        s = self.conio.read(1)
        # write to our console
        if show:
          out.write(s)
          out.flush()
        stay, keep_first, first_line = self._handle_line(s)
        if first_line is not None:
          show = True
        if keep_first:
          out.write(first_line)
          out.flush()
      # user input from stdin
      if self.in_fd in rl:
        c = sys.stdin.read(1)
        if ord(c[0]) == 127: # DEL
          c = chr(8) # Backspace
        self.conio.write(c)
      # check emu exit
      if self.check_exit_cb is not None:
        done = self.check_exit_cb()
        if done:
          stay = False
    if add_final_nl:
      out.write("\n\r")
