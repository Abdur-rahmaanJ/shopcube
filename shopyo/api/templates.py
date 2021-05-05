from flask import render_template


def yo_render(template, context_dict):
    return render_template(template, **context_dict)
