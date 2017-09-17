import curses
import threading
import time
from datetime import datetime
from LogRegistry import LogRegistry

class Display():
    """To display the stats on the console
    """

    def __init__(self, registry):
        """ Initialise the curse application
        """
        
        self.stdscr = curses.initscr()
        # We save the LogRegistry as attribute
        self.logRegistry = registry

        def displayUpdate():
            """ A function to display and update
            """
            while True:
                self.display()
                time.sleep(1)
        print("\x1b[8;48;200t")
        self.initialiseCurse()

        # We define a thread to call to update the display
        self.displayUpdate = threading.Thread(target=displayUpdate, daemon = True)
    
    def initialiseCurse(self):
        """ Generates the boxes
        """
        maxY, maxX = self.stdscr.getmaxyx()
        # We define option to add color
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Window to display total bytes and sizes
        totalStatsWindow = self.stdscr.subwin(int(maxY/15), int(maxX//1.8), 2, 2)
        totalStatsY, totalStatsX = totalStatsWindow.getmaxyx()
        totalStatsWindow.addstr(0,10,"Total hits :")
        totalStatsWindow.addstr(0,10+int(totalStatsX/3),"Total bytes : ")
        totalStatsWindow.addstr(0,20+int(totalStatsX/2),"Failed queries : ")
        
        # Window to display the values
        self.totalHitsWindow = totalStatsWindow.derwin(1,10,0,23)
        self.totalBytesWindow = totalStatsWindow.derwin(1,10,0,24+int(totalStatsX/3))
        self.failedQueriesWindow = totalStatsWindow.derwin(1,10,0,37+int(totalStatsX/2))
        
        # Window for the date
        self.dateWindow = self.stdscr.subwin(int(maxY/14),int(maxX//7), 2, int(maxX//1.5))
        self.dateWindow.border()
        
        # Window for the two minutes stats
        partialStatsWindow = self.stdscr.subwin(int(maxY/3.5),maxX-2, int(maxY//8), 2)
        partialStatsY, self.partialStatsX = partialStatsWindow.getmaxyx()
        partialStatsWindow.addstr(1,int(self.partialStatsX/2.5), "Last two minutes stats", curses.color_pair(1))
        partialStatsWindow.addstr(3,2,"Average hits/2mins : ", curses.color_pair(4))
        partialStatsWindow.addstr(3,int(self.partialStatsX/5),"Average Bytes/2mins : ", curses.color_pair(4))
        partialStatsWindow.addstr(3,int(self.partialStatsX/2.4),"Top sections : ", curses.color_pair(4))
        partialStatsWindow.addstr(3,int(self.partialStatsX/1.47),"Top hosts : ", curses.color_pair(4))
        partialStatsWindow.addstr(3,int(self.partialStatsX/1.17),"Top methods : ", curses.color_pair(4))
        
        # We write the data into lines
        self.firstLine =  partialStatsWindow.derwin(1,self.partialStatsX-2,5,1)
        self.secondLine =  partialStatsWindow.derwin(1,self.partialStatsX-2,7,1)
        self.thirdLine =  partialStatsWindow.derwin(1,self.partialStatsX-2,9,1)
        partialStatsWindow.border()
        
        # We also display the latest log entries within the 2 minutes time frame
        self.registryWindow = self.stdscr.subwin(int(maxY/4),maxX-4, int((maxY/20)+maxY/2.25), 2)
        self.registryWindow.border()
        self.registryWindow.scrollok(True)
        
        # And the alerts
        self.alertWindow = self.stdscr.subwin(int(maxY/4),maxX-4, int((maxY/20)+maxY/1.4), 2)
        self.alertWindow.border()


    def clearCurse(self):
        """ Clears the display
        """
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def display(self):
        """Displays the values
        """
        # Clears everything
        self.firstLine.clear()
        self.secondLine.clear()
        self.thirdLine.clear()
        self.totalHitsWindow.clear()
        self.totalBytesWindow.clear()
        self.failedQueriesWindow.clear()
        self.registryWindow.clear()
        self.alertWindow.clear()
        
        r= self.logRegistry
        # Writes total hits, total bytes, fails, date, average hits and average bytes
        self.totalHitsWindow.addstr(0,0, str(r.totalHits), curses.color_pair(3))
        self.totalBytesWindow.addstr(0,0, str(r.totalBytes), curses.color_pair(3))
        self.failedQueriesWindow.addstr(0,0, str(r.fails), curses.color_pair(1))
        self.dateWindow.addstr(1,2, datetime.now().strftime("%d/%b/%Y:%H:%M:%S"))
        self.firstLine.addstr(0,8,str(r.avgHits))
        self.firstLine.addstr(0,int(self.partialStatsX/4.5),str(r.avgBytes))
        
        # Then we have to display top 3 sections, hosts and methods
        t=r.sections.most_common(3)
        if(len(t)!=0):
            if(len(t)>=1):
                self.firstLine.addstr(0,int(self.partialStatsX/2.4),t[0][0]+' : '+str(t[0][1]))
            if(len(t)>=2):
                self.secondLine.addstr(0,int(self.partialStatsX/2.4),t[1][0]+' : '+str(t[1][1]))
            if(len(t)>=3):
                self.thirdLine.addstr(0,int(self.partialStatsX/2.4),t[2][0]+' : '+str(t[2][1]))
        t=r.hosts.most_common(3)
        if(len(t)!=0):
            if(len(t)>=1):
                self.firstLine.addstr(0,int(self.partialStatsX/1.52),t[0][0]+' : '+str(t[0][1]))
            if(len(t)>=2):
                self.secondLine.addstr(0,int(self.partialStatsX/1.52),t[1][0]+' : '+str(t[1][1]))
            if(len(t)>=3):
                self.thirdLine.addstr(0,int(self.partialStatsX/1.52),t[2][0]+' : '+str(t[2][1]))
        t=r.methods.most_common(3)
        if(len(t)!=0):
            if(len(t)>=1):
                self.firstLine.addstr(0,int(self.partialStatsX/1.17),t[0][0]+' : '+str(t[0][1]))
            if(len(t)>=2):
                self.secondLine.addstr(0,int(self.partialStatsX/1.17),t[1][0]+' : '+str(t[1][1]))
            if(len(t)>=3):
                self.thirdLine.addstr(0,int(self.partialStatsX/1.17),t[2][0]+' : '+str(t[2][1]))
        n = len(r.registry)
        
        # Update the registry display.
        if(n>0):
            self.registryWindow.addstr(0,0,'\n'.join(list(map(str,r.registry))))
            
        # Update the alerts
        self.alertWindow.addstr(2,2,r.alertLog,curses.color_pair(1))
        
        # And we refresh everything
        self.firstLine.refresh()
        self.secondLine.refresh()
        self.thirdLine.refresh()
        self.totalHitsWindow.refresh()
        self.totalBytesWindow.refresh()
        self.failedQueriesWindow.refresh()
        self.registryWindow.refresh()
        self.dateWindow.refresh()
        self.alertWindow.refresh()
                
        
        

