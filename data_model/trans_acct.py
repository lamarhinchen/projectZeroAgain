import datetime


class TransAccounts:

    # Fill in your Models with necessary/desirable methods like a Constructor and repr methods

    def __init__(self, trans_id=0, acct_id=0, acct_to_id=0, money_change=0.00, trans_type="deposit",
                 date_completed=datetime.datetime.now()):
        # All tables will have some key that is unique. A typical solution is to give the model an ID.
        self.trans_id = trans_id
        self.acct_id = acct_id
        self.acct_to_id = acct_to_id
        self.money_change = round(float(money_change), 2)
        self.trans_type = trans_type
        self.date_completed = date_completed

    def __repr__(self):
        return repr(dict(trans_id=self.trans_id, acct_id=self.acct_id, acct_to_id=self.acct_to_id,
                         money_change=self.money_change,
                         trans_type=self.trans_type))

    def json(self):
        return {
            "transactionID": self.trans_id,
            "accountID": self.acct_id,
            "transfer to accountID": self.acct_to_id,
            "amount": self.money_change,
            "transaction": self.trans_type,
            "date completed": self.date_completed
        }

    @staticmethod
    def json_parse(json):
        transaccounts = TransAccounts()
        transaccounts.trans_id = json["transactionID"]
        transaccounts.acct_id = json["accountID"]
        transaccounts.acct_to_id = json["transfer to accountID"]
        transaccounts.money_change = json["amount"]
        transaccounts.trans_type = json["transaction"]
        transaccounts.date_completed = json["date completed"]

        return transaccounts
