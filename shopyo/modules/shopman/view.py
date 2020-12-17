

# from flask import render_template
# from flask import url_for
# from flask import redirect
from flask import flash
from flask import request

# # 
from shopyoapi.html import notify_success
from shopyoapi.forms import flash_errors
from shopyoapi.module import ModuleHelp

from modules.shopman.forms import DeliveryOptionForm


from .models import DeliveryOption

mhelp = ModuleHelp(__file__, __name__)

globals()[mhelp.blueprint_str] = mhelp.blueprint

module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route(mhelp.info["dashboard"])
def dashboard():
    context = {}

    context.update({'info': mhelp.info})
    return mhelp.render('dashboard.html', **context)


@module_blueprint.route('/delivery'+mhelp.info["dashboard"])
def delivery():
    context = {}
    form = DeliveryOptionForm()
    options = DeliveryOption.query.all()

    context.update({
        'form': form,
        'options': options
        })
    context.update({'info': mhelp.info})
    return mhelp.render('delivery.html', **context)


@module_blueprint.route('/delivery/option/add', methods=['GET', 'POST'])
def delivery_add_option():
    if request.method == 'POST':
        form = DeliveryOptionForm()
        if form.validate_on_submit():
            toadd = DeliveryOption()
            toadd.option = form.option.data
            toadd.price = float(form.price.data)
            toadd.insert()
            flash(notify_success('Option Added!'))
            return mhelp.redirect_url('shopman.delivery')
        else:
            flash_errors(form)
            return mhelp.redirect_url('shopman.delivery')

@module_blueprint.route('/delivery/option/update', methods=['GET', 'POST'])
def delivery_option_update():
    if request.method == 'POST':
        
        opt_id = request.form['id']
        option_data = request.form['option']
        price_data = request.form['price']

        option = DeliveryOption.query.get(opt_id)
        option.option = option_data
        option.price = price_data
        option.update()

        flash(notify_success('Option updated!'))
        return mhelp.redirect_url('shopman.delivery')


@module_blueprint.route('/delivery/option/<option_id>/delete', methods=['GET'])
def delivery_option_delete(option_id):
    option = DeliveryOption.query.get(option_id)
    option.delete()

    flash(notify_success('Option Deleted!'))
    return mhelp.redirect_url('shopman.delivery')