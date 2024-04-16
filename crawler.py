import requests

url = 'google.com'


def request(url):
    try:
        return requests.get('http://' + url)
        # print(get_response)
    except requests.exceptions.ConnectionError:
        pass


target_url = "google.com"

with open("/home/zilola/PycharmProjects/kali2/subdomains.list", 'r') as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url

        response = request(test_url)
        if response:
            print(f"[+] Discovered subdomain --> {test_url}")


