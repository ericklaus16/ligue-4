import yfinance as yf
import numpy as np

investimentos = []

# Função para calcular a volatilidade (desvio padrão)
def calcular_volatilidade(precos):
    retornos = precos.pct_change()  # Calcula os retornos diários
    volatilidade = retornos.std()  # Desvio padrão dos retornos
    return volatilidade.iloc[0]  # Garantir que retornamos um único valor

# Função para calcular o retorno médio
def calcular_retorno_medio(precos):
    retornos = precos.pct_change()  # Calcula os retornos diários
    retorno_medio = retornos.mean()  # Média dos retornos diários
    return retorno_medio.iloc[0]  # Garantir que retornamos um único valor

# Função para calcular o índice de Sharpe
def calcular_indice_sharpe(retorno_medio, volatilidade, taxa_livre_risco=0.05):
    # Supondo uma taxa livre de risco anual de 5%
    sharpe_ratio = (retorno_medio - taxa_livre_risco) / volatilidade
    return sharpe_ratio

# Função para classificar o risco
def classificar_risco(volatilidade, sharpe_ratio):
    if volatilidade < 0.02 and sharpe_ratio > 1.0:
        return "Baixo Risco"
    elif 0.02 <= volatilidade < 0.05 or sharpe_ratio >= 0.5:
        return "Médio Risco"
    else:
        return "Alto Risco"

# Função principal para obter dados e calcular risco
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

# Exemplo de uso com ativos
ativos = ["AAPL", "MSFT", "GOOG", "TSLA"]  # Tickers de ações da Apple, Microsoft, Google, Tesla

# Ações brasileiras precisam do sufixo .SA, por exemplo 'AMAR3.SA' é a açao das americanas.

# for ativo in ativos:
#     calcular_risco_ativos(ativo)

def aprofundamento_iterativo(ativos, profundidade_maxima):
    melhores_portfolios = []

    def avaliar_portfolio(portfolio):
        volatilidades = [calcular_volatilidade(yf.download(ativo, period="1y")['Adj Close']) for ativo in portfolio]
        retornos_medios = [calcular_retorno_medio(yf.download(ativo, period="1y")['Adj Close']) for ativo in portfolio]
        sharpe_ratios = [calcular_indice_sharpe(retorno, volatilidade) for retorno, volatilidade in zip(retornos_medios, volatilidades)]

        volatilidade_media = np.mean(volatilidades)
        sharpe_ratio_medio = np.mean(sharpe_ratios)

        return volatilidade_media, sharpe_ratio_medio

    def buscar_portfolio(ativos, profundidade_total, portfolio_atual):
        if profundidade_total == 0:
            volatilidade_media, sharpe_ratio_medio = avaliar_portfolio(portfolio_atual)
            risco = classificar_risco(volatilidade_media, sharpe_ratio_medio)
            melhores_portfolios.append({
                "Portfolio": portfolio_atual,
                "Volatilidade Média": volatilidade_media,
                "Sharpe Ratio Médio": sharpe_ratio_medio,
                "Classificação de Risco": risco
            })
            return

        for i in range(len(ativos)):
            novo_portfolio = portfolio_atual + [ativos[i]]
            buscar_portfolio(ativos[i+1:], profundidade_total - 1, novo_portfolio)

    buscar_portfolio(ativos, profundidade_maxima, [])
    return melhores_portfolios

ativos = ["AAPL", "MSFT", "GOOG", "TSLA"]
profundidade_maxima = 2
melhores_portfolios = aprofundamento_iterativo(ativos, profundidade_maxima)

for portfolio in melhores_portfolios:
    print(f"Portfolio: {portfolio['Portfolio']}")
    print(f"Volatilidade Média: {portfolio['Volatilidade Média']:.4f}")
    print(f"Sharpe Ratio Médio: {portfolio['Sharpe Ratio Médio']:.4f}")
    print(f"Classificação de Risco: {portfolio['Classificação de Risco']}\n")

def poda_alfa_beta(ativos, profundidade_maxima, alpha, beta):
    # Piazada, aqui é o seguinte: a gente vai fazer um loop para cada ativo
    # e dentro desse loop, a gente vai fazer outro loop para cada profundidade
    # que a gente quer calcular. Então, a cada iteração, a gente vai calcular
    # o risco de um ativo em uma profundidade diferente e, se o risco for
    # maior que o alpha ou menor que o beta, a gente vai adicionar o ativo
    # em uma lista de ativos para serem podados

    return None