# coding: utf8

import cheatsheet
import unittest
from workflow import Workflow

shortcuts = {
    "chrome":{
        "Open a new window":"⌘ + n",
        "Open a new window in Incognito mode":"⌘ + t",
    },
    "RES":{
        "Show help for keyboard shortcuts":"shift + /",
        "Launch RES command line.":"/",
        "Move up in posts":"j"
    }
}
cheatsheet.shortcuts = shortcuts

class TestCheatsheet(unittest.TestCase):

    def setUp(self):
        cheatsheet.wf = Workflow()

    def test_getApps(self):
        res = cheatsheet.getApps()
        self.assertListEqual(res, ['chrome', 'RES'])

    def test_getAppShortcuts(self):
        res = cheatsheet.getAppShortcuts('chrome')
        self.assertListEqual(res, ["Open a new window", "Open a new window in Incognito mode"])

    def test_getShortcut(self):
        res = cheatsheet.getShortcut("chrome","Open a new window")
        self.assertEqual(res, "⌘ + n")

    def test_addItems(self):
        res = cheatsheet.wf._items
        self.assertEqual(len(res),0)
        cheatsheet.addItems(['a','b'])
        res = cheatsheet.wf._items
        self.assertEqual(len(res),2)

    # # test get apps
    # def test_run_no_args(self):
    #     res = cheatsheet.wf._items
    #     self.assertEqual(len(res),0)
    #     cheatsheet.run([])
    #     self.assertEqual(len(res),2)
    #     #TODO check items are chrome and RES

    # def test_run_one_arg(self):
    #     res = cheatsheet.wf._items
    #     self.assertEqual(len(res),0)
    #     cheatsheet.run(["RES"])
    #     self.assertEqual(len(res),3)
    #     #TODO check items

    # def test_run_two_arg(self):
    #     res = cheatsheet.wf._items
    #     self.assertEqual(len(res),0)
    #     cheatsheet.run(["RES", "Move up in posts"])
    #     self.assertEqual(len(res),1)

if __name__ == '__main__':
    unittest.main()