import unittest
from tkinter import *
from collections import deque

from TuneCoach.gui.MainController import MainController

def fun(x):
    return x+1

class MainControllerTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

    def test_init(self):
        root = Tk()
        mainController = MainController(root)
        expected_threshold = 15
        expected_yellow_threshold = 35
        expected_is_paused = True
        expected_should_save = False
        expected_deque = deque([])

        expected_list = [expected_threshold, expected_yellow_threshold, expected_is_paused, expected_should_save, expected_deque]
        actual_list = [mainController.threshold, mainController.yellow_threshold, mainController.paused, mainController.should_save, mainController.queue]
        self.assertListEqual(expected_list, actual_list)

    def test_(self):
        return 0


if __name__ == '__main__':
    unittest.main()