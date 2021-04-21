from contollers import bank_controller, home_controller


def route(app):
    # Call all other controllers
    bank_controller.route(app)
    home_controller.route(app)
