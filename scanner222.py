import re
import urllib.parse

import requests
from bs4 import BeautifulSoup


class Scanner:

    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links_from(self, url):
        response = self.session.get(url)
        # matches = re.findall(b'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', response.content)

        # return re.findall(b'(?:href=")(.*)"', response.content)
        return re.findall(b'(?:href=")([^"]*)"', response.content)

        # href_matches = re.findall(r'href="[^"]*"', html_content)

        # return [link.strip() for link in matches if link.strip()]


    def crawl(self, url=None):
        if url is None:
            url = self.target_url

        href_links = self.extract_links_from(url)

        for link in href_links:
            link = link.decode()
            link = urllib.parse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find_all('form')

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urllib.parse.urljoin(url, action)

        method = form.get("method")

        inputs_list = form.find_all("input")
        post_data = {}

        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")

            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value

        if method == 'post':
            return self.session.post(post_url, data=post_data)

        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)

            for form in forms:
                print(f"\n\n[+] Testing form in {link}")
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)

                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link + " in the following form:")
                    print(form)

                if "=" in form:
                    print(f"[+] Testing {link}")

                    is_vulnerable_to_xss = self.test_xss_in_link(link)
                    if is_vulnerable_to_xss:
                        print("[***] Discovered XSS in " + link)

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        url = url.replace("=", "=" + xss_test_script).encode()
        res = self.session.get(url)

        # print("url: ", url)
        # print("url_type: ", type(url))

        return xss_test_script in res.content.decode()

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        res = self.submit_form(form, xss_test_script, url)

        return xss_test_script in res.content.decode()


if __name__ == "__main__":

    target_url = "http://192.168.2.128/dvwa/"
    ignore_links = ["http://192.168.2.128/dvwa/logout.php"]

    # target_url = "http://192.168.2.128/mutillidae/"
    # vuln_scanner = Scanner(target_url, ignore_links)
    # vuln_scanner.crawl(target_url)


    data_dict = {
        "username": "admin",
        "password": "password",
        "Login": "submit",
    }

    vuln_scanner = Scanner(target_url, ignore_links)
    vuln_scanner.session.post("http://192.168.2.128/dvwa/login.php", data=data_dict)

    # forms = vuln_scanner.extract_forms("http://192.168.2.128/dvwa/vulnerabilities/xss_r/")
    # print(forms)

    # response = vuln_scanner.submit_form(forms[0], "test", "http://192.168.2.128/mutillidae/index.php?page=dns-lookup.php")

    # response = vuln_scanner.submit_form(forms[0], "test", "http://192.168.2.128/dvwa/vulnerabilities/xss_r/")
    # print(response.content.decode())

    # response1 = vuln_scanner.test_xss_in_form(forms[0], "http://192.168.2.128/dvwa/vulnerabilities/xss_r/")
    # print("\nIS VULNERABLE form: ", response1)

    # response2 = vuln_scanner.test_xss_in_link("http://192.168.2.128/dvwa/vulnerabilities/xss_r/?name=<sCript>alert('test')</scriPt>")
    # print("\nIS VULNERABLE link: ", response2)

    vuln_scanner.crawl()
    vuln_scanner.run_scanner()
