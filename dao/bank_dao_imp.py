from bank_db.trans_conn import TransDbConn
from cust_exceptions.access_denied import AccessDenied
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.invalid_trans_type import InvalidTransType
from cust_exceptions.invalid_value import InvalidValue
from cust_exceptions.not_enough_funds import NotEnoughFunds
from bank_db.db_conn import DbConn as Clients
from bank_db.money_conn import MoneyDbConn as Checking
from dao.bank_dao import BankDAO
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_exceptions.acct_already_exists import AcctAlreadyExists


class BankDAOImp(BankDAO):

    # make a new bank account
    def make_acct_money(self, user_id):
        # load result set from data base
        tuple_holder = (user_id,)
        db_view = Checking.make_connect(
            """insert into bank_accounts(acct_id, user_id) values(default, %s) RETURNING *;""", tuple_holder)
        return [bank_users.json() for bank_users in db_view.values()]

    # record a deposit or withdraw
    def record_trans(self, bank_id=0, trans_type="deposit", amount=0.00, bank_id_to=0):
        if amount <= 0:
            raise IncorrectMoneyValue("Must input a positive dollar amount greater than Zero!")
        # load result set from data base
        tuple_holder = (bank_id, bank_id)
        acct_credits = TransDbConn.get_trans_value(
            """select sum(money_change) from acct_transaction where acct_id=%s and trans_type='deposit' or acct_to_id=%s and trans_type='transfer';""",
            tuple_holder)
        # load result set from data base
        tuple_holder = (bank_id, bank_id)
        acct_debits = TransDbConn.get_trans_value(
            """select sum(money_change) from acct_transaction where acct_id=%s and trans_type='withdraw' or acct_id=%s and trans_type='transfer';""",
            tuple_holder)
        my_debits = 0
        if acct_debits[0] is not None:
            my_debits = acct_debits[0]
        money_conv = "${:,.2f}"
        if trans_type == "withdraw" and float(acct_credits[0] - my_debits) - amount < 0 or trans_type == "transfer" and float(
                acct_credits[0] - my_debits) - amount < 0:
            raise NotEnoughFunds("You do not have enough funds to complete this withdraw!")
        if trans_type == "transfer":
            # load result set from data base
            tuple_holder = (bank_id, bank_id_to, amount, trans_type)
            db_view = TransDbConn.make_connect(
                """insert into acct_transaction(trans_id, acct_id, acct_to_id, money_change, trans_type) values(default, %s, %s, %s, %s) RETURNING *;""",
                tuple_holder)
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            # load result set from data base
            tuple_holder = (bank_id, amount, trans_type)
            db_view = TransDbConn.make_connect(
                """insert into acct_transaction(trans_id, acct_id, money_change, trans_type) values(default, %s, %s, %s) RETURNING *;""",
                tuple_holder)
            return [bank_users.json() for bank_users in db_view.values()]

    # make a deposit or withdraw money
    def mk_trans_acct(self, bank_id, user_id, trans_type):
        # balance code begin
        # load result set from data base
        tuple_holder = (bank_id, bank_id)
        acct_credits = TransDbConn.get_trans_value(
            """select sum(money_change) from acct_transaction where acct_id=%s and trans_type='deposit' or acct_to_id=%s and trans_type='transfer';""",
            tuple_holder)
        # load result set from data base
        tuple_holder = (bank_id, bank_id)
        acct_debits = TransDbConn.get_trans_value(
            """select sum(money_change) from acct_transaction where acct_id=%s and trans_type='withdraw' or acct_id=%s and trans_type='transfer';""",
            tuple_holder)
        my_debits = 0
        if acct_debits[0] is not None:
            my_debits = acct_debits[0]
        # balance code end

        if "deposit" in dict(trans_type):
            if trans_type["deposit"] <= 0:
                raise IncorrectMoneyValue("Must input a positive dollar amount greater than Zero!")
            newbalance = round(float(acct_credits[0] - my_debits), 2)
            # load result set from data base
            tuple_holder = (newbalance, bank_id)
            db_view = Checking.make_connect(
                """UPDATE bank_accounts SET balance=%s WHERE acct_id=%s AND disabled=false RETURNING *;""",
                tuple_holder)
        elif "withdraw" in dict(trans_type):
            if user_id is None:
                raise AccessDenied("You do not have access to this account!")
            if float(trans_type["withdraw"]) <= 0:
                raise IncorrectMoneyValue("Must input a positive dollar amount greater than Zero!")
            newbalance = round(float(acct_credits[0] - my_debits), 2)
            if newbalance < 0:
                raise NotEnoughFunds("You do not have enough funds to complete this withdraw!")
            # load result set from data base
            tuple_holder = (newbalance, bank_id, user_id)
            db_view = Checking.make_connect(
                """UPDATE bank_accounts SET balance=%s WHERE acct_id=%s AND user_id=%s AND disabled=false RETURNING *;""",
                tuple_holder)
        else:
            raise InvalidTransType("Invalid transaction type, please correct!")
        return [bank_users.json() for bank_users in db_view.values()]

    # update the transaction history and transfer funds
    def trans_bank_money(self, user_id, bank_id, to_bank_id, trans_amount):
        # validate the transaction amount
        format_trans_amount = round(float(trans_amount["amount"]), 2)
        # check to make sure the values put in are valid
        if format_trans_amount <= 0:
            raise IncorrectMoneyValue("The search parameters must be greater than zero!")
        # 1. first record the transaction
        db_view = self.record_trans(bank_id=bank_id, trans_type="transfer", amount=format_trans_amount,
                                    bank_id_to=to_bank_id)
        # 2. second balance the withdraw
        trans_type = {"withdraw": format_trans_amount}
        self.mk_trans_acct(bank_id=bank_id, user_id=user_id, trans_type=trans_type)
        # 3. last balance the deposit
        trans_type_to = {"deposit": format_trans_amount}
        self.mk_trans_acct(bank_id=to_bank_id, user_id=None, trans_type=trans_type_to)
        return db_view

    # get a users bank account
    def get_bank_acct(self, bank_id, user_id=None):
        if user_id is None:
            # load result set from data base
            tuple_holder = (bank_id,)
            db_view = Checking.make_connect(
                """SELECT * FROM bank_accounts WHERE acct_id=%s AND disabled=false;""", tuple_holder)
            if len(db_view) > 0:
                return [bank_users.json() for bank_users in db_view.values()]
            else:
                raise AcctDoesNotExist(f"The bank account acctID: {bank_id} does not exist!")
        else:
            # load result set from data base
            tuple_holder = (user_id, bank_id)
            db_view = Checking.make_connect(
                """SELECT * FROM bank_accounts WHERE user_id=%s AND acct_id=%s AND disabled=false;""", tuple_holder)
            if len(db_view) > 0:
                return [bank_users.json() for bank_users in db_view.values()]
            else:
                raise AcctDoesNotExist(f"The bank account for userID: {user_id}, acctID: {bank_id} does not exist!")

    # delete a users bank account
    def del_bank_acct(self, bank_id, user_id):
        # load result set from data base
        tuple_holder = (user_id, bank_id)
        db_view = Checking.make_connect(
            """UPDATE bank_accounts SET disabled=true WHERE user_id=%s AND acct_id=%s AND disabled=false RETURNING *;""",
            tuple_holder)
        if len(db_view) > 0:
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            raise AcctDoesNotExist(
                f"The bank account for userID: {user_id} was not successfully deleted as it does not exist!")

    # create a new user account
    def create_user(self, new_user):
        # validate if username exists for testing
        # validate username
        my_username = new_user["username"]
        my_password = new_user["password"]
        # load result set from data base
        tuple_holder = (my_username,)
        db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE username=%s;""", tuple_holder)
        for test_val in db_view:
            if my_username in db_view[test_val].username and not db_view[test_val].disabled:
                raise AcctAlreadyExists(f"UserName: '{my_username}' is already being used!")
            elif my_username in db_view[test_val].username and db_view[test_val].disabled:
                # Re-enable user account in database
                tuple_holder = (my_username,)
                db_view = Clients.make_connect(
                    """UPDATE bank_users SET disabled=false WHERE username=%s RETURNING *;""", tuple_holder)
                return [bank_users.json() for bank_users in db_view.values()]
        # Create new user account in data base
        tuple_holder = (my_username, my_password)
        db_view = Clients.make_connect(
            """insert into bank_users(user_id, username, password, disabled, date_created) values(default, %s, %s, false, current_timestamp) RETURNING *;""",
            tuple_holder)
        return [bank_users.json() for bank_users in db_view.values()]

    # get all the users bank accounts
    def get_acct_money(self, user_id):
        # load result set from data base
        tuple_holder = (user_id,)
        db_view = Checking.make_connect("""SELECT * FROM bank_accounts WHERE user_id=%s AND disabled=false;""",
                                        tuple_holder)
        return [bank_users.json() for bank_users in db_view.values()]

    # get a user if id=None or all the users
    def get_users(self, user_id=None):
        if user_id is None:
            # load result set from data base
            db_view = Clients.make_connect("SELECT * FROM bank_users WHERE disabled=false;")
            if len(db_view) == 0:
                raise AcctDoesNotExist("There are no accounts to see!")
            # return all users
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            # return a user
            # load result set from data base
            tuple_holder = (user_id,)
            db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE user_id=%s AND disabled=false;""",
                                           tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"userID: {user_id} does not exist!")
            return [bank_users.json() for bank_users in db_view.values()]

    def update_bank_acct(self, bank_id, user_id, update_data):
        # return a bank account
        # load result set from data base
        tuple_holder = (update_data["nickname"], bank_id, user_id)
        db_view = Checking.make_connect(
            """UPDATE bank_accounts SET nickname=%s WHERE acct_id=%s AND user_id=%s AND disabled=false RETURNING *;""",
            tuple_holder)
        return [bank_users.json() for bank_users in db_view.values()]

    # search through a users bank accounts to find ones the fall with the specified range
    def find_bank_acct(self, user_id, amountless, amountgreater):
        # return a bank account
        if amountless is None:
            # load result set from data base
            tuple_holder = (user_id, amountgreater)
            db_view = Checking.make_connect(
                """SELECT * FROM bank_accounts WHERE user_id=%s AND balance>=%s AND disabled=false;""", tuple_holder)
            return [bank_users.json() for bank_users in db_view.values()]
        elif amountgreater is None:
            # load result set from data base
            tuple_holder = (user_id, amountless)
            db_view = Checking.make_connect(
                """SELECT * FROM bank_accounts WHERE user_id=%s AND balance<=%s AND disabled=false;""", tuple_holder)
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            # load result set from data base
            tuple_holder = (user_id, amountless, amountgreater)
            db_view = Checking.make_connect(
                """SELECT * FROM bank_accounts WHERE user_id=%s AND balance<=%s AND balance>=%s AND disabled=false;""",
                tuple_holder)
            return [bank_users.json() for bank_users in db_view.values()]

    def update_user(self, user=None, user_id=None):
        if user is None or user_id is None:
            # value passed in is empty then throw an error
            raise InvalidValue("No user info was given!")
        else:
            # check which values are present
            if "username" in dict(user) and "password" in dict(user):
                username = user["username"]
                user_pass = user["password"]
                # load result set from data base
                tuple_holder = (username,)
                db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE username=%s;""", tuple_holder)
                if len(db_view) > 0 and db_view[0].disabled:
                    raise AcctAlreadyExists("This account name is being used by an inactive account!")
                elif len(db_view) > 0 and not db_view[0].disabled:
                    raise AcctAlreadyExists("This account name is already being used!")
                tuple_holder = (username, user_pass, user_id)
                db_view = Clients.make_connect(
                    """UPDATE bank_users SET username=%s, password=%s WHERE user_id=%s AND disabled=false RETURNING *;""",
                    tuple_holder)
                return [bank_users.json() for bank_users in db_view.values()]
            elif "username" in dict(user):
                username = user["username"]
                # load result set from data base
                tuple_holder = (username,)
                db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE username=%s;""", tuple_holder)
                if len(db_view) > 0 and db_view[0].disabled:
                    raise AcctAlreadyExists("This account name is being used by an inactive account!")
                elif len(db_view) > 0 and not db_view[0].disabled:
                    raise AcctAlreadyExists("This account name is already being used!")
                tuple_holder = (username, user_id)
                db_view = Clients.make_connect(
                    """UPDATE bank_users SET username=%s WHERE user_id=%s AND disabled=false RETURNING *;""",
                    tuple_holder)
                return [bank_users.json() for bank_users in db_view.values()]
            elif "password" in dict(user):
                user_pass = user["password"]
                tuple_holder = (user_pass, user_id)
                db_view = Clients.make_connect(
                    """UPDATE bank_users SET password=%s WHERE user_id=%s AND disabled=false RETURNING *;""",
                    tuple_holder)
                return [bank_users.json() for bank_users in db_view.values()]

    # Delete a user if None then delete all users
    def delete_user(self, user_id=None):
        if user_id is None:
            # Delete all users
            # load result set from data base
            db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE disabled=false;""")
            if len(db_view) == 0:
                raise AcctDoesNotExist("There are no accounts left to delete!")
            db_view = Clients.make_connect("""UPDATE bank_users SET disabled=true WHERE disabled=false RETURNING *;""")
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            # Delete a user
            # load result set from data base
            tuple_holder = (user_id,)
            db_view = Clients.make_connect("""SELECT * FROM bank_users WHERE user_id=%s AND disabled=false;""",
                                           tuple_holder)
            if len(db_view) > 0:
                # Delete user acct by disabling access to it
                tuple_holder = (user_id,)
                db_view = Clients.make_connect(
                    """UPDATE bank_users SET disabled=true WHERE user_id=%s RETURNING *;""", tuple_holder)
                return [bank_users.json() for bank_users in db_view.values()]
            else:
                raise AcctDoesNotExist(f"UserID: '{user_id}' does not exist!")


if __name__ == "__main__":
    print(BankDAOImp.get_users())
