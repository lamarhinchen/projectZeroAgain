from flask import Flask
from services.bank_service import BankService
from contollers import front_controller as fc

app = Flask(__name__)

fc.route(app)

if __name__ == "__main__":
    app.run(debug=True)
else:
    print(__name__)
