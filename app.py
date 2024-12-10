from flask import Flask, render_template, request, jsonify
import random
import copy
import time
import tracemalloc

app = Flask(__name__)

nos_gerados = 0
nos_visitados = 0

# Função para criar o tabuleiro
def criar_tabuleiro():
    return [[0 for _ in range(7)] for _ in range(6)]

# Função para verificar se alguém venceu
def verificar_vitoria(tabuleiro, jogador):
    # Verificar linhas
    for row in range(6):
        for col in range(4):
            if all(tabuleiro[row][col + i] == jogador for i in range(4)):
                return True

    # Verificar colunas
    for col in range(7):
        for row in range(3):
            if all(tabuleiro[row + i][col] == jogador for i in range(4)):
                return True

    # Verificar diagonais (direita para baixo)
    for row in range(3):
        for col in range(4):
            if all(tabuleiro[row + i][col + i] == jogador for i in range(4)):
                return True

    # Verificar diagonais (esquerda para baixo)
    for row in range(3):
        for col in range(3, 7):
            if all(tabuleiro[row + i][col - i] == jogador for i in range(4)):
                return True

    return False

# Função para verificar se o tabuleiro está cheio
def tabuleiro_cheio(tabuleiro):
    return all(tabuleiro[0][col] != 0 for col in range(7))

# Função para realizar o movimento
def fazer_movimento(tabuleiro, col, jogador):
    for row in range(5, -1, -1):
        if tabuleiro[row][col] == 0:
            tabuleiro[row][col] = jogador
            return tabuleiro
    return tabuleiro

def medir_desempenho(func, *args, **kwargs):
    global nos_gerados, nos_visitados
    nos_gerados = 0
    nos_visitados = 0

    # Inicia medição de tempo e memória
    tracemalloc.start()
    start_time = time.time()

    # Executar a função
    resultado = func(*args, **kwargs)

    # Finaliza medição de tempo e memória
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    desempenho = {
        "nos_gerados": nos_gerados,
        "nos_visitados": nos_visitados,
        "tempo_execucao": end_time - start_time,
        "memoria_utilizada": peak / 1024
    }

    return resultado, desempenho

def alpha_beta_iterativo(tabuleiro, profundidade, alpha, beta, maximizando):
    melhor_jogada = None
    melhor_valor = -float('inf') if maximizando else float('inf')

    for col in range(7):
        if tabuleiro[0][col] == 0:
            tabuleiro_copy = copy.deepcopy(tabuleiro)
            fazer_movimento(tabuleiro_copy, col, 2 if maximizando else 1)
            valor = jogada_alpha_beta(tabuleiro_copy, profundidade - 1, alpha, beta, not maximizando)

            if maximizando and valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = col
            elif not maximizando and valor < melhor_valor:
                melhor_valor = valor
                melhor_jogada = col

            alpha = max(alpha, melhor_valor) if maximizando else alpha
            beta = min(beta, melhor_valor) if not maximizando else beta

            if beta <= alpha:
                break  # Poda Beta

    return melhor_jogada

# Algoritmo de Aprofundamento Iterativo
def jogada_iterativa(tabuleiro, profundidade_max):
    melhor_jogada = None
    for profundidade in range(1, profundidade_max + 1):
        melhor_jogada = alpha_beta_iterativo(tabuleiro, profundidade, -float('inf'), float('inf'), True)
    return melhor_jogada

# Algoritmo de Poda Alpha-Beta
def jogada_alpha_beta(tabuleiro, profundidade, alpha, beta, maximizando):
    global nos_gerados, nos_visitados

    if profundidade == 0 or tabuleiro_cheio(tabuleiro) or verificar_vitoria(tabuleiro, 1) or verificar_vitoria(tabuleiro, 2):
        nos_visitados += 1
        return avaliar(tabuleiro)
    
    if maximizando:
        melhor_valor = -float('inf')
        melhor_jogada = None
        for col in range(7):
            if tabuleiro[0][col] == 0:
                nos_gerados += 1
                tabuleiro_copy = copy.deepcopy(tabuleiro)
                fazer_movimento(tabuleiro_copy, col, 2)
                valor = jogada_alpha_beta(tabuleiro_copy, profundidade - 1, alpha, beta, False)
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = col
                alpha = max(alpha, melhor_valor)
                if beta <= alpha:
                    break
        return melhor_jogada
    else:
        melhor_valor = float('inf')
        melhor_jogada = None
        for col in range(7):
            if tabuleiro[0][col] == 0:
                tabuleiro_copy = copy.deepcopy(tabuleiro)
                fazer_movimento(tabuleiro_copy, col, 1)
                valor = jogada_alpha_beta(tabuleiro_copy, profundidade - 1, alpha, beta, True)
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = col
                beta = min(beta, melhor_valor)
                if beta <= alpha:
                    break
        return melhor_jogada
    

