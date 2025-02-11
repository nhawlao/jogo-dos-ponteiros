from jogo_dos_ponteiros import JogoPonteiros
from aima.search import *
import random

def __main__():
    """
    Função para teste do problema/solução
    Escolha qualquer algoritmo de busca dentro do arquivo search,
    ou utilize o A*
    """
    jogo = JogoPonteiros(random.randint(0,3))
    print(astar_search(jogo).solution())