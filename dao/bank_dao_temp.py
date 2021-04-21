import re
from cust_logging.my_logger import MyLog as Log_Me
from bank_db.db_conn import DbConn as Clients
from dao.bank_dao import BankDAO
from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from data_model.db_model import BankUsers


class BankDAOTemp(BankDAO):
    # Custom bank user error msg
    # if message is 'success!' then no errors
    cust_err_msg = "success!"

    my_http_resp_code = 200

    def create_user(self, new_user):
        # validate if username exists for testing
        # validate username
        my_username = new_user["username"]
        my_password = new_user["password"]
        try:
            # load result set from data base
            db_view = Clients.make_connect(f"SELECT * FROM bank_users WHERE username='{my_username}';")
            for test_val in db_view:
                if my_username in db_view[test_val].username:
                    self.cust_err_msg = f"UserName: '{my_username}' is already being used!"
                    raise AcctAlreadyExists(self.cust_err_msg)

            # Create new user account in data base
            db_view = Clients.make_connect(
                f"insert into bank_users(user_id, username, password, disabled, date_created) values(default, '{my_username}', '{my_password}', false, current_timestamp);")
        except AcctAlreadyExists as a:
            self.my_http_resp_code = 201  # acct already exists
            return a.message, self.my_http_resp_code
        self.my_http_resp_code = 201  # input accepted and account created
        sendthis = self.get_users()
        return sendthis, self.my_http_resp_code

    def get_users(self, user_id=None):
        if user_id is None:
            # load result set from data base
            db_view = Clients.make_connect("SELECT * FROM bank_users;")
            # return all users
            return [bank_users.json() for bank_users in db_view.values()]
        else:
            # return a user
            try:
                # load result set from data base
                db_view = Clients.make_connect(f"SELECT * FROM bank_users WHERE user_id={user_id};")
                validate_ifnotexists = True
                for test_val in db_view:
                    if user_id == db_view[test_val].identify_me:
                        validate_ifnotexists = False
                        self.my_http_resp_code = 201  # acct does exist
                        return db_view[test_val].json(), self.my_http_resp_code
                if validate_ifnotexists:
                    self.cust_err_msg = f"UserID: '{user_id}' does not exist!"
                    raise AcctAlreadyExists(self.cust_err_msg)
            except AcctAlreadyExists as a:
                self.my_http_resp_code = 404  # This account does not exist
                return a.message, self.my_http_resp_code

    def update_user(self, user=None):
        if user is None:
            # return all users
            # Output error message
            self.cust_err_msg = "No user info was given!"
            Log_Me.info_log(
                f"Info! {self.cust_err_msg}")
            return [self.cust_err_msg]
        else:
            # return a user
            username = user["username"]
            user_id = user["userID"]
            try:
                # load result set from data base
                db_view = Clients.make_connect(f"SELECT * FROM bank_users WHERE username='{username}';")
                for test_val in db_view:
                    if username in db_view[test_val].username and user_id != db_view[
                        test_val].identify_me:
                        self.cust_err_msg = f"UserName: '{username}' is already being used!"
                        raise AcctAlreadyExists(self.cust_err_msg)
            except AcctAlreadyExists as a:
                self.my_http_resp_code = 201  # acct already exists
                return a.message, self.my_http_resp_code
            try:
                # load result set from data base
                db_view = Clients.make_connect(f"SELECT * FROM bank_users WHERE user_id={user_id};")
                validate_ifnotexists = True
                for test_val in db_view:
                    if int(user_id) == int(db_view[test_val].identify_me):
                        validate_ifnotexists = False
                        self.my_http_resp_code = 201  # acct does exist
                        old_user_info = db_view[test_val].json()
                        Clients.bankusers[test_val] = Clients.bankusers[test_val].json_parse(user)
                        return [
                                   f"Before: {old_user_info} Now: {Clients.bankusers[test_val].json()}"], self.my_http_resp_code
                if validate_ifnotexists:
                    self.cust_err_msg = f"UserID: '{user_id}' does not exist!"
                    raise AcctAlreadyExists(self.cust_err_msg)
            except AcctAlreadyExists as a:
                self.my_http_resp_code = 404  # This account does not exist
                return a.message, self.my_http_resp_code

    def delete_user(self, user_id=None):
        if user_id is None:
            # Delete all users
            for test_val in Clients.bankusers:
                Clients.bankusers[test_val].disabled = "True"
            return [bank_users.json() for bank_users in Clients.bankusers.values()]
        else:
            # Delete a user
            try:
                validate_ifnotexists = True
                for test_val in Clients.bankusers:
                    if user_id == Clients.bankusers[test_val].identify_me:
                        validate_ifnotexists = False
                        self.my_http_resp_code = 205  # acct does exist
                        Clients.bankusers[test_val].disabled = "True"
                        return Clients.bankusers[test_val].json(), self.my_http_resp_code
                if validate_ifnotexists:
                    self.cust_err_msg = f"UserID: '{user_id}' does not exist!"
                    raise AcctAlreadyExists(self.cust_err_msg)
            except AcctAlreadyExists as a:
                self.my_http_resp_code = 404  # This account does not exist
                return a.message, self.my_http_resp_code

    @staticmethod
    def close_down(inputted_value="e"):
        if inputted_value.lower() == "e":
            exit(0)

    @classmethod
    def login(cls):
        # validate if username exists else try again
        validated = True
        while validated:
            print("------------Login------------", end="\n\n")
            # validate username
            my_username = cls.validate_username()
            for test_val in Clients.bankusers:
                if my_username in Clients.bankusers[test_val]["username"]:
                    validated = False
            if validated:
                print(f"UserName: {my_username} does not exist!")
                print("Do you want to make a new account?")
                create_new_acct = input("'c' to create account or anything else to continue: ")
                cls.close_down(create_new_acct)
                if create_new_acct == "c":
                    cls.create_user(my_username)
                    return

        # validate if password exists else try again
        validated = True
        while validated:
            # validate password
            my_password = cls.validate_password()
            if my_password not in Clients.bankusers[0]["password"]:
                print(f"Password: {my_password} is incorrect!")
            else:
                validated = False

        print("Logging in.....")


if __name__ == "__main__":
    print(BankDAOTemp.get_users(""))
