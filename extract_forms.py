import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://192.168.2.128/mutillidae/index.php?page=dns-lookup.php"

response = request(target_url)

soup = BeautifulSoup(response.content, 'html.parser')
forms_list = soup.find_all('form')
# print(forms_list)

for form in forms_list:
    action = form.get("action")
    post_url = urljoin(target_url, action)
    # print("post_url", post_url)
    method = form.get("method")
    # print("method", method)

    inputs_list = form.find_all("input")
    post_data = {}

    for input in inputs_list:
        input_name = input.get("name")

        input_type = input.get("type")
        input_value = input.get("value")

        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value

    result = requests.post(post_url, data=post_data)
    print(result.content.decode())