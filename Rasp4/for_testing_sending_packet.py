import socket, time, os, struct
from ipaddress import ip_address

try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

# IPv6s
INVALID_DST_IPv6 = "fd53:xxxx:xxx:3::15"  # Invalid IPv6
INVALID_SRC_IPv6 = "fd53:xxxx:xxx:3::12"  # Invalid IPv6
VALID_SRC_IPv6 = "fd53:xxxx:xxx:5::14"
VALID_DST_IPv6 = "fd53:xxxx:xxx:5::10"
VALID_SPORT = 13400
VALID_DPORT = 13400
INVALID_SPORT = 13455
INVALID_DPORT = 13455
MULTICAST_TTL = 32
VALID_MULTICAST = "ff02::1"
INVALID_MULTICAST = "ff02::2"
mes = "Default"

# Next headers for IPv6 protocols
IPV6_NEXT_HEADER_HOP_BY_HOP = 0
IPV6_NEXT_HEADER_TCP = 6
IPV6_NEXT_HEADER_UDP = 17
IPV6_NEXT_HEADER_ICMP = 58
UPPER_LAYER_PROTOCOLS = [
    IPV6_NEXT_HEADER_TCP,
    IPV6_NEXT_HEADER_UDP,
    IPV6_NEXT_HEADER_ICMP,
]

# ICMP Protocol codes
ICMP_ECHO_REQUEST = 128
ICMP_ECHO_RESPONSE = 129

# Default hop limit for IPv6
HOP_LIMIT_DEFAULT = 64

def checksum_calculate(data):
    # Create halfwords from data bytes. Example: data[0] = 0x01, data[1] = 0xb2 => 0x01b2
    halfwords = [
        ((byte0 << 8) | byte1)
        for byte0, byte1 in zip_longest(data[::2], data[1::2], fillvalue=0x00)
    ]
    checksum = 0
    for halfword in halfwords:
        checksum += halfword
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum ^= 0xFFFF
    if checksum == 0:
        return 0xFFFF
    else:
        return checksum

class IPv6Header():
    _version = 6
    _header_length = 40

    def __init__(self,
                 source_address,
                 destination_address,
                 traffic_class=0,
                 flow_label=0,
                 hop_limit=64,
                 payload_length=0,
                 next_header=0):
        self.version = self._version
        self._source_address = self._convert_to_ipaddress(source_address)
        self._destination_address = self._convert_to_ipaddress(destination_address)
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.hop_limit = hop_limit
        self.payload_length = payload_length
        self.next_header = next_header

    def _convert_to_ipaddress(self, value):
        if isinstance(value, bytearray):
            value = bytes(value)
        return ip_address(value)

    @property
    def source_address(self):
        return self._source_address

    @source_address.setter
    def source_address(self, value):
        self._source_address = self._convert_to_ipaddress(value)

    @property
    def destination_address(self):
        return self._destination_address

    def pack(self):
        data = bytearray([
            ((self.version & 0x0F) << 4) | ((self.traffic_class >> 4) & 0x0F),
            ((self.traffic_class & 0x0F) << 4) |
            ((self.flow_label >> 16) & 0x0F),
            ((self.flow_label >> 8) & 0xFF),
            ((self.flow_label & 0xFF))
        ])
        data += struct.pack(">H", self.payload_length)
        data += bytearray([self.next_header, self.hop_limit])
        data += self.source_address.packed
        data += self.destination_address.packed
        return data

    @classmethod
    def unpack(cls, data):
        b = bytearray(data.read(4))
        version = (b[0] >> 4) & 0x0F
        traffic_class = ((b[0] & 0x0F) << 4) | ((b[1] >> 4) & 0x0F)
        flow_label = ((b[1] & 0x0F) << 16) | (b[2] << 8) | b[3]
        payload_length = struct.unpack(">H", data.read(2))[0]
        next_header = ord(data.read(1))
        hop_limit = ord(data.read(1))
        src_addr = bytearray(data.read(16))
        dst_addr = bytearray(data.read(16))
        return cls(src_addr, dst_addr, traffic_class, flow_label, hop_limit,
                   payload_length, next_header)

    def __repr__(self):
        return "IPv6Header(source_address={}, destination_address={}, next_header={}, payload_length={}, hop_limit={}, traffic_class={}, flow_label={})".format(
            self.source_address.compressed, self.destination_address.compressed,
            self.next_header, self.payload_length, self.hop_limit,
            self.traffic_class, self.flow_label)

    def __len__(self):
        return self._header_length

    def display_info(self):
        print("###[ IPv6 ]###")
        print("version = " + str(self.version))
        print("tc = " + str(self.traffic_class))
        print("fl = " + str(self.flow_label))
        print("plen = " + str(self.payload_length))
        print("nh = " + str(self.next_header))
        print("hlim = " + str(self.hop_limit))
        print("src = " + str(self._source_address))
        print("dst = " + str(self._destination_address))

# (Other classes such as TCPHeader, UDPHeader remain the same.)


def print_menu():
    cloop = True
    while cloop:
        print(22 * "-", "MENU", 22 * "-")
        print("\t1. [Send] {:<24}".format("Send A Valid UDP Packet"))
        print("\t2. [Send] {:<24}".format("Send An Invalid destination IPv6 UDP Packet"))
        print("\t3. [Send] {:<24}".format("View log (/log/log_data/ulogd/full.log)"))
        print("\t4. [Send] {:<24}".format("View valid packet counter"))
        print("\t5. [Send] {:<24}".format("View invalid packet counter"))
        print("\t0. [Exit] {:<24}".format("Exit"))
        print(50 * "-")
        try:
            choice = input("Enter your choice [0-5]: ")
            if (int(choice) >= 0 and int(choice) <= 5):
                cloop = False
        except ValueError:
            print('')
    return choice

def main():
    cloop = True
    while cloop:
        try:
            choice = print_menu()
            if int(choice) == 1:
                send_udp_packet(src_addr=VALID_SRC_IPv6, dst_addr=VALID_DST_IPv6, src_port=VALID_SPORT, dst_port=VALID_DPORT)
            elif int(choice) == 2:
                # UDP invalid destination IP
                send_udp_packet(src_addr=VALID_SRC_IPv6, dst_addr=INVALID_DST_IPv6, src_port=VALID_SPORT, dst_port=VALID_DPORT)
            elif int(choice) == 3:
                try:
                    os.system('tail /log/log_data/ulogd/full.log')
                except Exception as exx:
                    print(exx)
            elif int(choice) == 4:
                try:
                    os.system('ip6tables -nvL wl_uo_5_14_to_5_10')
                except Exception as exx:
                    print(exx)
            elif int(choice) == 5:
                try:
                    os.system('ip6tables -nvL INVALID_IPV6')
                except Exception as exx:
                    print(exx)
            elif int(choice) == 0:
                cloop = False
        except KeyboardInterrupt:
            print('\nThanks! See you later!\n\n')
            cloop = False

if __name__ == '__main__':
    main()
