
import unittest
from watchman.core import Watchman, Process
import subprocess

class TestCoreProcessSetup(unittest.TestCase):
  
  def test_process_from_config(self):
    p = Process("test/date-forever.sh")
    self.assertEqual(p.command, "test/date-forever.sh")

  def test_process_has_proc(self):
    p = Process({"run": "test/date-forever.sh"})
    self.assertIsInstance(p, subprocess.Popen)

class TestCoreWatchmanSetup(unittest.TestCase):

  def setUp(self):
    self.wm = Watchman()

  def test_watchman_init_none(self):
    # watchman initialised with no processes 
    self.assertEqual(len(self.wm.processes),0)



if __name__ == "__main__":
  unittest.main()
