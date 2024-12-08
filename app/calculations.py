import yfinance as yf
from itertools import combinations

def buscar_ativos(ativos):
    data = {}

    for ativo in ativos:
        try:
            ativo += ".SA"
            stock_data = yf.Ticker(ativo).history(period="1y")
            if 'Close' not in stock_data.columns:
                raise ValueError(f"Dados 'Close' ausentes para o ativo {ativo}")
            data[ativo] = {
                "returns": stock_data["Close"].pct_change().dropna(),
                "risk": stock_data["Close"].pct_change().std(),
                "average_return": stock_data["Close"].pct_change().mean()
            }
        except Exception as e:
            data[ativo] = {"erro": f"Erro ao buscar ativo: {e}"}
    return data

def calcular_alocacao(portfolio, budget, data):
    alocacao = {}
    total_retorno = sum(data[ativo]["average_return"] for ativo in portfolio)

    for ativo in portfolio:
        proporcao = data[ativo]["average_return"] / total_retorno
        alocacao[ativo] = round(float(budget) * float(proporcao), 3)

    return alocacao

def aprofundamento_iterativo_recursivo(data, max_depth, current_depth, portfolio, risk_level, visited, best):
    if(current_depth > max_depth):
        return best
    
    max_risk = {"low": 0.05, "medium": 0.15, "high": 0.3}[risk_level]

    portfolio_return = sum(data[asset]["average_return"] for asset in portfolio)
    portfolio_risk = sum(data[asset]["risk"] for asset in portfolio)

    if portfolio_risk <= max_risk and portfolio_return > best[0]:
        best = (portfolio_return, portfolio)

    for asset in data:
        if asset not in visited:
            visited.add(asset)
            best = aprofundamento_iterativo_recursivo(
                data, max_depth, current_depth + 1, 
                portfolio + [asset], risk_level, visited, best
            )
            visited.remove(asset)

    return best

def aprofundamento_iterativo_ii(data, budget, risk_level):
    best_portfolio = (float("-inf"), [])

    for max_depth in range(1, len(data)):
        visited = set()
        best_portfolio = aprofundamento_iterativo_recursivo(
            data, max_depth, 0, [], risk_level, visited, best_portfolio
        )
    
    return best_portfolio[1], best_portfolio[0]

def otimizar_portfolio(ativos, investment_amount, investment_risk):
    data = buscar_ativos(ativos)
    print("Erros em ativos:")
    for asset, info in data.items():
        if 'erro' in info:
            print(f"{asset}: {info['erro']}")
    
    assets_validos = {k: v for k, v in data.items() if "erro" not in v}

    if not assets_validos:
        return { "Erro:": "Nenhum ativo válido para otimização. Verifique os tickers ou tente novamente." }
    
    portfolio_interativo, retorno_interativo = aprofundamento_iterativo_ii(assets_validos, investment_amount, investment_risk)
    # portfolio_alpha_beta, retorno_alpha_beta = poda_alfa_beta(assets_validos, 3, 0.1, 0.1)

    alocacao_interativo = calcular_alocacao(portfolio_interativo, investment_amount, assets_validos)

    return {
        "Iterativo": { 
            "Portfolio:" : portfolio_interativo, 
            "Retorno:" : retorno_interativo,
            "Alocacao": alocacao_interativo
        },
        # "Alpha-Beta": { "Portfolio:" : portfolio_alpha_beta, "Retorno:" : retorno_alpha_beta }
    }

def poda_alfa_beta(ativos, profundidade_maxima, alpha, beta):
    # Piazada, aqui é o seguinte: a gente vai fazer um loop para cada ativo
    # e dentro desse loop, a gente vai fazer outro loop para cada profundidade
    # que a gente quer calcular. Então, a cada iteração, a gente vai calcular
    # o risco de um ativo em uma profundidade diferente e, se o risco for
    # maior que o alpha ou menor que o beta, a gente vai adicionar o ativo
    # em uma lista de ativos para serem podados

    return None
