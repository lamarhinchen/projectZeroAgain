import unittest

from psycopg2 import Error

from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.input_value_error import InputValueError
from cust_exceptions.invalid_value import InvalidValue
from dao.bank_dao_imp import BankDAOImp as test
from services.bank_service import BankService as service_test


# ########################## TESTS ##############################################################
class TestMethods(unittest.TestCase):

    # test a list of values is outputted
    def test_output_type_1(self):
        out = test.get_users(None)
        # test a list of values is outputted
        assert len(out[0]) > 0

    # test password is correct
    def test_validation_password_1(self):
        out = service_test.validate_password("Dalk74!dsf)")
        assert out == "Dalk74!dsf)"

    # test username is correct
    def test_validation_username_1(self):
        out = service_test.validate_username("lamar3.hinc")
        assert out == "lamar3.hinc"

    # test bad input in username
    def test_bad_username_1(self):
        try:
            service_test.validate_username("1Dfdgdfgfdbfgdg4..)")
            raise AssertionError("Incorrect values were able to be passed to the username!")
        except InputValueError as e:
            assert e.message == "Your username cannot be more than 15 char!"

    # test bad input in password
    def test_bad_password_1(self):
        try:
            service_test.validate_password("1Dalk7&4!dsf)")
            raise AssertionError("Incorrect values were able to be passed to the password!")
        except InputValueError as e:
            assert e.message == "Your password may only use letters numbers or these symbols: !.@(_#)"

    # test bad input in id field to catch sql error
    def test_bad_userID_1(self):
        try:
            service_test.update_user_by_id(user_id="fdgsfgdfsg", change_user_info="ghghghhgfgh")
            raise AssertionError("Incorrect values were able to be passed to the update user method!")
        except Error as e:
            assert e.cursor

    # test bad input in update user
    def test_bad_updateUser_1(self):
        try:
            test.update_user(self, user=None, user_id=None)
            raise AssertionError("Nothing was passed but no exception was raised")
        except InvalidValue as e:
            assert e.message == "No user info was given!"

    # test account already exists
    def test_account_exists_username_1(self):
        try:
            test.update_user(self, user={"username": "lamar1.hinc", "password": "dsjfaH7!df"}, user_id=4)
            raise AssertionError("A duplicate username was passed but an exception was not raised!")
        except AcctAlreadyExists as e:
            assert e.message == "This account name is already being used!"

    # test negative values of money in a search
    def test_bad_search_params_1(self):
        try:
            service_test.search_my_acct(user_id=6, amountless=-789, amountgreater=-678)
            raise AssertionError("It did not catch the negative values in the search params!")
        except IncorrectMoneyValue as e:
            assert e.message == "The balance range parameters are bad! The upper range must be a greater value than the lower range!"

    # test bad userID in the middle of the search
    def test_bad_ID_search_params_1(self):
        try:
            service_test.search_my_acct(user_id=6546356, amountless=789, amountgreater=678)
            raise AssertionError("This userID does not exist but it was not caught!")
        except AcctDoesNotExist as e:
            assert e.message == "userID: 6546356 does not exist!"


if __name__ == '__main__':
    unittest.main()
