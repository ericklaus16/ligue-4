from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = "João"
    return render_template('index.html', user = user)

@main.route('/about')
def about():
    return "Página Sobre"
