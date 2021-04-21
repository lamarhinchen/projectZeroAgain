from psycopg2 import Error

from cust_exceptions.access_denied import AccessDenied
from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.input_value_error import InputValueError
from cust_exceptions.invalid_trans_type import InvalidTransType

from cust_exceptions.invalid_value import InvalidValue
from cust_exceptions.not_enough_funds import NotEnoughFunds
from cust_logging.my_logger import MyLog as Log_Me
from flask import jsonify, request
from services.bank_service import BankService

Log_Me.info_log("Bank App Started")  # Would replace using print("Program Started")


def route(app):
    # custom welcome message
    @app.route('/', methods=["GET", "POST"])
    def hello_world():
        Log_Me.info_log("The home page was loaded!")  # You are on the home page
        return "Welcome to the Bank App!", 200

    # customer page not found message
    @app.errorhandler(404)
    def page_not_found(e):
        # how to load a custom page not found template doc
        # return render_template('404.html'), 404
        return "Page Not Found!", 404

    # get all the users
    @app.route("/clients", methods=["GET"])
    def get_all_users():
        try:
            # Serializing json
            users = jsonify(BankService.all_users())
            Log_Me.info_log("All users were successfully loaded!")
            return users, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e.message}, return 404 http code")
            return e.message, 404

    # get one user
    @app.route("/clients/<user_id>/", methods=["GET"])
    def get_user(user_id):
        try:
            user = jsonify(BankService.get_user_by_id(int(user_id)))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded userID:{user_id}, return 200 http code")
            return user, 200
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e.message}, return 404 http code")
            return e.message, 404

    # delete all users
    @app.route("/clients", methods=["DELETE"])
    def delete_all_users():
        try:
            user = jsonify(BankService.delete_all_users())
            # You deleted all users
            Log_Me.info_log(
                f"Info! You deleted all users successfully, return 205 http code")
            return user, 205
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e.message}, return 400 http code")
            return e.message, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e.message}, return 404 http code")
            return e.message, 404

    # delete a user
    @app.route("/clients/<user_id>", methods=["DELETE"])
    def delete_user(user_id):
        try:
            user = jsonify(BankService.delete_user_by_id(int(user_id)))
            # You deleted a user
            Log_Me.info_log(
                f"Info! User:{user_id}, return 205 http code")
            return user, 205
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e.message}, return 404 http code")
            return e.message, 404
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e.message}, return 400 http code")
            return e.message, 400

    # update the user's info
    @app.route("/clients/<user_id>/", methods=["PUT"])
    def update_user(user_id):
        try:
            # process the request json and uri info
            user = jsonify(BankService.update_user_by_id(int(user_id), request.json))
            # User was successfully updated
            Log_Me.info_log(
                f"Info! userID: {user_id} Successfully updated with your changes to the account, return 200 http code")
            return user, 200
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400
        except AcctAlreadyExists as e:
            Log_Me.error_log(f"Error! {e.message}, return 400 http code")
            return e.message, 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e.message}, return 406 http code")
            return e.message, 406
        except InputValueError as e:
            Log_Me.error_log(f"Error! {e.message}, return 406 http code")
            return e.message, 406
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e.message}, return 404 http code")
            return e.message, 404
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # make a new user
    @app.route("/clients", methods=["POST"])
    def create_user():
        try:
            new_user = request.json
            result = jsonify(BankService.create_bank_user(new_user))
            # Output of account creation
            Log_Me.info_log(
                f"Info! You have successfully created a new user, return 201 http code")
            return result, 201
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except AcctAlreadyExists as e:
            Log_Me.error_log(f"Error! {e.message}, return 400 http code")
            return e.message, 400
        except InputValueError as e:
            Log_Me.warning_log(f"Warning! {e.message}, return 400 http code")
            return e.message, 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e.message}, return 406 http code")
            return e.message, 406

    # make a new bank account for a user
    @app.route("/clients/<user_id>/accounts", methods=["POST"])
    def create_bank_acct(user_id):
        try:
            user = jsonify(BankService.mk_acct_by_id(int(user_id)))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded user:{user_id}, return 201 http code")
            return user, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log("Error! ID does not exist, return 404 http code")
            return a.message, 404  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # get all a user's bank accounts
    @app.route("/clients/<user_id>/accounts", methods=["GET"])
    def get_bank_accts(user_id):
        try:
            user = jsonify(BankService.get_acct_by_id(int(user_id)))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded user:{user_id}, return 201 http code")
            return user, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log("Error! ID does not exist, return 404 http code")
            return a.message, 404  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # make a deposit or withdraw
    @app.route("/clients/<user_id>/accounts/<bank_id>", methods=["PATCH"])
    def get_bank_acct(user_id, bank_id):
        try:
            user_acct = jsonify(BankService.dw_acct_by_id(int(bank_id), int(user_id), request.json))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded user:{user_id}, return {BankService.my_http_resp_code} http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except InvalidTransType as i:
            Log_Me.error_log(f"Error! {i.message}, return 401 http code")
            return i.message, 401
        except IncorrectMoneyValue as i:
            Log_Me.error_log(f"Error! {i.message}, return 401 http code")
            return i.message, 401
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
        except NotEnoughFunds as n:
            Log_Me.error_log(f"Error! {n.message}, return 422 http code")
            return n.message, 422
        except AccessDenied as i:
            Log_Me.error_log(f"Error! {i.message}, return 404 http code")
            return i.message, 401  # bad request

    # delete a bank account
    @app.route("/clients/<user_id>/accounts/<bank_id>", methods=["DELETE"])
    def delete_bank_acct(user_id, bank_id):
        try:
            user_acct = jsonify(BankService.delete_bank_acct_by_id(int(bank_id), int(user_id)))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded user:{user_id}, return {BankService.my_http_resp_code} http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # return a specific bank account
    @app.route("/clients/<user_id>/accounts/<bank_id>", methods=["GET"])
    def get_my_bank_acct(user_id, bank_id):
        try:
            user_acct = jsonify(BankService.get_my_acct(int(bank_id), int(user_id)))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully loaded user:{user_id}, return {BankService.my_http_resp_code} http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # update bank account nickname
    @app.route("/clients/<user_id>/accounts/<bank_id>", methods=["PUT"])
    def update_my_bank_acct(user_id, bank_id):
        try:
            user_acct = jsonify(BankService.update_my_acct(int(bank_id), int(user_id), request.json))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully updated bank account for user:{user_id}, return {BankService.my_http_resp_code} http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid ID, return 400 http code")
            return "Not a valid ID", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # search bank accounts between these amounts
    @app.route("/clients/<user_id>/accounts/search", methods=["GET"])
    def search_my_bank_acct(user_id):
        try:
            amountless = request.args.get("amountLessThan", default=None, type=float)
            amountgreater = request.args.get("amountGreaterThan", default=None, type=float)
            if amountless is None and amountgreater is None:
                user_acct = jsonify(BankService.get_acct_by_id(int(user_id)))
                # if no values just get all accounts for the user
                Log_Me.info_log(
                    f"Info! Successfully found all bank accounts for user:{user_id}, return 201 http code")
                return user_acct, 201
            user_acct = jsonify(
                BankService.search_my_acct(int(user_id), amountless, amountgreater))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully found these bank accounts for user:{user_id}, return accounts greater than({amountgreater}) but less than({amountless}) http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid value, return 400 http code")
            return "Not a valid value", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except IncorrectMoneyValue as i:
            Log_Me.error_log(f"Error! {i.message}, return 404 http code")
            return i.message, 400  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400

    # transfer funds between accounts
    @app.route("/clients/<user_id>/accounts/<bank_id>/transfer/<to_bank_id>", methods=["PATCH"])
    def transfer_bank_acct(user_id, bank_id, to_bank_id):
        try:
            user_acct = jsonify(BankService.trans_acct_by_id(int(user_id), int(bank_id), int(to_bank_id), request.json))
            # You inputted a bad id value
            Log_Me.info_log(
                f"Info! Successfully transferred money from acctID:{bank_id} and to acctID:{to_bank_id}, return http code")
            return user_acct, 201
        except ValueError:
            Log_Me.error_log("Error! Not a valid value, return 400 http code")
            return "Not a valid value", 400  # bad request
        except AcctDoesNotExist as a:
            Log_Me.error_log(f"Error! {a.message}, return 404 http code")
            return a.message, 404  # bad request
        except IncorrectMoneyValue as i:
            Log_Me.error_log(f"Error! {i.message}, return 400 http code")
            return i.message, 400  # bad request
        except InvalidTransType as i:
            Log_Me.error_log(f"Error! {i.message}, return 400 http code")
            return i.message, 400  # bad request
        except NotEnoughFunds as i:
            Log_Me.error_log(f"Error! {i.message}, return 422 http code")
            return i.message, 422  # bad request
        except AccessDenied as i:
            Log_Me.error_log(f"Error! {i.message}, return 401 http code")
            return i.message, 401  # bad request
        except Error as e:
            Log_Me.error_log(f"Error! {e}, return 400 http code")
            return e, 400
