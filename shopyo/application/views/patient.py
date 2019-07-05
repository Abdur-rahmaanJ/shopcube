from flask import (
    Blueprint, render_template, request, redirect, url_for
    )
from models import db, Patients
from flask_sqlalchemy import sqlalchemy
from settings import get_value

patient_blueprint = Blueprint('patient', __name__, url_prefix='/patient')
