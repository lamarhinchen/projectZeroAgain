class BankUsers:

    # Fill in your Models with necessary/desirable methods like a Constructor and repr methods

    def __init__(self, identify_me=0, username="", password="", disabled=False, date_created="Today"):
        # All tables will have some key that is unique. A typical solution is to give the model an ID.
        self.identify_me = identify_me
        self.username = username
        self.password = password
        self.disabled = disabled
        self.date_created = date_created

    def __repr__(self):
        return repr(dict(identify_me=self.identify_me, username=self.username, password=self.password,
                         date_created=self.date_created))

    def json(self):
        return {
            "userID": self.identify_me,
            "username": self.username,
            "password": self.password,
            "account deleted": self.disabled,
            "date created": self.date_created
        }

    @staticmethod
    def json_parse(json):
        bankuser = BankUsers()
        bankuser.identify_me = json["userID"]
        bankuser.username = json["username"]
        bankuser.password = json["password"]
        bankuser.disabled = json["account deleted"]
        bankuser.date_created = json["date created"]

        return bankuser
