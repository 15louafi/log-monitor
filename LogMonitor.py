import threading
import argparse
import time
from LogRegistry import LogRegistry
from Display import Display

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP log parser by LOUAFI Aïmen')
    parser.add_argument('-t', '--threshold', metavar='threshold', type=int, default = 1000, help='The threshold for the two minutes alarm')
    parser.add_argument('logfile', metavar='log file', help='The http log file')
    args = parser.parse_args()
    reg = LogRegistry(args.logfile,args.threshold)
    displ = Display(reg)
    reg.parserManager.start()
    displ.displayUpdate.start()
    displ.stdscr.getch()
    displ.clearCurse()
    
