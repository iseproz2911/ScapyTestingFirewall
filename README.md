# ScapyTestingFirewall
This document provides instructions for using Scapy to send and manipulate Ethernet packets from a Windows machine to a Raspberry Pi 4. The goal is to evaluate the firewall's ability to handle and block such packets when configured.
Objective
Use Scapy to modify Ethernet packets and test firewall rules on the Raspberry Pi.
Develop Python programs to manipulate and send custom Ethernet packets.
Analyze whether firewall rules effectively block or allow parameter modifications on the Raspberry Pi.

Scapy Overview
Scapy is a powerful Python library that allows users to create, modify, send, and capture network packets. It supports various protocols and packet types, including:
Ethernet: Modify source/destination MAC addresses and Ethertype.
VLAN: Change VLAN IDs.
IPv4/IPv6: Modify IP headers.
Protocols: Adjust fields for TCP, UDP, ICMP, and more.

Setting Up Scapy on Windows
Ensure Scapy is installed on the Windows machine using the following commands:
```
pip install scapy
pip install netaddr
pip install sqlalchemy
```
Implementation Steps

1. Set Up IPv6 and VLAN on Windows
Configure the network adapter on the Windows machine to support IPv6 and VLAN tagging:
Enable IPv6 in the network adapter settings.
2. Use appropriate VLAN IDs in the adapter’s configuration.

3. Develop Scapy Scripts to Modify Ethernet Packets
Write Python scripts using Scapy to modify Ethernet packet fields.

4. Receive/Send Packets on Raspberry Pi
Develop a Python program for the Raspberry Pi to:
Capture and analyze incoming packets.
Make changes to its network adapter parameters based on the received packets (e.g., VLAN ID or IP address).

5. Test Without Firewall

Disable the firewall on the Raspberry Pi and test whether parameter modifications sent from the Windows machine are applied:
Disable Firewall
Test Modifications

Run the Scapy script on Windows and verify:
Whether the Raspberry Pi’s network parameters are altered as expected.

6.Re-enable Firewall
Re-enable the firewall on the Raspberry Pi and evaluate whether modifications are still possible.

7. Reporting Results
https://hackmd.io/@iamproz2911/BJOBe4EEJg
