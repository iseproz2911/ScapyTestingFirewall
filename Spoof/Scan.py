from scapy.all import ARP, Ether, srp
def scan_network(target_ip):
   """
   Quét mạng để tìm các thiết bị, trả về IP và MAC của các thiết bị.
   """
   # Gửi yêu cầu ARP đến tất cả các IP trong dải mạng
   arp_request = ARP(pdst=target_ip)
   broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
   arp_request_broadcast = broadcast / arp_request
   # Gửi và nhận phản hồi
   answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
   devices = []
   for element in answered_list:
       devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
   return devices
def save_to_file(devices, filename="targets.txt"):
   """
   Lưu danh sách thiết bị vào file.
   """
   try:
       with open(filename, 'w') as file:
           file.write("IP Address\t\tMAC Address\n")
           file.write("-----------------------------------------\n")
           for device in devices:
               file.write(f"{device['ip']}\t\t{device['mac']}\n")
       print(f"Kết quả quét đã được lưu vào file: {filename}")
   except Exception as e:
       print(f"Lỗi khi lưu file: {e}")
# Dải mạng (thay bằng dải mạng của bạn)
target_ip = "10.10.22.1/24"
# Quét mạng
devices = scan_network(target_ip)
# In kết quả ra màn hình
print("IP Address\t\tMAC Address")
print("-----------------------------------------")
for device in devices:
   print(f"{device['ip']}\t\t{device['mac']}")
# Lưu kết quả vào file
save_to_file(devices)