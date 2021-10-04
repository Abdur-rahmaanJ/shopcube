import copy
from flask import session
from modules.box__ecommerce.product.models import Product

class Cart:
    '''
    {
        'items': 
        {
            '620ba5dd-08a3-11ec-bfee-40f02f67a6a8':
            [
                {
                    'color': 'c1', 
                    'quantity': 1, 
                    'size': 's1'
                },
                {
                    'color': 'c1', 
                    'quantity': 1, 
                    'size': 's2'
                },
            ]
        }, 
        'num_items': 1, 
        'total_price': 100.0
    }
    '''


    @classmethod
    def _data(cls):
        '''
        '620ba5dd-08a3-11ec-bfee-40f02f67a6a8':
            [
                {
                    'color': 'c1', 
                    'quantity': 1, 
                    'size': 's1'
                },
                {
                    'color': 'c1', 
                    'quantity': 1, 
                    'size': 's2'
                },
            ]
        '''
        if 'cart' not in session:
            session['cart'] = {}
        return session['cart']

    @classmethod
    def _num_items(cls):
        return sum([cls.items_quantity(barcode) for barcode in cls._data()])

    @classmethod
    def _total_price(cls):
        cart_total_price = 0
        for barcode in cls._data():
            product = Product.query.filter_by(barcode=barcode).first()
            cart_total_price += (
                cls.items_quantity(barcode) * product.selling_price
            )

        return cart_total_price

    @classmethod
    def data(cls):
        num_items = cls._num_items()
        cart_data = cls._data()
        total_price = cls._total_price()

        return {
        'items': cart_data,
        'num_items': num_items,
        'total_price': total_price
        }

    @classmethod
    def reset(cls):
        session['cart'] = {}

    @classmethod
    def has_barcode(cls, barcode):
        return barcode in cls._data()

    @classmethod
    def has_order(cls, barcode, item_info):
        '''if only quantity differs, color and size remains the same'''
        if not barcode in cls._data():
            return False
        if len(cls._data()[barcode]) == 0:
            return False
        items = cls._data()[barcode]
        for i, item in enumerate(items):
            if (
                (item['color'] == item_info['color']) and 
                (item['size'] == item_info['size'])
                ):
                return {'i': i}
        return False

    @classmethod
    def items_quantity(cls, barcode):
        items = cls._data()[barcode]
        total_q = sum([int(item['quantity']) for item in items])
        return total_q


    @classmethod
    def add(cls, barcode, item_info):
        '''
        :item_info: {
            'quantity': 1,
            'color': 'white',
            'size': 'XL'
        }
        '''
        product = Product.query.filter_by(barcode=barcode).first()
        if cls.has_barcode(barcode):
            has_order = cls.has_order(barcode, item_info)
            if has_order:
                updated_quantity = cls.items_quantity(barcode) + item_info['quantity']
                if updated_quantity > product.in_stock:
                    return False
                cls._data()[barcode][has_order['i']]['quantity'] += item_info['quantity']
            else:
                cls._data()[barcode].append(item_info)
        elif not cls.has_barcode(barcode):
            cls._data()[barcode] = []
            cls._data()[barcode].append(item_info)

        return True

    @classmethod
    def remove(cls, barcode, size, color):
        try:
            has_order = cls.has_order(barcode, {'size': size, 'color': color})
            if has_order:
                del cls._data()[barcode][has_order['i']]
                if len(cls._data()[barcode]) == 0:
                    del cls._data()[barcode]
        except KeyError:
            pass

    @classmethod
    def update(cls, form_dict):
        '''
        ImmutableMultiDict([('csrf_token', 'IjRlNmY3ZmI4ZjY3OGRjZTBhN2M1ZTYxNWNkYWQ5YjM5
Zjg2NGI2NTEi.YSxyhw.xHbr1Lde7b-nsuJ1ZEYhAZ0wuTQ'), ('barcode_1', '620ba5dd-08a3-
11ec-bfee-40f02f67a6a8'), ('size_1', '5'), ('color_1', '6'), ('quantity_1', '1')
, ('barcode_2', '620ba5dd-08a3-11ec-bfee-40f02f67a6a8'), ('size_2', '6'), ('colo
r_2', '6'), ('quantity_2', '1')])
        '''
        cls.reset()
        
        for key in form_dict:
            if key.startswith("barcode"):
                barcode = form_dict[key].strip()
                product = Product.query.get(barcode)

                number = key.split("_")[1]

                quantity = form_dict['quantity_{}'.format(number)]
                size = form_dict['size_{}'.format(number)]
                color = form_dict['color_{}'.format(number)]

                item_info = {
                    'quantity': int(quantity),
                    'size': size,
                    'color': color
                }

                cls.add(barcode, item_info)
