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

    def myBot_vs_Other(self, myBotName, otherBotName, map):
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

        params = [cmd, myBot, otherBot, mapfile, "--nolaunch" ]
        #print params
        with open(f_out_name, 'w') as outfile:
            with open(f_err_name, 'w') as errfile:
                subprocess.call(subprocess.list2cmdline(params), cwd=folder, stdout=outfile, stderr=errfile)

        #self.assertTrue(myBotName.rsplit(".")[0] in tail(f_out_name,1)[0], "Oh oh We lost this game")
        #self.assertTrue("player 1" in tail(f_out_name,1)[0], "Oh oh We lost this game")
        #self.assertTrue(file_len(f_err_name) == 1, "One bot had en error ")
        if "player 1" in tail(f_out_name,1)[0]:
            return 1
        else:
            return 0



    def test_find_best(self):
        files = [file for file in os.listdir(".\\bots\\") if file.endswith(".py") ]
        mapfiles = [file for file in os.listdir(".\\maps\\") if file.endswith(".map")]


        for candidate in ["my_bot.py"]:
            print "Candidate {0}\n 2= Win on both sides, 1= Win one side, 0 = Lose\n*****************".format(candidate)
            wins = 0
            for opponent in files:
                if opponent not in ["strategy.py", "my_bot.py"]:
                    for map in mapfiles:
                        win = self.myBot_vs_Other(candidate, opponent, map)
                        win = win + self.myBot_vs_Other(opponent, candidate, map)
                        print "{2} Candidate {0} vs {1} -  on map {3}".format(candidate, opponent, win, map)
                        wins += win
            print candidate + " got " + str(wins) + "wins"




if __name__ == '__main__':
    unittest.main()