from flask import Blueprint, render_template

indexController = Blueprint('indexController', __name__)


@indexController.route('/')
def index():
    return render_template('index.html')
