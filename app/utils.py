import numpy as np
import matplotlib
import yfinance as yf

import seaborn as sns

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from datetime import datetime
import os

def create_forecast_plot(melhor_portfolio):
    ativos = [ativo["Ativo"] for ativo in melhor_portfolio["Portfolio"]]
    alocacao = melhor_portfolio["alocacao"]
    
    # Baixar os preços históricos dos ativos
    precos = {}
    for ativo in ativos:
        try:
            precos[ativo] = yf.download(ativo, period="1y")['Adj Close'].values
        except Exception as e:
            print(f"Erro ao baixar dados para o ativo {ativo}: {e}")
            precos[ativo] = None
    
    # Remover ativos que não possuem dados
    precos = {ativo: preco for ativo, preco in precos.items() if preco is not None}
    
    if not precos:
        raise ValueError("Nenhum dado válido foi encontrado para os ativos.")
    
    # Garantir que todas as séries temporais tenham o mesmo comprimento
    max_len = min(len(preco) for preco in precos.values())
    precos_align = {ativo: preco[:max_len] for ativo, preco in precos.items()}

    # Calcular os retornos diários de cada ativo
    retornos_diarios = {}
    for ativo, preco in precos_align.items():
        retornos_diarios[ativo] = (preco[1:] / preco[:-1] - 1)

    # Calcular o valor do portfólio ao longo do tempo
    valor_portfolio = np.zeros_like(list(precos.values())[0][1:])
    for i, ativo in enumerate(ativos):
        peso = alocacao.get(ativo, 0)
        valor_portfolio += retornos_diarios[ativo] * peso

    # Calcular o Drawdown
    valor_maximo = np.maximum.accumulate(valor_portfolio)
    drawdown = (valor_portfolio - valor_maximo) / valor_maximo

    # Plotar o gráfico de Drawdown
    plt.figure(figsize=(10, 6))
    plt.plot(drawdown, label="Drawdown do Portfólio", color='red', linewidth=2)
    plt.title("Drawdown do Portfólio", fontsize=16)
    plt.xlabel("Tempo (Dias)", fontsize=12)
    plt.ylabel("Drawdown", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Salvar o gráfico em um arquivo temporário com timestamp para evitar conflitos
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # file_path = os.path.join('./app/static', 'plots', f'plot_{timestamp}.png')
    file_path = os.path.join('./app/static', 'plots', f'plot.png')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path)
    plt.close()  # Fecha o gráfico para liberar a memória
    # return f'../static/plots/plot_{timestamp}.png'
    return f'../static/plots/plot.png'

def create_distribution_plot(melhor_portfolio):
    ativos = [ativo["Ativo"] for ativo in melhor_portfolio["Portfolio"]]
    alocacao = melhor_portfolio["alocacao"]
    total_investido = sum(alocacao.values())
    
    sizes = [alocacao.get(ativo, 0) for ativo in ativos]
    colors = plt.cm.Paired.colors[:len(sizes)]  # Usando uma paleta de cores

    # Criando o gráfico de pizza
    plt.pie(sizes, labels=ativos, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True, explode=(0.1, 0, 0, 0, 0))

    legend_labels = [f'{ativo} - R${alocacao.get(ativo, 0):,.2f} ({alocacao.get(ativo, 0)/total_investido*100:.1f}%)' for ativo in ativos]
    plt.legend(legend_labels, loc='upper left', fontsize=10, title="Ativos", bbox_to_anchor=(1, 1))

    plt.axis('equal')  # Para garantir que o gráfico fique circular

    plt.tight_layout()

    # Salvar o gráfico em um arquivo temporário com timestamp para evitar conflitos
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # file_path = os.path.join('./app/static', 'plots', f'dist_plot_{timestamp}.png')
    file_path = os.path.join('./app/static', 'plots', f'dist_plot.png')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path)
    plt.close()  # Fecha o gráfico para liberar a memória
    return f'../static/plots/dist_plot.png'

def create_risk_plot(melhor_portfolio):
    ativos = melhor_portfolio["Portfolio"]
    risks = [ativo["Volatilidade"] for ativo in ativos]  # Usando volatilidade como risco
    returns = [ativo["Retorno Médio"] * 100 for ativo in ativos]  # Retorno em % para facilitar a visualização
    sharpe_ratios = [ativo["Índice de Sharpe"] for ativo in ativos]

    # Definir diferentes formas para os pontos
    markers = ['o', 's', '^', 'D', 'v']  # Círculo, Quadrado, Triângulo, Diamante, Triângulo invertido
    colors = plt.cm.viridis(np.linspace(0, 1, len(ativos)))  # Gerar cores com base no número de ativos

    # Configurando o gráfico de dispersão
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando gráfico de dispersão para cada ativo com diferentes formas
    for i, ativo in enumerate(ativos):
        ax.scatter(risks[i], returns[i], s=300, c=[colors[i]], marker=markers[i], label=ativo["Ativo"], edgecolor='black', alpha=0.8)

        # Adicionando rótulo ao lado de cada ponto
        ax.text(risks[i] + 0.01, returns[i] + 0.5, ativo["Ativo"], fontsize=10, ha='left', va='center')

    # Configurar eixos
    ax.set_title('Risco vs Retorno de Ativos', fontsize=16, fontweight='bold')
    ax.set_xlabel('Volatilidade (Risco)', fontsize=12)
    ax.set_ylabel('Retorno Esperado (%)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    # Adicionar barra de cores para Sharpe Ratio
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(sharpe_ratios), vmax=max(sharpe_ratios))), ax=ax)
    cbar.set_label('Índice de Sharpe', fontsize=12)

    # Legenda personalizada à direita e com mais espaçamento entre itens
    ax.legend(title="Ativos", fontsize=10, loc='right', bbox_to_anchor=(1, 0.5), labelspacing=1.5)
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # filename = f'risk_plot_{timestamp}.png'
    filename = 'risk_plot.png'
    file_path = os.path.join('./app/static/plots', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Salvar o gráfico e retornar o caminho relativo
    plt.savefig(file_path)
    plt.close()
    return f'../static/plots/{filename}'