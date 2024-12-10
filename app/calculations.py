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

    total_alocacao = sum(alocacao.values())

    if float(total_alocacao) > float(budget):
        ajuste = total_alocacao - budget

        for ativo in alocacao:
            alocacao[ativo] -= (alocacao[ativo] / total_alocacao) * ajuste

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

def aprofundamento_iterativo(data, budget, risk_level):
    best_portfolio = (float("-inf"), [])

    for max_depth in range(1, len(data)):
        visited = set()
        best_portfolio = aprofundamento_iterativo_recursivo(
            data, max_depth, 0, [], risk_level, visited, best_portfolio
        )
    
    return best_portfolio[1], best_portfolio[0]

def poda_alfa_beta_recursivo(data, depth, alpha, beta, portfolio, risk_level, maximizing_player):
    if depth == 0 or not data:
        # Caso base: retorna o retorno total do portfólio se respeitar o risco
        max_risk = {"low": 0.05, "medium": 0.15, "high": 0.3}[risk_level]
        portfolio_return = sum(data[asset]["average_return"] for asset in portfolio if asset in data)
        portfolio_risk = sum(data[asset]["risk"] for asset in portfolio if asset in data)
        if portfolio_risk <= max_risk:
            return portfolio_return, portfolio
        return float("-inf"), []

    if maximizing_player:
        max_eval = float("-inf")
        best_portfolio = []

        for asset in data:
            if asset not in portfolio:  # Evita que o ativo seja repetido no portfólio
                new_data = {k: v for k, v in data.items() if k != asset}  # Remove o ativo atual para a próxima chamada
                eval_value, current_portfolio = poda_alfa_beta_recursivo(
                    new_data, depth - 1, alpha, beta, portfolio + [asset], risk_level, False
                )
                if eval_value > max_eval:
                    max_eval = eval_value
                    best_portfolio = current_portfolio
                alpha = max(alpha, eval_value)
                if beta <= alpha:  # Poda
                    break

        return max_eval, best_portfolio
    else:
        min_eval = float("inf")
        best_portfolio = []

        for asset in data:
            if asset not in portfolio:  # Evita que o ativo seja repetido no portfólio
                new_data = {k: v for k, v in data.items() if k != asset}  # Remove o ativo atual para a próxima chamada
                eval_value, current_portfolio = poda_alfa_beta_recursivo(
                    new_data, depth - 1, alpha, beta, portfolio + [asset], risk_level, True
                )
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_portfolio = current_portfolio
                beta = min(beta, eval_value)
                if beta <= alpha:  # Poda
                    break

        return min_eval, best_portfolio

def poda_alfa_beta(data, depth, alpha, beta, maximizing_player, risk_level, budget):
    result_value, result_portfolio = poda_alfa_beta_recursivo(data, depth, alpha, beta, [], risk_level, maximizing_player)

    if result_value > 0:
        result_portfolio = [asset for asset in result_portfolio if asset in data]
        alocacao = calcular_alocacao(result_portfolio, budget, data)
        total_alocacao = sum(alocacao.values())

        if total_alocacao > budget:
            ajuste = total_alocacao - budget

            for asset in result_portfolio:
                alocacao[asset] -= (alocacao[asset] / total_alocacao) * ajuste

        return result_value, result_portfolio

def otimizar_portfolio(ativos, investment_amount, investment_risk):
    data = buscar_ativos(ativos)
    print("Erros em ativos:")

    for asset, info in data.items():
        if 'erro' in info:
            print(f"{asset}: {info['erro']}")
    
    assets_validos = {k: v for k, v in data.items() if "erro" not in v and "average_return" in v and "risk" in v}

    max_depth = len(assets_validos)

    if not assets_validos:
        return { "Erro:": "Nenhum ativo válido para otimização. Verifique os tickers ou tente novamente." }
    
    portfolio_interativo, retorno_interativo = aprofundamento_iterativo(assets_validos, investment_amount, investment_risk)
    
    retorno_alpha_beta, portfolio_alpha_beta = poda_alfa_beta(assets_validos, max_depth, float("-inf"), float("inf"), True, investment_risk, investment_amount)

    portfolio_alpha_beta = [asset for asset in portfolio_alpha_beta if asset in assets_validos]

    alocacao_interativo = calcular_alocacao(portfolio_interativo, investment_amount, assets_validos)
    alocacao_alpha_beta = calcular_alocacao(portfolio_alpha_beta, investment_amount, assets_validos)

    return {
        "Iterativo": { 
            "Portfolio:" : portfolio_interativo, 
            "Retorno:" : retorno_interativo,
            "Alocacao": alocacao_interativo
        },
        "Alpha-Beta": { 
            "Portfolio:" : portfolio_alpha_beta, 
            "Retorno:" : retorno_alpha_beta,
            "Alocacao": alocacao_alpha_beta
        }
    }