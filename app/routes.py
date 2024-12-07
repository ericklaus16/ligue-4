from flask import Blueprint, render_template, request, jsonify
import yfinance as yf

from .utils import create_forecast_plot, create_distribution_plot, create_risk_plot
from .calculations import calcular_risco_ativos, aprofundamento_iterativo, poda_alfa_beta

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

@main.route('/calcular-risco', methods=['POST'])
def calcular_risco():
    data = request.get_json()  # Recebe os dados enviados no fetch
    investment_amount = data.get("investmentAmount")
    investment_type = data.get("investmentType")
    investment_interest = data.get("investmentInterest")  # Lista de ativos
    investment_risk = data.get("investmentRisk")  # Risco selecionado pelo usuário

    erros = []

    for ativo in investment_interest:
        try:
            ativo_br = ativo + ".SA"
            calcular_risco_ativos(ativo_br)
        except Exception as e:
            erros.append({
                "ativo": ativo,
                "erro": f"Erro ao calcular: {str(e)}"
            })  
    
    melhor_portfolio = aprofundamento_iterativo(investment_amount, investment_risk)

    return jsonify({
        "investment_amount": investment_amount,
        "investment_risk": investment_risk,
        "melhor_portfolio": melhor_portfolio,
        "erros": erros
    })