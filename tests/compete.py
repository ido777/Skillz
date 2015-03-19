import subprocess
import unittest
import sys
import os
import logging
from subprocess import Popen


# Add to the system path the folder that include Pirates files
sys.path.append(".")
sys.path.append("..\\")
sys.path.append(os.getcwd() + "\\..\\lib")
sys.path.append(os.getcwd() + "\\..\\bots")

os.chdir("..")
print "Working Dir " , os.getcwd()


def file_len(fname):
    i = 0
    with logging.codecs.open(fname,'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def tail(fname, len):
    file_length = file_len(fname)
    tail = []
    with logging.codecs.open(fname,'r') as f:

        for i, l in enumerate(f):
            if i >= file_length -len:
                tail.append(l)

    return tail

class TestPiratesBot(unittest.TestCase):

    def setUp(self):
        self.myBot = "myBot.py"

    def myBot_vs_Other(self, myBotName, otherBotName):
        # test my bot against demo bot
        cmd =  os.getcwd() + '\\run.bat'
        myBot = ".\\bots\\" + myBotName
        otherBot = ".\\bots\\" + otherBotName
        folder = os.getcwd() + "\\..\\"

        filename = myBotName.rsplit(".")[0] + "_" + otherBotName.rsplit(".")[0]
        f_out_name = filename + "_out.txt"
        f_err_name = filename + "_err.txt"
        f_out = open(f_out_name, 'w')
        f_err = open(f_err_name, 'w')

        params = [cmd, myBot, otherBot]

        with open(f_out_name, 'w') as outfile:
            with open(f_err_name, 'w') as errfile:
                subprocess.call(subprocess.list2cmdline(params), cwd=folder, stdout=outfile, stderr=errfile)

        #self.assertTrue(myBotName.rsplit(".")[0] in tail(f_out_name,1)[0], "Oh oh We lost this game")
        self.assertTrue("player 1" in tail(f_out_name,1)[0], "Oh oh We lost this game")
        self.assertTrue(file_len(f_err_name) == 1, "One bot had en error ")


    def test_myBot_vs_Demo1(self):
        self.myBot_vs_Other("MyBot.py", "demoBot1.pyc")

    def test_myBot_vs_Demo2(self):
        self.myBot_vs_Other("MyBot.py", "demoBot2.pyc")

    def test_myBot_vs_Demo3(self):
        self.myBot_vs_Other("MyBot.py", "demoBot3.pyc")

    def test_myBot_vs_Demo4(self):
        self.myBot_vs_Other("MyBot.py", "demoBot4.pyc")




if __name__ == '__main__':
    unittest.main()