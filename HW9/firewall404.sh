#!/bin/sh
#HW9
#Dhruv Aggarwal
#aggarw45
#4/2/20

#flush all chains
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t raw -F
sudo iptables -t raw -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -t filter -F
sudo iptables -t filter -X


#for all outgoing packets change source
sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

#block certain ip's
iptables -A INPUT -s 164.1.0.1/97.19.10.12 -j DROP

#block all other hosts pinged
sudo iptables -A INPUT  -p icmp --icmp-type echo-request -j REJECT

#port forwarding to port of my choice(2307)
iptables -t nat -A PREROUTING -p tcp --dport 2307 -j DNAT --to 192.168.0.25:22
iptables -A INPUT -p tcp --dport 2307 -j ACCEPT
iptables -A FORWARD -p tcp --dport 22 -j ACCEPT

#allow only ssh purdue domain
iptables -A INPUT -s ecn.purdue.edu -p tcp --dport 22 -j ACCEPT

#allow only single access
iptables -A INPUT -p tcp --dport 80 -j DROP
iptables -A INPUT -p tcp -s 192.168.0.25 --dport 80 -j ACCEPT

#permit port 113
iptables -A INPUT -p tcp -m tcp --syn --dport 113 -j ACCEPT