from datetime import datetime, timezone, timedelta
import threading
import time
from collections import Counter
from LogEntry import LogEntry

class LogRegistry():
    """This class saves all the logs file treated into dictionary. It also updates the dictionary based on changes on log files
    """
    def __init__(self, file, threshold):
        # The threshold for which we trigger the 'high traffic' alert
        self.threshold=threshold 
        # We save the logfile
        self.file=file
        # We store the last line read of the log
        self.lastLine=0
        # Save the raw logs
        self.registry=[]
        # Storing all the section hits for the past 2 mins
        self.sections = Counter()
        # Storing all the hosts for the past 2 mins
        self.hosts = Counter()
        # Storing the used methods 2 mins
        self.methods = Counter()
        # Total number of hits/entries
        self.totalHits=0
        # Average hits : 2 minutes time span
        self.avgHits=0
        # Incorrect queries
        self.fails = 0
        # Total number of bytes exchanged
        self.totalBytes = 0
        # Avg number of bytes : 2 mins
        self.avgBytes = 0
        # Saves if we are in state of alert
        self.alert = False
        # Saves all the alerts into a string
        self.alertLog = ""
        
        def register():
            """ A function that calls for the updates
            """
            while True:
                self.update()
                time.sleep(5)

        # A Thread in order to parse
        self.parserManager = threading.Thread(target=register, daemon = True)
        
    def addNewEntry(self, entry):
        """Adds a new Entry to the registry and updates the stats"""
        if entry.parsed:
            time = datetime.now()
            # We first update the total stats : bytes, total hits and fails
            self.totalHits+=1
            if (entry.bytes != "-"):
                self.totalBytes+=int(entry.bytes)
            # If status is between 401 and 499 then the query failed 
            if ((entry.status != "-") and (int(entry.status) > 400) and (int(entry.status) < 500)):
                self.fails+=1
            if (abs((entry.date.replace(tzinfo=None) - time).total_seconds()) < 120):
                # Then we check if it is within the 2 mins time frame and update
                self.registry.append(entry)
                self.sections[entry.section] += 1
                self.hosts[entry.host] += 1
                self.methods[entry.method] +=1
                self.avgHits += 1
                if (entry.bytes != "-"):
                    self.avgBytes += int(entry.bytes)
                    
    def deleteEntry(self):
        """Deletes the oldest entry (it's the first one) and updates stats"""
        entry = self.registry.pop(0)
        # Decrement the stats
        self.avgHits-=1
        if (entry.bytes != "-"):
            self.avgBytes-=int(entry.bytes)
        self.sections[entry.section] -= 1
        self.hosts[entry.host] -= 1
        self.methods[entry.method] -=1
    
    def addAlert(self):
        """Adds an alert"""
        alert = ("HIGH TRAFFIC generated an alert - hits = %d, triggered at [%s]\n"
                 % (self.avgHits,datetime.now().strftime("%d/%b/%Y:%H:%M:%S")))
        self.alertLog= self.alertLog + alert
        self.alert=True
    
    def removeAlert(self):
        """Removes an alert"""
        alert = ("The alert has stopped. The traffic has recovered at [%s]\n" 
                % datetime.now().strftime("%d/%b/%Y:%H:%M:%S")) 
        self.alertLog= self.alertLog + alert
        self.alert = False
                
            
    def update(self):
        """Updates the registry : removes the old entries, adds the new ones with addNewEntry"""
        with open(self.file, 'r') as log:
            count = 0
            for line in log:
                # We only read lines that have not yet been read
                if (count >= self.lastLine):
                    # We turn them into log entries
                    l=LogEntry(line)
                     # And add them to the registry
                    self.addNewEntry(l)
                count+=1
            # Updates the last read line
            self.lastLine=count
        # Now we have to remove the old entries
        time = datetime.now()
        while len(self.registry) != 0 and abs((self.registry[0].date.replace(tzinfo=None) - time).total_seconds()) > 120:
            self.deleteEntry()
        # Now we handle the alerts
        if (self.avgHits>self.threshold and not self.alert):
            self.addAlert()
        elif (self.avgHits<self.threshold and self.alert):
            self.removeAlert()
            

        
                    
                    
                    
                    
                    
                    
                    
