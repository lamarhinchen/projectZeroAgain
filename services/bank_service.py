import re
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.invalid_value import InvalidValue
from dao.bank_dao_imp import BankDAOImp
from cust_exceptions.input_value_error import InputValueError


class BankService:
    bank_data = BankDAOImp()
    my_http_resp_code = 200

    @classmethod
    def create_bank_user(cls, new_user):
        # check if username is valid
        cls.validate_username(new_user["username"])
        # check if password is valid
        cls.validate_password(new_user["password"])
        # create the new user
        acct_created = cls.bank_data.create_user(new_user)
        return acct_created

    # make a new bank account for a user
    @classmethod
    def mk_acct_by_id(cls, user_id):
        # make sure the user exists
        cls.bank_data.get_users(user_id)
        # make the new bank account
        result = cls.bank_data.make_acct_money(user_id)
        return result

    @classmethod
    def get_acct_by_id(cls, user_id):
        cls.bank_data.get_users(user_id)
        result = cls.bank_data.get_acct_money(user_id)
        return result

    @classmethod
    def all_users(cls):
        # get the users
        return cls.bank_data.get_users()

    @classmethod
    def get_user_by_id(cls, user_id):
        acct_response = cls.bank_data.get_users(user_id=user_id)
        return acct_response

    @classmethod
    def delete_all_users(cls):
        return cls.bank_data.delete_user()

    @classmethod
    def delete_user_by_id(cls, user_id):
        # check if user account exists
        cls.bank_data.get_users(user_id)
        # deletes the user account
        acct_response = cls.bank_data.delete_user(user_id=user_id)
        return acct_response

    # Make an update to a users account
    @classmethod
    def update_user_by_id(cls, user_id, change_user_info):
        # check to make sure the client ID exists
        cls.bank_data.get_users(user_id=user_id)
        # check which values exist
        print(change_user_info)
        if "username" in dict(change_user_info):
            print(change_user_info)
            # validate if username is allowed
            cls.validate_username(change_user_info["username"])
        if "password" in dict(change_user_info):
            print(change_user_info)
            # validate if password is allowed
            cls.validate_password(change_user_info["password"])
        if "username" not in dict(change_user_info) and "password" not in dict(change_user_info):
            raise InvalidValue("You need a username or a password value to make an update!")
        # make the update to the account
        acct_response = cls.bank_data.update_user(user=change_user_info, user_id=user_id)
        return acct_response

    # make a deposit or withdraw
    @classmethod
    def dw_acct_by_id(cls, bank_id, user_id, trans_type):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        # check to see if the bank account exists
        cls.bank_data.get_bank_acct(bank_id, user_id)
        # make a record of the transactions table
        if "deposit" in dict(trans_type):
            cls.bank_data.record_trans(bank_id=bank_id, trans_type="deposit",
                                       amount=round(float(trans_type["deposit"]), 2))
        elif "withdraw" in dict(trans_type):
            cls.bank_data.record_trans(bank_id=bank_id, trans_type="withdraw",
                                       amount=round(float(trans_type["withdraw"]), 2))
        # complete the deposit or withdraw
        data_response = cls.bank_data.mk_trans_acct(bank_id, user_id, trans_type)
        return data_response

    @classmethod
    def delete_bank_acct_by_id(cls, bank_id, user_id):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        # check to see if the bank account exists
        cls.bank_data.get_bank_acct(bank_id, user_id)
        # delete the bank account
        data_response = cls.bank_data.del_bank_acct(bank_id, user_id)
        return data_response

    @classmethod
    def get_my_acct(cls, bank_id, user_id):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        data_response = cls.bank_data.get_bank_acct(bank_id, user_id)
        return data_response

    @classmethod
    def update_my_acct(cls, bank_id, user_id, update_data):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        # check to see if the bank account exists
        cls.bank_data.get_bank_acct(bank_id, user_id)
        # execute the query
        data_response = cls.bank_data.update_bank_acct(bank_id, user_id, update_data)
        return data_response

    @classmethod
    def search_my_acct(cls, user_id, amountless, amountgreater):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        # check to make sure the values put in are valid
        if amountgreater is not None and amountless is not None:
            if float(amountless) < float(amountgreater):
                raise IncorrectMoneyValue(
                    "The balance range parameters are bad! The upper range must be a greater value than the lower range!")
        if amountgreater is None and amountless is not None:
            if float(amountless < 0):
                raise IncorrectMoneyValue("The search parameters must be None or greater than zero!")
        elif amountgreater is not None and amountless is None:
            if float(amountgreater < 0):
                raise IncorrectMoneyValue("The search parameters must be None or greater than zero!")
        else:
            if float(amountless) < 0 or float(amountgreater) < 0:
                raise IncorrectMoneyValue("The search parameters must be None or greater than zero!")
        # execute the query
        data_response = cls.bank_data.find_bank_acct(user_id, amountless, amountgreater)
        return data_response

    @classmethod
    def trans_acct_by_id(cls, user_id, bank_id, to_bank_id, trans_amount):
        # check to see if the user exists
        cls.bank_data.get_users(user_id)
        # check to see if the bank account exists
        cls.bank_data.get_bank_acct(bank_id, user_id)
        # check to see if the bank account we are transferring to exists
        cls.bank_data.get_bank_acct(to_bank_id)
        # execute the query
        data_response = cls.bank_data.trans_bank_money(user_id, bank_id, to_bank_id, trans_amount)
        return data_response

    @classmethod
    def validate_username(cls, username=None):
        # validate user input username
        if username is not None:
            username = username.lower()
            if len(username) < 8:
                raise InputValueError("Your username needs to be at least 8 char!")
            elif len(username) > 15:
                raise InputValueError("Your username cannot be more than 15 char!")
            elif re.findall("[^a-zA-Z0-9.]", username):
                raise InputValueError("Your username may only use letters numbers or a period!")
            else:
                if not re.findall("[a-zA-Z]", username):
                    raise InputValueError("Your username must have at least 1 letter!")
                if re.findall("^[0-9.]", username):
                    raise InputValueError("Your username cannot start with a number or period!")
                if re.findall("[.]$", username):
                    raise InputValueError("Your username cannot end with a period!")
            return username
        else:
            raise InvalidValue("No value Given!")

    @classmethod
    def validate_password(cls, password=None):
        # validate user input password
        if password is not None:
            if len(password) < 8:
                raise InputValueError("Your password needs to be at least 8 char!")
            elif len(password) > 15:
                raise InputValueError("Your password cannot be more than 15 char!")
            elif re.findall("[^a-zA-Z0-9!.@(_#)]", password):
                raise InputValueError("Your password may only use letters numbers or these symbols: !.@(_#)")
            else:
                if not re.findall("[0-9]", password):
                    raise InputValueError("Your password must have at least one number!")
                if not re.findall("[a-zA-Z]", password):
                    raise InputValueError("Your password must have at least 1 letter!")
                if not re.findall("[A-Z]", password):
                    raise InputValueError("Your password must have at least 1 uppercase letter!")
                if not re.findall("[a-z]", password):
                    raise InputValueError("Your password must have at least 1 lowercase letter!")
                if not re.findall("[!.@(_#)]", password):
                    raise InputValueError("Your password must have at least 1 special symbol: !.@(_#)")
            return password
        else:
            raise InvalidValue("No value Given!")


if __name__ == "__main__":
    print(BankService.get_user_by_id(user_id=0))
