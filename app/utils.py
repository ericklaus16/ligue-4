import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from datetime import datetime
import os

def create_forecast_plot():
    # Dados fictícios
    x = [1, 2, 3, 4, 5, 6, 7]
    y1 = [3, 5, 2, 5, 7, 9, 8]
    y2 = [1, 2, 1, 3, 4, 5, 3]

    plt.plot(x, y1, color='blue')
    plt.plot(x, y2, color='lightblue')
    plt.xticks([])
    plt.yticks([])

    # Salvar o gráfico em um arquivo temporário com timestamp para evitar conflitos
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # file_path = os.path.join('./app/static', 'plots', f'plot_{timestamp}.png')
    file_path = os.path.join('./app/static', 'plots', f'plot.png')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path)
    plt.close()  # Fecha o gráfico para liberar a memória
    # return f'../static/plots/plot_{timestamp}.png'
    return f'../static/plots/plot.png'

def create_distribution_plot():
    labels = ['Categoria 1', 'Categoria 2', 'Categoria 3', 'Categoria 4']
    sizes = [15, 30, 45, 10]
    colors = ['lightblue', 'steelblue', 'dodgerblue', 'deepskyblue']
    explode = (0.1, 0, 0, 0)  # Separa a primeira fatia

    # Criar o gráfico de pizza
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140) 

    # Mostrar o gráfico
    
    plt.axis('equal')  # Para garantir que o círculo seja desenhado como um círculo
    # Salvar o gráfico em um arquivo temporário com timestamp para evitar conflitos
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # file_path = os.path.join('./app/static', 'plots', f'dist_plot_{timestamp}.png')
    file_path = os.path.join('./app/static', 'plots', f'dist_plot.png')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path)
    plt.close()  # Fecha o gráfico para liberar a memória
    return f'../static/plots/dist_plot.png'

def create_risk_plot():
    investments = ['Ações', 'Títulos', 'Imóveis', 'Fundos Mútuos', 'Criptomoedas']
    risks = [8, 3, 5, 4, 9]  # Escala de risco de 1 a 10
    returns = [10, 4, 6, 5, 12]  # Retornos esperados em %

    # Configurar o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criar gráfico de dispersão para representar risco x retorno
    scatter = ax.scatter(risks, returns, s=300, c=np.arange(len(investments)), cmap='viridis', edgecolor='black', alpha=0.8)

    # Adicionar rótulos para os pontos
    for i, investment in enumerate(investments):
        ax.text(risks[i] + 0.2, returns[i], investment, fontsize=10, ha='left', va='center')

    # Configurar eixos
    # ax.set_title('Riscos vs Retornos de Investimentos', fontsize=16, fontweight='bold')
    # ax.set_xlabel('Risco (1-10)', fontsize=12)
    # ax.set_ylabel('Retorno Esperado (%)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    # Adicionar barra de cores para contexto
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical')
    cbar.set_label('Categorias de Investimento', fontsize=12)

    # Mostrar gráfico
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # filename = f'risk_plot_{timestamp}.png'
    filename = 'risk_plot.png'
    file_path = os.path.join('./app/static/plots', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Salvar o gráfico e retornar o caminho relativo
    plt.savefig(file_path)
    plt.close()
    return f'../static/plots/{filename}'