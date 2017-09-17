from datetime import datetime, timezone
# a log line is formatted as follows: 
# '68.259.66.4 - - [21/Mar/2016:22:59:27 +0100] "GET /robots.txt HTTP/1.1" 103 7896 "-" "Mozilla/5.0 (compatible; AhrefsBot/5.0; +http://ahrefs.com/robot/)"'

class LogEntry:
    '''Represents an entry in the log. This usually is a single line from the log'''
   
    # logLine is a line from the log file
    def __init__(self, logLine):
        # Stores the logLine
        self.str=logLine 
        # Removes the spaces. Since most entries are separated by spaces, this may be simpler than using regular expressions
        l=logLine.split() 
        # Wrong format
        if (len(l)!=9 or len(l)!=15):
            # We save a boolean 'parsed' to know if the entry was treated already
            self.parsed=False
        # Saves the Host
        self.host=l[0]
        # Saves the ID
        self.ident=l[1]
        # The User
        self.user=l[2]
        # We start extracting the time
        tempTime=" ".join([l[3],l[4]])
        # Removes the brackets
        self.time=tempTime[1:-1]
        # Convert into a datetime object, more convenient
        self.date=datetime.strptime(self.time, "%d/%b/%Y:%H:%M:%S %z") 
        tempRequest=" ".join([l[5],l[6],l[7]])
        # Removes the quotation mark
        self.request = tempRequest[1:-1]
        # We need the section separately for the stats
        self.section=l[6]
        # We need the methods also
        self.method=l[5][1::]
        # We save the status and bytes
        self.status=l[8]
        self.bytes=l[9]
        # Boolean twhich saves whether or not there are a referer and a user agent
        self.refagentExist=False
        self.parsed = True
        
        # Checks if the referer and user agent exitst
        if (len(l)==15):
            self.referer=l[10][1:-1]
            tempUserAgent=" ".join([l[11],l[12],l[13],l[14]])
            self.userAgent=tempUserAgent[1:-1]
            self.refagentExist=True
    
    
    def __str__(self):
        if (self.parsed):
            h = " ".join([self.host,
                            self.ident,
                            self.user,
                            '['+self.time+']',
                            '"'+self.request+'"',
                            self.status,
                            self.bytes])
            if (self.refagentExist):
                h+= " ".join([' "'+self.referer+'"',
                            '"'+self.userAgent+'"'])
        else:
            h="Not a log entry !"
        return h
                        

        