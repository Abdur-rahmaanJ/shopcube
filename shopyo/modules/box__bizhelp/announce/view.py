

# from flask import render_template
# from flask import url_for
# from flask import redirect
from flask import flash
from flask import request

from shopyoapi.html import notify_success
from shopyoapi.forms import flash_errors
from shopyoapi.module import ModuleHelp

from .forms import AnnounceForm
from .models import Announcement

from flask_login import login_required

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


# TODO add pagination
@module_blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():

    context = mhelp.context()
    form = AnnounceForm()
    context.update({
        'form': form
        })
    return mhelp.render('dashboard.html', **context)


@module_blueprint.route("/add/check", methods=["GET", "POST"])
@login_required
def add_check():
    if request.method == 'POST':
        form = AnnounceForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect(url_for("{}.dashboard".format(mhelp.info['module_name'])))
        toadd_announce = Announcement(
            content=form.content.data,
            title=form.title.data,
        )
        toadd_announce.save()
    return mhelp.redirect_url('{}.dashboard'.format(mhelp.info['module_name']))


@module_blueprint.route("/list", methods=["GET", "POST"])
@login_required
def list():
    context = mhelp.context()
    announcements = Announcement.query.all()
    context.update({
        'announcements': announcements
        })
    return mhelp.render('list.html', **context)


@module_blueprint.route("/<announce_id>/delete/check", methods=["GET"])
@login_required
def delete_check(announce_id):
    announcement = Announcement.query.get(announce_id)
    announcement.delete()
    return mhelp.redirect_url(mhelp.method('list'))


@module_blueprint.route("/<announce_id>/edit", methods=["GET", "POST"])
@login_required
def edit(announce_id):
    context = mhelp.context()
    announcement = Announcement.query.get(announce_id)
    
    form = AnnounceForm(obj=announcement)

    context.update({
        'dir':dir,
        'announcement': announcement,
        'form': form
        })
    return mhelp.render('edit.html', **context)



@module_blueprint.route("/<announce_id>/edit/check", methods=["GET", "POST"])
@login_required
def edit_check(announce_id):

    if request.method == 'POST':
        announcement = Announcement.query.get(announce_id)
        form = AnnounceForm(obj=announcement)
        if not form.validate_on_submit():
            flash_errors(form)
            return mhelp.redirect_url(mhelp.method('list'))
        form.populate_obj(announcement)
        announcement.update()
        flash(notify_success('Announcement updated!'))
        return mhelp.redirect_url(mhelp.method('list'))
