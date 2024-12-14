# ***TEST RECEIVING PACKET****
# [Test Steps]
# 1. Read current packet record.
#    $ ip6tables -nvL INPUT
#    $ ip6tables -nvL INVALID_IPV6
# 2. Run script to send an Invalid data definition packet.
#    a. Open command prompt in the Python script folder.
#    b. Run command: python for_testing_receiving_packet.py
#    c. Input 2 to send an Invalid TCP flags packet.

from md_fw_declare import *
from md_fw_menu import *

# Set the source address to an invalid IPv6 address
PKT_Default_Receive[IPv6].src = INVALID_SRC_IPv6

def print_infor():
    try:
        global PKT_Default_Receive
        print("\n----------Packet-information-------------")
        PKT_Default_Receive.show()
    except Exception as ex:
        print("Error: " + str(ex))

# Function to send a packet
def send_packet():
    global PKT_Default_Receive
    try:
        PKT_Default_Receive.show()
        sendp(PKT_Default_Receive, iface=IFACE)
    except:
        print("Error: Please Connect Ethernet...")

# Main function to handle menu and actions
def main():
    cloop = True
    while cloop:
        try:
            choice = print_menu()
            if int(choice) == 1:
                print_infor()  # Option 1: Show packet information
            elif int(choice) == 2:
                send_packet()  # Option 2: Send an invalid packet
            elif int(choice) == 0:
                cloop = False  # Option 0: Exit the loop
        except KeyboardInterrupt:
            print('\nThanks! See you later!\n\n')
            cloop = False  # Exit on keyboard interrupt

if __name__ == '__main__':
    main()

# [Expected Results]
# Verify that packets with unspecified IPv6 TCP in the data definition are discarded.
# 1. Read packet record after sending 1 packet:
#    $ ip6tables -nvL INPUT
#    $ ip6tables -nvL INVALID_IPV6
#    You can see INVALID_IPV6 has increased by 1.
# 2. View log to show details:
#    $ tail /log/log_data/ulogd/full.log
#    $ tail /data/log_data/ulogd/full.log
#    Example log entry:
#    Input DROP IN=eth0.5 OUT=
#    MAC=ff:ff:ff:ff:ff:ff:xx:xx:xx:xx:xx:xx:xx:xx:xx:00:00:00 
#    SRC=fd53:xxxx:xxx:3::10 DST=fd53:xxxx:xx:5::14 
#    LEN=67 TC=0 HOPLIMIT=64 FLOWLBL=0 PROTO=TCP 
#    SPT=13400 DPT=13400 SEQ=0 ACK=0 WINDOW=8192 SYN URGP=0 MARK=0
