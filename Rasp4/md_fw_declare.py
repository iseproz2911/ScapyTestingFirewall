#md_fw_declare.py

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
IFACE = "Ethernet" #fill the ID of destination network card

# Number of threads used
PKT_COUNT = 5
# Scan Ports
FROM_PORT = 1
TO_PORT = 65536

# MAC Address
SRC_MAC = "2C:58:B9:8B:50:CB"
DST_MAC = "D8:3A:DD:A4:BE:B9" 
INVALID_SRC_MAC = "fa:fb:fc:fd:fe:ff" #Invalid MAC

# VLAN ID
VLAN_ID = 0

# IPv6s
INVALID_DST_IPv6 = "fd53:abcd:5678:3::10" #Invalid IPv6
INVALID_SRC_IPv6 = "fd53:abcd:5678:3::13" #Invalid IPv6
VALID_SRC_IPv6 = "fd53:abcd:5678:5::10"
VALID_DST_IPv6 = "fd53:abcd:5678:5::13"
VALID_DST_Multicast = "ff02::1"
INVALID_DST_Multicast = "ff02::2"

# Ports
VALID_SPORT = 13400
VALID_DPORT = 13400
INVALID_DPORT = 13456
INVALID_SPORT = 13456
RANGE = (1000, 65535)
pro_type = TCP

dot1q = Dot1Q(vlan=VLAN_ID)

payload_default ="Default"
PKT_Default_Receive = Ether()/dot1q/IPv6(src=VALID_SRC_IPv6,
                                        dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default
PKT_Default_Send = Ether(dst=DST_MAC,src=SRC_MAC)/dot1q/IPv6(src=VALID_SRC_IPv6,
                                        dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default