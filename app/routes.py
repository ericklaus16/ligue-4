from flask import Blueprint, render_template, url_for
import os
from .utils import create_forecast_plot, create_distribution_plot, create_risk_plot

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = "Eric"
    return render_template('index.html', user=user)

@main.route('/results')
def about():
    forecast_plot_path = create_forecast_plot()  
    distribution_plot_path = create_distribution_plot()
    risk_plot_path = create_risk_plot()

    return render_template('results.html', forecast_plot_url=forecast_plot_path, distribution_plot_url=distribution_plot_path, risk_plot_url=risk_plot_path)
