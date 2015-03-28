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

    def myBot_vs_Other(self, myBotName, otherBotName, map="2_PointOfPeril.map"):
        # test my bot against demo bot
        cmd =  os.getcwd() + '\\run.bat'
        myBot = ".\\bots\\" + myBotName
        otherBot = ".\\bots\\" + otherBotName

        folder = os.getcwd() + "\\..\\"
        mapfile = os.getcwd() + "\\maps\\" + map

        filename = myBotName.rsplit(".")[0] + "_" + otherBotName.rsplit(".")[0]
        f_out_name = ".\\logs\\" + filename + "_out.txt"
        f_err_name = ".\\logs\\" + filename + "_err.txt"
        f_out = open(f_out_name, 'w')
        f_err = open(f_err_name, 'w')

        #params = [cmd, myBot, otherBot, mapoption, map]
        #print params
        params = [cmd, myBot, otherBot, mapfile]
        print params
        with open(f_out_name, 'w') as outfile:
            with open(f_err_name, 'w') as errfile:
                subprocess.call(subprocess.list2cmdline(params), cwd=folder, stdout=outfile, stderr=errfile)

        #self.assertTrue(myBotName.rsplit(".")[0] in tail(f_out_name,1)[0], "Oh oh We lost this game")
        print tail(f_out_name,1)[0]
        print tail(f_out_name,2)[0]
        self.assertTrue(file_len(f_err_name) == 1, "One bot had en error ")
        if myBotName == 'my_bot.py':
            self.assertTrue("player 1" in tail(f_out_name,1)[0], "Oh oh We lost this game")
        else:
            if otherBotName == 'my_bot.py':
                self.assertTrue("player 2" in tail(f_out_name,1)[0], "Oh oh We lost this game")


    '''
    def test_Demo9_vs_Demo9(self):
        self.myBot_vs_Other("demoBot9.py", "demoBot9.py")

    def test_Demo8_vs_Demo8(self):
        self.myBot_vs_Other("demoBot8.py", "demoBot8.py")

    def test_Demo7_vs_Demo7(self):
        self.myBot_vs_Other("demoBot7.py", "demoBot7.py")

    def test_Demo6_vs_Demo6(self):
        self.myBot_vs_Other("demoBot6.py", "demoBot6.py")

    '''
    def test_My_vs_Demo9(self):
        self.myBot_vs_Other("my_bot.py", "demoBot9.py")

    def test_Demo9_vs_My(self):
        self.myBot_vs_Other("my_bot.py", "demoBot9.py")

    def test_My_vs_Last(self):
        self.myBot_vs_Other("my_bot.py", "last_bot.py")

    def test_Last_vs_My(self):
        self.myBot_vs_Other("last_bot.py", "my_bot.py")



    def test_My_vs_New(self):
        self.myBot_vs_Other("my_bot.py", "new_bot.py")

    def test_New_vs_My(self):
        self.myBot_vs_Other("new_bot.py", "my_bot.py")

    def test_My_vs_My(self):
        self.myBot_vs_Other("my_bot.py", "my_bot.py")

    def test_Pirates_vs_Cloak(self):
        self.myBot_vs_Other("pirates_example.py", "cloak_example.py")

    def test_Island_vs_Location(self):
        self.myBot_vs_Other("location_example.py", "island_example.py")

    def test_My_vs_Misc(self):
        self.myBot_vs_Other("pirates_example.py", "misc_example.py")




if __name__ == '__main__':
    unittest.main()