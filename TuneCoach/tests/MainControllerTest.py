import unittest
from unittest.mock import Mock
from tkinter import *
from collections import deque

from TuneCoach.gui.MainController import MainController
from TuneCoach.gui.MainWindow import MainWindow

MainWindow = Mock()

class MainControllerTest(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.mainController = MainController(self.root)

    def test_init(self):
        expected_threshold = 15
        expected_yellow_threshold = 35
        expected_is_paused = True
        expected_should_save = False
        expected_deque = deque([])

        expected_list = [expected_threshold, expected_yellow_threshold, expected_is_paused, expected_should_save, expected_deque]
        actual_list = [self.mainController.threshold, self.mainController.yellow_threshold, self.mainController.paused, self.mainController.should_save, self.mainController.queue]
        self.assertListEqual(expected_list, actual_list)

    def test_load_from(self):
        self.assertEqual(False, self.mainController.should_save)


if __name__ == '__main__':
    unittest.main()