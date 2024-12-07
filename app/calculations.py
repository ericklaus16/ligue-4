import yfinance as yf
import numpy as np

investimentos = []
profundidade_maxima = 2

limite_risco_baixo = 0.02
limite_risco_medio = 0.05

def calcular_volatilidade(precos):
    retornos = precos.pct_change()  # Calcula os retornos diários
    volatilidade = retornos.std()  # Desvio padrão dos retornos
    return volatilidade.iloc[0]  # Garantir que retornamos um único valor

def calcular_retorno_medio(precos):
    retornos = precos.pct_change()  # Calcula os retornos diários
    retorno_medio = retornos.mean()  # Média dos retornos diários
    return retorno_medio.iloc[0]  # Garantir que retornamos um único valor

def calcular_indice_sharpe(retorno_medio, volatilidade, taxa_livre_risco=0.05):
    # Supondo uma taxa livre de risco anual de 5%
    sharpe_ratio = (retorno_medio - taxa_livre_risco) / volatilidade
    return sharpe_ratio

def classificar_risco(volatilidade, sharpe_ratio):
    if volatilidade < 0.02 and sharpe_ratio > 1.0:
        return "low"
    elif 0.02 <= volatilidade < 0.05 or sharpe_ratio >= 0.5:
        return "medium"
    else:
        return "high"

def calcular_risco_ativos(ticker, periodo="1y"):
    # Baixando os dados históricos de preços
    ativo = yf.download(ticker, period=periodo)
    
    # Calculando volatilidade e retorno médio
    volatilidade = calcular_volatilidade(ativo['Adj Close'])
    retorno_medio = calcular_retorno_medio(ativo['Adj Close'])
    
    # Calculando índice de Sharpe
    sharpe_ratio = calcular_indice_sharpe(retorno_medio, volatilidade)
    
    # Classificando o risco
    risco = classificar_risco(volatilidade, sharpe_ratio)
    
    # Exibindo os resultados
    print(f"Ativo: {ticker}")
    print(f"Volatilidade: {volatilidade:.4f}")  # Agora deve funcionar corretamente
    print(f"Retorno Médio: {retorno_medio:.4f}")
    print(f"Índice de Sharpe: {sharpe_ratio:.4f}")
    print(f"Classificação de Risco: {risco}\n")

    investimentos.append({
        "Ativo": ticker,
        "Volatilidade": volatilidade,
        "Retorno Médio": retorno_medio,
        "Índice de Sharpe": sharpe_ratio,
        "Classificação de Risco": risco
    })

def aprofundamento_iterativo(valor_total, risco_desejado):
    melhores_portfolios = []
    profundidade_maxima = len(investimentos) if len(investimentos) < 5 else 5

    # Filtrar os ativos pelo risco desejado
    ativos_filtrados_por_risco = [
        ativo for ativo in investimentos if ativo["Classificação de Risco"].lower() == risco_desejado.lower()
    ]

    if not ativos_filtrados_por_risco:
        return { "erro": "Nenhum ativo encontrado com o risco desejado" }

    def avaliar_portfolio(portfolio):
        volatilidades = [ativo["Volatilidade"] for ativo in portfolio]
        sharpe_ratios = [ativo["Índice de Sharpe"] for ativo in portfolio]

        volatilidade_media = np.mean(volatilidades)
        sharpe_ratio_media = np.mean(sharpe_ratios)

        return volatilidade_media, sharpe_ratio_media

    def buscar_portfolio(ativos, profundidade_total, portfolio_atual):
        if profundidade_total == 0: ## Condição de parada
            volatilidade_media, sharpe_ratio_media = avaliar_portfolio(portfolio_atual)
            
            if volatilidade_media < 0.02 and sharpe_ratio_media > 1.0 and risco_desejado == "low":
                risco = "Baixo Risco"
            elif 0.02 <= volatilidade_media < 0.05 or sharpe_ratio_media >= 0.5 and risco_desejado == "medium":
                risco = "Médio Risco"
            else:
                risco = "Alto Risco"

            melhores_portfolios.append({
                "Portfolio": portfolio_atual,
                "Volatilidade Média": volatilidade_media,
                "Sharpe Ratio Médio": sharpe_ratio_media,
                "Classificação de Risco": risco
            })
            return

        for i in range(len(ativos)):
            novo_portfolio = portfolio_atual + [ativos[i]]
            buscar_portfolio(ativos[i+1:], profundidade_total - 1, novo_portfolio)

    buscar_portfolio(ativos_filtrados_por_risco, profundidade_maxima, [])

    melhor_portfolio = max(
        melhores_portfolios,
        key=lambda x: (x["Sharpe Ratio Médio"], x["Volatilidade Média"])
    )

    total_sharpe = sum([ativo["Índice de Sharpe"] for ativo in melhor_portfolio["Portfolio"]])

    alocacao = {
        ativo["Ativo"]: float(valor_total) * float(ativo["Índice de Sharpe"] / total_sharpe)
        for ativo in melhor_portfolio["Portfolio"]
    }

    melhor_portfolio["alocacao"] = alocacao
    # print(melhor_portfolio["alocacao"])

    return melhor_portfolio

def poda_alfa_beta(ativos, profundidade_maxima, alpha, beta):
    # Piazada, aqui é o seguinte: a gente vai fazer um loop para cada ativo
    # e dentro desse loop, a gente vai fazer outro loop para cada profundidade
    # que a gente quer calcular. Então, a cada iteração, a gente vai calcular
    # o risco de um ativo em uma profundidade diferente e, se o risco for
    # maior que o alpha ou menor que o beta, a gente vai adicionar o ativo
    # em uma lista de ativos para serem podados

    return None