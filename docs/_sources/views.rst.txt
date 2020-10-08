Views
=====

.. toctree::
    :titlesonly:

Shopyo creates some boiler plate codes for you using the startapp command. Please refer to the `Modules section <modules.html>`_

View codes by default
---------------------

Here are some boiler plate codes created:

.. code:: python

    import os
    import json

    from flask import Blueprint
    # from flask import render_template
    # from flask import url_for
    # from flask import redirect
    # from flask import flash
    # from flask import request

    # from shopyoapi.enhance import base_context
    # from shopyoapi.html import notify_success
    # from shopyoapi.forms import flash_errors

    dirpath = os.path.dirname(os.path.abspath(__file__))
    module_info = {}

    with open(dirpath + "/info.json") as f:
        module_info = json.load(f)

    globals()['{}_blueprint'.format(module_info["module_name"])] = Blueprint(
        "{}".format(module_info["module_name"]),
        __name__,
        template_folder="templates",
        url_prefix=module_info["url_prefix"],
    )


    module_blueprint = globals()['{}_blueprint'.format(module_info["module_name"])]

    module_name = module_info["module_name"]


    @module_blueprint.route('/')
    def index():
        return ''


Using the above you can develop as usual. To change module name and module url, please refer to the modules section under info.json

Passing parameters to templates
-------------------------------

Please see the `Templates <templates.html>`_ section on how to pass
template variables