# This code will eventually be replaced. This will be a way of storing
# information for your models. This information will be lost when you terminate
# your application. After we learn about SQL we will replace this with a
# connection to a real database to persist your information.

# When you finish here look at the dao package next.
from data_model.db_model import BankUsers


class TempDB:
    # We are just adding some pre-populated data for us to work with.
    # Note this is a class variable for ease-of-use.
    bankusers = {
        0: BankUsers(identify_me=0, username="lamar1.hinc", password="DarkMagician8!", disabled=False),
        1: BankUsers(identify_me=1, username="lamar2.hinc", password="DarkMagician8!", disabled=False),
        2: BankUsers(identify_me=2, username="lamar3.hinc", password="DarkMagician8!", disabled=False),
        3: BankUsers(identify_me=3, username="lamar4.hinc", password="DarkMagician8!", disabled=False),
        4: BankUsers(identify_me=4, username="lamar5.hinc", password="DarkMagician8!", disabled=False),
        5: BankUsers(identify_me=5, username="lamar6.hinc", password="DarkMagician8!", disabled=False),
        6: BankUsers(identify_me=6, username="lamar7.hinc", password="DarkMagician8!", disabled=False),
        7: BankUsers(identify_me=7, username="lamar8.hinc", password="DarkMagician8!", disabled=False),
        8: BankUsers(identify_me=8, username="lamar9.hinc", password="DarkMagician8!", disabled=False),
        9: BankUsers(identify_me=9, username="lamar10.hinc", password="DarkMagician8!", disabled=False),
        10: BankUsers(identify_me=10, username="lamar11.hinc", password="DarkMagician8!", disabled=False)
    }
