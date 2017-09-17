'''Generates a logfile. Each line comes from the randomLineGenerator'''
import random
from datetime import datetime
import sys
import argparse
import time
import os

# We save all the possible values
status = [101, 103, 200, 203, 301, 404, 502]
method = ['GET', 'POST', 'PUT', 'DELETE']
section = ['/program','/users','/directs','/load.php','/img','/index.php','/videos','/robots.txt']
clients = ['127.168.0.1', '127.168.0.2', '127.168.0.3', '127.168.0.4', '127.168.0.5', '127.168.0.6']

def randomLineGenerator():
    # Randomly chooses the values
    line = random.choice(clients)+" - -  ["
    # Puts the data into the right format
    date = datetime.now().strftime("%d/%b/%Y:%H:%M:%S") 
    date+=' +0100] "'
    line+=date
    line+=random.choice(method)+' '+random.choice(section)+ ' HTTP/1.1" '
    line+=str(random.choice(status))
    # We also have to choose the bytes randomly
    line+=' '+str(random.randint(0, 7000))+' "-" "Mozilla/5.0 (compatible; AimenBot/1.0; +http://www.mycoolwebsite.com/bot.html)"' 
    return line
    
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='HTTP log generator')
    p.add_argument('logfile', help='Choose the logfile for which you want to generate log entries')
    args = p.parse_args()   
    try:     
        while True:
            with open(args.logfile, 'a') as file:
                # We generate a line, write it and then wait a certain amount of time
                a=randomLineGenerator()
                file.write(a+os.linesep)
                time.sleep(random.randint(0,3))
    except KeyboardInterrupt:
        sys.exit(0)
