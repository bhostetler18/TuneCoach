import unittest
from unittest.mock import Mock
from unittest.mock import patch
from tkinter import *
from collections import deque

from TuneCoach.gui.MainController import MainController
from TuneCoach.gui.Session import load_session

class TestMainController(unittest.TestCase):
    def setUp(self):
        self.root = Mock()
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

    def test_load_from_when_path_not_valid(self):
        with patch.object(self.root, 'perform_load', return_value=(None, True)):
            actual_return_value = self.mainController.load_from()
            self.assertEqual(False, actual_return_value)

    # def test_load_from_when_session_is_none(self):
        # with patch.object()
        # load_session.

if __name__ == '__main__':
    # root = Tk()
    # mainController = MainController(root)
    unittest.main()