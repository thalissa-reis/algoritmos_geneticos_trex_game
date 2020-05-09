import random
import numpy as np
from chrome_trex import DinoGame


# Sinta-se livre para brincar com os valores abaixo

CHANCE_MUT = .2      # Chance de mutação de um peso qualquer
CHANCE_CO = .25      # Chance de crossing over de um peso qualquer
NUM_INDIVIDUOS = 15  # Tamanho da população
NUM_MELHORES = 8     # Número de indivíduos que são mantidos de uma geração para a próxima


def ordenar_lista(lista, ordenacao, decrescente=True):
    """
    Argumentos da Função:
        lista: lista de números a ser ordenada.
        ordenacao: lista auxiliar de números que define a prioridade da
        ordenação.
        decrescente: variável booleana para definir se a lista `ordenacao`
        deve ser ordenada em ordem crescente ou decrescente.
    Saída:
        Uma lista com o conteúdo de `lista` ordenada com base em `ordenacao`.
    Por exemplo,
        ordenar_lista([2, 4, 5, 6], [7, 2, 5, 4])
        # retorna [2, 5, 6, 4]
        ordenar_lista([1, 5, 4, 3], [3, 8, 2, 1])
        # retorna [5, 1, 4, 3]
    """
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]


def populacao_aleatoria(n):
    populacao=[]
    for i in range(n):
        individuo=np.random.uniform(-20,20,(3,10))
        populacao.append(individuo)
    return populacao

def valor_das_acoes(individuo, estado):
    acoes = individuo @ estado
    return acoes

def melhor_jogada(individuo, estado):
    acoes = valor_das_acoes(individuo, estado)
    acao = np.argmax(acoes)
    return acao

def mutacao(individuo):
    for i in range(len(individuo)):
        for j in range(len(individuo[0])):
            chance = np.random.uniform(0,1,1)
            if chance <= CHANCE_MUT:
                multiplicador=np.random.uniform(0.7,1.8,1)
                individuo[i][j] = individuo[i][j]*multiplicador

def crossover(individuo1, individuo2):
   filho = individuo1.copy()
   for i in range(len(filho)):
       for j in range(len(filho[0])):
           chance = np.random.uniform(0,1,1)
           if chance <= CHANCE_CO:
               filho[i][j]=individuo2[i][j]
   return filho

def calcular_fitness(jogo, individuo):
    jogo.reset()
    while not jogo.game_over:
        estado = jogo.get_state()
        acao = melhor_jogada(individuo,estado)
        jogo.step(acao)
    return jogo.get_score()

def proxima_geracao(populacao, fitness):
    populacao_ordenada=ordenar_lista(populacao, fitness)
    proxima_ger = []
    populacao_mantida=populacao_ordenada[0:NUM_MELHORES]
    for individuo_antigo in populacao_mantida:
        proxima_ger.append(individuo_antigo)
    while len(proxima_ger) < NUM_INDIVIDUOS:
        pais =random.choices(populacao_mantida, k = 2)
        mae=pais[0]
        pai=pais[1]
        filho = crossover(mae,pai)
        mutacao(filho)
        proxima_ger.append(filho)
    return proxima_ger

def mostrar_melhor_individuo(jogo, populacao, fitness):
    fps_antigo = jogo.fps
    jogo.fps = 100
    ind = populacao[max(range(len(populacao)), key=lambda i: fitness[i])]
    print('Melhor individuo:', ind)
    while True:
        if input('Pressione enter para rodar o melhor agente. Digite q para sair. ') == 'q':
            jogo.fps = fps_antigo
            return
        fit = calcular_fitness(jogo, ind)
        print('Fitness: {:4.1f}'.format(jogo.get_score()))


###############################
# CÓDIGO QUE RODA O ALGORITMO #
###############################

# Referência: for loop (for x in lista)
#             list.append()

# OBS: Todos os prints dentro dessa função são opcionais.
#      Eles estão aqui para facilitar a visualização do algoritmo.

num_geracoes = 100
jogo = DinoGame(fps=50_000)

populacao = populacao_aleatoria(NUM_INDIVIDUOS)

print('ger | fitness\n----+-' + '-'*5*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    fitness = []
    for individuo_g in populacao:
        fitness_individuo=calcular_fitness(jogo, individuo_g)
        fitness.append(fitness_individuo)
    populacao = proxima_geracao(populacao, fitness)

    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))

    # Opcional: parar se o fitness estiver acima de algum valor (p.ex. 300)

# Calcule a lista de fitness para a última geração
fitness=[]
for individuo_g in populacao:
    fitness_individuo=calcular_fitness(jogo,individuo_g)
    fitness.append(fitness_individuo)
mostrar_melhor_individuo(jogo, populacao, fitness)
