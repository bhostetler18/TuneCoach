import unittest
from unittest.mock import Mock
from unittest.mock import patch
from tkinter import *
from collections import deque

import TuneCoach.gui.MainWindow
from TuneCoach.gui.MainController import MainController
from TuneCoach.gui.MainWindow import MainWindow
# from TuneCoach.gui.MainWindow import MainWindow
# from TuneCoach.gui.MainWindow import invalid_path


# mainWindow.sayhi = Mock(return_value="foo")

class TestMainController(unittest.TestCase):
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

    def test_load_from_when_path_not_valid(self):
        # with patch.object(MainWindow, 'perform_load', return_value=(None, True)):
        with patch.object(MainWindow, 'perform_load', return_value=(None, True)):
        # mock_obj = Mock()
        # mock_obj.perform_load.return_value = (None, True)
            actual_return_value = self.mainController.load_from()
        # self.assertEqual(3, 3)
            self.assertEqual(False, actual_return_value)


if __name__ == '__main__':
    root = Tk()
    mainController = MainController(root)
    unittest.main()