# Função para escolher a melhor jogada usando Aprofundamento Iterativo ou Poda Alpha-Beta
def ia_jogada(tabuleiro, algoritmo="iterativo", profundidade=3):
    # Verificar jogada vencedora imediata
    for col in range(7):
        if tabuleiro[0][col] == 0:
            tabuleiro_copy = copy.deepcopy(tabuleiro)
            fazer_movimento(tabuleiro_copy, col, 2)
            if verificar_vitoria(tabuleiro_copy, 2):
                return col, {"nos_gerados": 0, "nos_visitados": 0, "tempo_execucao": 0, "memoria_utilizada": 0}

    # Verificar bloqueio de vitória adversária
    for col in range(7):
        if tabuleiro[0][col] == 0:
            tabuleiro_copy = copy.deepcopy(tabuleiro)
            fazer_movimento(tabuleiro_copy, col, 1)
            if verificar_vitoria(tabuleiro_copy, 1):
                return col, {"nos_gerados": 0, "nos_visitados": 0, "tempo_execucao": 0, "memoria_utilizada": 0}

    # Caso nenhum ganho ou bloqueio imediato, usar algoritmo
    if algoritmo == "iterativo":
        jogada, desempenho = medir_desempenho(jogada_iterativa, tabuleiro, profundidade)
    elif algoritmo == "alpha_beta":
        jogada, desempenho = medir_desempenho(jogada_alpha_beta, tabuleiro, profundidade, -float('inf'), float('inf'), True)

    return jogada, desempenho

def avaliar_posicao(tabuleiro, row, col):
    jogador = tabuleiro[row][col]
    adversario = 1 if jogador == 2 else 2
    score = 0

    # Verificar direções
    direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in direcoes:
        count_jogador, count_adversario, espacos_vazios = 0, 0, 0
        for i in range(4):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 6 and 0 <= c < 7:
                if tabuleiro[r][c] == jogador:
                    count_jogador += 1
                elif tabuleiro[r][c] == adversario:
                    count_adversario += 1
                elif tabuleiro[r][c] == 0:
                    espacos_vazios += 1

        # Recompensar jogadas vantajosas e bloquear adversárias
        if count_jogador == 3 and espacos_vazios == 1:
            score += 50
        elif count_adversario == 3 and espacos_vazios == 1:
            score -= 80

    return score

# Função de avaliação para Poda Alpha-Beta
def avaliar(tabuleiro):
    score = 0
    
    if verificar_vitoria(tabuleiro, 2):
        return 10000  # Vitória da IA
    elif verificar_vitoria(tabuleiro, 1):
        return -10000  # Vitória do jogador

    for row in range(6):
        for col in range(7):
            if tabuleiro[row][col] == 0:
                continue
            score += avaliar_posicao(tabuleiro, row, col)

    center_col = 3
    center_count = sum(row[center_col] == 2 for row in tabuleiro)
    score += center_count * 3

    return score

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/jogar', methods=["POST"])
def jogar():
    data = request.get_json()
    tabuleiro = data['tabuleiro']
    jogador = data['jogador']
    col = data['col']
    algoritmo = data['algoritmo']
    profundidade_recebida = int(data['profundidade'])
    
    # Jogada do jogador
    tabuleiro = fazer_movimento(tabuleiro, col, jogador)
    
    # Verificar vitória do jogador
    if verificar_vitoria(tabuleiro, jogador):
        return jsonify({"tabuleiro": tabuleiro, "vitoria": jogador})
    
    # Jogada da IA
    ia_col, metrics = ia_jogada(tabuleiro, algoritmo=algoritmo, profundidade=profundidade_recebida)  # Profundidade de 6
    tabuleiro = fazer_movimento(tabuleiro, ia_col, 2)
    
    # Verificar vitória da IA
    if verificar_vitoria(tabuleiro, 2):
        return jsonify({"tabuleiro": tabuleiro, "vitoria": 2, "metrics": metrics})
    
    return jsonify({"tabuleiro": tabuleiro, "jogadaIA": ia_col, "metrics": metrics})

if __name__ == "__main__":
    app.run(debug=True)
