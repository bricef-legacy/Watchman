
import subprocess
import sys
import signal
import psutil

ON_POSIX = 'posix' in sys.builtin_module_names

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

class Process:
  def __init__(self, name, cmd, *args, **kwargs):
    self.popen = None
    self.name = name
    self.command = cmd
 
    self.popen_defaults = {
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
        'shell': True,
        'bufsize': 1,
        'close_fds': ON_POSIX
    }
    self.popen_defaults.update(kwargs)
    self.args = args
 

  def start(self):
    print("Starting: "+self.command+" "+str(self.popen_defaults))
    self.popen = psutil.Popen(self.command, **self.popen_defaults)
  
  @property
  def pid(self):
    if self.popen:
      return self.popen.pid

  def stop(self):
    if self.popen:
      self.popen.kill()
  
  def is_running(self):
    if self.popen:
      return self.popen.is_running()
    else:
      return False

class Watchman:
  def __init__(self):
    self.processes = []

  def add(self,process):
    self.processes.append(process)

