from modules.box__default.auth.forms import LoginForm
from modules.box__default.auth.forms import RegisterCustomerForm


def get_auth_login_form():
    return LoginForm()

def get_auth_register_customer_form():
    return RegisterCustomerForm()


available_everywhere = {
    "get_auth_login_form": get_auth_login_form,
    "get_auth_register_customer_form": get_auth_register_customer_form
}
