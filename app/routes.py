from flask import Blueprint, render_template, request, jsonify
import yfinance as yf

from .utils import create_forecast_plot, create_distribution_plot, create_risk_plot
from .calculations import calcular_risco_ativos, aprofundamento_iterativo, poda_alfa_beta

main = Blueprint('main', __name__)

melhor_portfolio = None

@main.route('/')
def home():
    user = "Eric"
    return render_template('index.html', user=user)

@main.route('/results')
def about():
    return render_template('results.html')

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
    create_forecast_plot(melhor_portfolio)  
    create_distribution_plot(melhor_portfolio)
    create_risk_plot(melhor_portfolio)

    return jsonify({
        "investment_amount": investment_amount,
        "investment_risk": investment_risk,
        "melhor_portfolio": melhor_portfolio,
        "erros": erros
    })