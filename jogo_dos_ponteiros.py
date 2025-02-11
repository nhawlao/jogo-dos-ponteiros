import random
from collections import Counter
from aima.search import Problem

class JogoPonteiros(Problem):
    """
    Jogo no qual o objetivo é fazer com que todas as setas
    de um tabuleiro 2x2 gerado aleatoriamente apontem para
    a mesma direção

    Cada estado (state) é representado por uma tupla ((tabuleiro), pos_agente), onde:
    tabuleiro:
        uma 4-tupla com inteiros de 0 a 3, mapeada pela rotação de uma seta no
        sentido horário [0: esquerda, 1: cima, 2: direita, 3: baixo]
    pos_agente:
        um inteiro de 0 a 3 que representa a posição atual do agente no tabuleiro
    """
    def __init__(self, pos_inicial=0):
        
        tabuleiro = tuple(random.randint(0,3) for _ in range(4))
        self.initial = (tabuleiro, pos_inicial)
        
        self.goal = self.gera_estado_final(tabuleiro)
        
        self.exiba_tabuleiro(tabuleiro)

    def gera_estado_final(self, tabuleiro):
        """
        Gera tabuleiro de estado final considerando
        a posição mais comum dentro do estado inicial
        """
        direcao_comum = Counter(tabuleiro).most_common(1)[0][0]
        return (tuple([direcao_comum] * 4), None)  # Agent position doesn't matter in goal state

    def exiba_tabuleiro(self, tabuleiro):
        """
        Exibe o tabuleiro usando as direções
        declaradas a partir de suas posições
        no vetor, seguindo uma rotação no
        sentido horario.
        <:0 ^:1 >:2 v:3
        """
        ponteiros = ['<', '^', '>', 'v']
        print(f"""
         {ponteiros[tabuleiro[0]]} | {ponteiros[tabuleiro[1]]}
        -------
         {ponteiros[tabuleiro[2]]} | {ponteiros[tabuleiro[3]]}
        """)

    def actions(self, state):
        """
        Retorna as possíveis ações, considerando
        a posição atual do agente dentro do tabuleiro:

            0 1
            2 3

        """
        tabuleiro, pos_agente = state
        acoes_possiveis = ['HORARIO', 'ANTIHORARIO']
        
        if pos_agente in (2, 3):
            acoes_possiveis.append('CIMA')
        if pos_agente in (0, 1):
            acoes_possiveis.append('BAIXO')
        if pos_agente in (0, 2):
            acoes_possiveis.append('DIREITA')
        if pos_agente in (1, 3):
            acoes_possiveis.append('ESQUERDA')
            
        return acoes_possiveis

    def result(self, state, action):
        """
        Retorna o um novo estado a partir
        da execução de ações sobre o estado
        atual.
        """
        tabuleiro, pos_agente = state
        novo_tabuleiro = list(tabuleiro)
        nova_pos = pos_agente

        if action == 'HORARIO':
            novo_tabuleiro[pos_agente] = (tabuleiro[pos_agente] + 1) % 4
        elif action == 'ANTIHORARIO':
            novo_tabuleiro[pos_agente] = (tabuleiro[pos_agente] - 1) % 4
        elif action == 'ESQUERDA':
            nova_pos = pos_agente - 1
        elif action == 'DIREITA':
            nova_pos = pos_agente + 1
        elif action == 'CIMA':
            nova_pos = pos_agente - 2
        elif action == 'BAIXO':
            nova_pos = pos_agente + 2

        novo_estado = (tuple(novo_tabuleiro), nova_pos)
        self.exiba_tabuleiro(novo_tabuleiro)
        return novo_estado

    def goal_test(self, state):
        """
        Retorna True caso o estado atual seja o estado final
        """
        tabuleiro, _ = state
        tabuleiro_final, _ = self.goal
        if tabuleiro == tabuleiro_final:
          self.exiba_tabuleiro(tabuleiro)
        return tabuleiro == tabuleiro_final

    def path_cost(self, c, state1, action, state2):
        """
        Retorna o custo de um caminho
        """
        return c + 1

    def h(self, node):
        """
        Função heurística: retorna o menor número de rotações
        necessárias para alcançar o estado final.
        """
        estado, _ = node.state
        tabuleiro_final, _ = self.goal
        
        return sum(min(abs(estado[i] - tabuleiro_final[i]), 
                      4 - abs(estado[i] - tabuleiro_final[i])) 
                  for i in range(4))