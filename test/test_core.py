
import unittest
from watchman.core import Watchman, Process
import subprocess

class TestCoreProcessSetup(unittest.TestCase):
  
  def test_process_from_config(self):
    p = Process("test", "test/date-forever.sh")
    self.assertEqual(p.command, "test/date-forever.sh")

  def test_process_not_started(self):
    p = Process("test", "test/date-forever.sh")
    self.assertEqual(p.pid, None)
  
  def test_start_and_stop_process(self):
    p = Process("test", "test/date-forever.sh")
    p.start()
    self.assertTrue(p.is_running())
    p.stop()
    self.assertFalse(p.is_running())


    

class TestCoreWatchmanSetup(unittest.TestCase):

  def setUp(self):
    self.wm = Watchman()

  def test_watchman_init_none(self):
    # watchman initialised with no processes 
    self.assertEqual(len(self.wm.processes),0)
  
  def test_process_addition(self):
    self.wm.add(Process("test", "test/date-forever.sh"))
    self.assertEqual(len(self.wm.processes), 1)



