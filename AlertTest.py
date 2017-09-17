import threading
import argparse
import os
import time
from LogRegistry import LogRegistry
from Display import Display
import LogGen

if __name__ == '__main__':
    with open('alerttest.txt', 'a') as file:
        a=LogGen.randomLineGenerator()
        file.write(a+os.linesep)
    reg = LogRegistry('alerttest.txt',9)
    displ = Display(reg)
    reg.parserManager.start()
    displ.displayUpdate.start()
    displ.stdscr.getch()
    displ.clearCurse()
    with open('alerttest.txt', 'a') as file:
        for i in range(10):
            a=LogGen.randomLineGenerator()
            file.write(a+os.linesep)
            time.sleep(1)
        