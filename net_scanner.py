import optparse
import re

import scapy.all as scapy


def scan(ip):
    # 1. ip ni surab arp suovini yaratish
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()

    # 2. paketni yuborib unga javob olish
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(scapy.ls(broadcast))
    # print(broadcast.summary())
    # broadcast.show()

    arp_request_broadcast = broadcast / arp_request
    # arp_request_broadcast.show()

    # 3. javobni tahlil qilish parsing
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(answered_list.summary())

    # print('IP\t\t\t\tMAC Address\n' + '-' * 38)
    # for element in answered_list:
    #     # print(element[1].show())
    #
    #     print(element[1].psrc + '\t\t' + element[1].hwsrc)

    # refactoring loop ---------------
    clients_list = []
    for element in answered_list:
        # print(element[1].show())
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
        # print(element[1].psrc + '\t\t' + element[1].hwsrc)
    return clients_list


def is_valid_ip(ip):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip)


def print_result(results_list):
    print('IP\t\t\t\tMAC Address\n' + '-' * 38)
    for client in results_list:
        # print(client)
        print(client['ip'] + '\t\t' + client['mac'])


def get_option_ip():
    parser = optparse.OptionParser()
    parser.add_option('-ip', '--ip', dest='ip', help="IP address to scan")

    (options, args) = parser.parse_args()

    if not options.ip:
        print(parser.error('[-] Please, specify IP address'))

    return options


if __name__ == '__main__':
    opts = get_option_ip()

    result = scan(opts.ip)
    print_result(result)
