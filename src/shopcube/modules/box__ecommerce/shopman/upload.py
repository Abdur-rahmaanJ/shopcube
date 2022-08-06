from app import app

from modules.box__ecommerce.shopman.models import DeliveryOption
from modules.box__ecommerce.shopman.models import PaymentOption

def upload_options():
    with app.app_context():
        d1 = DeliveryOption(
            option='home delivery',
            price='100'
            )
        d1.insert()

        p1 = PaymentOption(
            name='Cash',
            text='paid on delivery'
            )
        p1.insert()


def upload():
    print('Uploading delivery and payment data ...')
    upload_options()
