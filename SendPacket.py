from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.inet6 import *
from random import randint
from netaddr import *
import binascii
import sys
import signal
from threading import Thread
from sqlalchemy import false

# Interface
# IFACE = "Ethernet 2" #fill the ID of destination network card

PKT_COUNT = 5
FROM_PORT = 1
TO_PORT = 65536

# MAC Address
SRC_MAC = "2C:58:B9:8B:50:CB" #fill your MAC Address here
DST_MAC = "D8:3A:DD:A4:BE:B8" #fill the destination MAC
# INVALID_SRC_MAC = "fa:fb:fc:fd:fe:ff" #Invalid MAC

# VLAN ID
VLAN_ID = 0

#IPv4
# INVALID_DST_IPv4   
# INVALID_SRC_IPv4
VALID_DST_IPv4 = "10.10.22.133"
VALID_SRC_IPv4 = "10.10.22.198"

# IPv6s
# INVALID_DST_IPv6 = "fd53:efgh:1234:3::12"  
# INVALID_SRC_IPv6 = "fd53:asdz:2345:3::13"  
# VALID_SRC_IPv6 = "fd53:abcd:5678:5::10"
# VALID_DST_IPv6 = "fd53:abcd:5678:5::14" 
# VALID_DST_Multicast = "ff02::1"
# INVALID_DST_Multicast = "ff02::2"

# Ports
VALID_SPORT = 13400
VALID_DPORT = 13400
INVALID_DPORT = 13456
INVALID_SPORT = 13456
RANGE = (1000, 65535)
pro_type = TCP

# Layers
dot1q = Dot1Q(vlan = VLAN_ID)
payload_default1 = "hi"
# Payload
payload_default = """
import os
print("Executing Raspberry Pi...")

os.system('ip -6 addr del fd53:abcd:5678:5::14/64 dev eth0')

os.system('ip -6 addr add fd53:abcd:5678:5::11/64 dev eth0')

os.system('ifconfig') 
"""
payload_change_mac = """
import os

os.system('ip link set dev eth0 down')

os.system('ip link set dev eth0 address 00:11:22:33:44:55')

os.system('ip link set dev eth0 up')

os.system('ip addr show eth0')
"""

payload_change_ipv4 = """
import os

os.system('ifconfig wlan0 10.10.22.200 netmask 255.255.255.0')

os.system('ifconfig')
"""

   
# PKT_Default_Receive = Ether()/dot1q/IPv6(src=VALID_SRC_IPv6,
#                                           dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_change_ipv4 

PKT_Default_Send = Ether(dst=DST_MAC, src=SRC_MAC)/dot1q/IP(src=VALID_SRC_IPv4, 
                                                                  dst=VALID_DST_IPv4)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_change_ipv4 

for i in range(5):
    sendp(PKT_Default_Send)  
# print("Gói tin nhận:", PKT_Default_Receive.summary())
print("Gói tin gửi:", PKT_Default_Send.summary())
