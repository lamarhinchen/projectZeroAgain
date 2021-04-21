import datetime


class CheckingAcct:

    # Fill in your Models with necessary/desirable methods like a Constructor and repr methods

    def __init__(self, acct_id=0, user_id=0, nickname="", balance=0.00, disabled=False,
                 date_created=datetime.datetime.now()):
        # All tables will have some key that is unique. A typical solution is to give the model an ID.
        self.acct_id = acct_id
        self.user_id = user_id
        self.nickname = nickname
        self.balance = round(float(balance), 2)
        self.disabled = disabled
        self.date_created = date_created

    def __repr__(self):
        return repr(dict(acct_id=self.acct_id, user_id=self.user_id, nickname=self.nickname, balance=self.balance))

    def json(self):
        return {
            "acctID": self.acct_id,
            "userID": self.user_id,
            "balance": self.balance,
            "account nickname": self.nickname,
            "account deleted": self.disabled,
            "date created": self.date_created
        }

    @staticmethod
    def json_parse(json):
        checkingacct = CheckingAcct()
        checkingacct.acct_id = json["acctID"]
        checkingacct.user_id = json["userID"]
        checkingacct.nickname = json["account nickname"]
        checkingacct.balance = json["balance"]
        checkingacct.disabled = json["account deleted"]
        checkingacct.date_created = json["date created"]

        return checkingacct
