
import subprocess
import sys

ON_POSIX = 'posix' in sys.builtin_module_names

class Process(subprocess.Popen):
  def __init__(self, cmd, name=None, *args, **kwargs):
     self.name = name
     self.command = cmd

     defaults = {
         'stdout': subprocess.PIPE,
         'stderr': subprocess.STDOUT,
         'shell': True,
         'bufsize': 1,
         'close_fds': ON_POSIX
     }
     defaults.update(kwargs)

     super(Process, self).__init__(cmd, *args, **defaults) 


class Watchman:
  def __init__(self):
    self.processes = []


