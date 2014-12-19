#!/usr/bin/python

from datetime import datetime, timedelta
import sys, os, re, time, subprocess

logFile = '/var/log/hostmon.log'

OK = 0
WARNING = 1
UNKNOWN = 3

#check if hostmon proc is running
def is_running(process):
    s = subprocess.Popen(["ps","axw"],stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process,x):
            return True
    return False

#check timestamp of hostmon.log
def check_TS():
    t = os.path.getmtime(logFile)
    #check if logfile updated in past 48 hours
    if(datetime.now() - datetime.fromtimestamp(t) > timedelta(hours=48)):
        #if lf_stale returns 'N' we're good
        lf_stale = 'Y'
    else:
        lf_stale = 'N'
    return lf_stale

def main():
    #first verify hostmon process is running
    hm_ok = is_running("hostmon.pl")
    if hm_ok == True:
        #verify logfile present in /var/log/hostmon.log
        if os.path.isfile(logFile):
            lf_stale = check_TS()
            if lf_stale == 'Y':
                print "WARNING - logfile not updated in last 48 hours."
                sys.exit(WARNING)
            elif lf_stale == 'N':
                print "OK - Hostmon service running and logfile OK."
                sys.exit(OK)
        else:
            print "WARNING - Hostmon logfile not found!"
            sys.exit(WARNING)
    elif hm_ok == False:
        print "WARNING - Hostmon service is not running!"
        sys.exit(WARNING)
    else:
        print "UNKNOWN - ERROR"
        sys.exit(UNKNOWN)

if __name__ == '__main__':
    main()
