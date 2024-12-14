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
#IFACE = "Ethernet 2"

# Number of threads used
PKT_COUNT = 5
# Scan Ports
FROM_PORT = 1
TO_PORT = 65536

# MAC Address
SRC_MAC = "2C:58:B9:8B:50:CB"	
#DST_MAC = "D8:3A:DD:A4:BE:B9"
DST_MAC = "2C:58:B9:8B:4C:BC"
INVALID_SRC_MAC = "fa:fb:fc:fd:fe:ff"

# VLAN ID
VLAN_ID = 0

# IPv6s
# INVALID_DST_IPv6 = "fd53:xxxx:xxx:3::xx" #Invalid IPv6
# INVALID_SRC_IPv6 = "fd53:xxxx:xxx:3::xx" #Invalid IPv6
VALID_DST_IPv6 = "fd53:abcd:5678:5::13"
VALID_SRC_IPv6 = "fd53:abcd:5678:5::10"
VALID_DST_Multicast = "ff02::1"
INVALID_DST_Multicast = "ff02::2"

#IPv4
# INVALID_DST_IPv4   
# INVALID_SRC_IPv4
# VALID_DST_IPv4 = "10.10.22.193"
# VALID_SRC_IPv4 = "20.10.2.12"

VALID_SPORT = 135         
VALID_DPORT = 1880      
INVALID_DPORT = 13456      
INVALID_SPORT = 13456    
RANGE = (1000, 65535)      
pro_type = TCP  


# Layers
dot1q = Dot1Q(vlan=VLAN_ID) #vlan=VLAN_ID

# Payload
payload_default ="Hello"
PKT_Default_Receive = Ether()/dot1q/IPv6(src=VALID_SRC_IPv6,
                            dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default
PKT_Default_Send = Ether(src=SRC_MAC , dst= DST_MAC)/dot1q/IPv6(src=VALID_SRC_IPv6,
                            dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default

#IPv4
# PKT_Default_Send = Ether(src=SRC_MAC)/dot1q/IP(src=VALID_SRC_IPv4,
                            # dst=VALID_DST_IPv4)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default

for i in range(10):
    sendp(PKT_Default_Send)
print(f"The packet has been sent from {VALID_SRC_IPv6} to {VALID_DST_IPv6}")