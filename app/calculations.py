import yfinance as yf

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
    # Piazada, aqui é o seguinte: a gente vai fazer um loop para cada ativo
    # e dentro desse loop, a gente vai fazer outro loop para cada profundidade
    # que a gente quer calcular. Então, a cada iteração, a gente vai calcular
    # o risco de um ativo em uma profundidade diferente.

    melhores_portfolios = []

    def avaliar_portfolio(portfolio):
        # Calcular volatilidade media do portfólio

        # Calcular índice Sharpe médio do portfólio

        # Retornar os dois valores
        return None, None
    
    def buscar_portfolio(ativos, profundidade_total, portfolio_atual):
        # Se a profundida máxima for alcançada, avaliar o portfólio

        # Loop para iterar sobre os ativos e explorar as combinações

        # Acho que esse método não vai retornar nada

        return None

    # buscar_portfolio(ativos, profundidade_maxima, [])

    return melhores_portfolios

def poda_alfa_beta(ativos, profundidade_maxima, alpha, beta):
    # Piazada, aqui é o seguinte: a gente vai fazer um loop para cada ativo
    # e dentro desse loop, a gente vai fazer outro loop para cada profundidade
    # que a gente quer calcular. Então, a cada iteração, a gente vai calcular
    # o risco de um ativo em uma profundidade diferente e, se o risco for
    # maior que o alpha ou menor que o beta, a gente vai adicionar o ativo
    # em uma lista de ativos para serem podados

    return None