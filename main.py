from scapy.all import ARP, Ether, srp
from colorama import Fore
from pyfiglet import Figlet
from optparse import OptionParser

"""
    Net Scanner - Simple ARP-based Network Scanner

    Description:
    This tool scans the local network for active devices using the ARP protocol.
    It sends ARP requests to a given IP range (in CIDR format) and lists the
    responding devices along with their IP and MAC addresses.

    Usage:
        The -i or --ipaddress parameter is REQUIRED.
        The -if or --iface parameter is OPTIONAL. If not specified, the default interface (eth0) will be used.

    Examples:
        python net_scanner.py -i 192.168.1.0/24
        python net_scanner.py --ipaddress 10.0.0.0/24 --iface wlan0

    Notes:
        - Make sure you run the script with sufficient privileges (e.g., sudo) for network scanning.
        - You can list your available interfaces with 'ip link' or 'ifconfig'.
"""


def ns_parser():
    parser = OptionParser()
    parser.add_option('-i', '--ipaddress', dest='ip_address', help='IP address in CIDR format')
    parser.add_option('-if', '--iface', dest='iface', help='''
    Specify the network interface to use (e.g., eth0, wlan0, enp3s0).
    You can list available interfaces using 'ip link' or 'ifconfig'.
    This option is required if you want to bind the operation to a specific interface.
    ''')
    (options, args) = parser.parse_args()
    if not options.ip_address:
        print(Fore.RED + '[!] Please enter an IP address with -i')
        exit()
    return options

def net_scanner(ip, iface="eth0"):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered, _ = srp(packet, timeout=2, verbose=0, iface=iface)

    if answered:
        for send, recv in answered:
            print(Fore.GREEN + f"[+] IP: {recv.psrc} | MAC: {recv.hwsrc}")
    else:
        print(Fore.RED + "[-] No devices found.")

if __name__ == '__main__':
    figlet = Figlet(font='slant')
    print(Fore.CYAN + figlet.renderText('Net Scanner'))

    net_scan = ns_parser()
    net_scanner(net_scan.ip_address, iface=net_scan.iface)
