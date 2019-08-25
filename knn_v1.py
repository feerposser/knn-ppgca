from math import sqrt

# Dados fictícios. A chave é a classe e o conteúdo a localização dos pontos no gráfico.
dataset = {'a': [[1, 2],
                 [2, 3],
                 [3, 1]],
           'b': [[6, 5],
                 [7, 7],
                 [8, 6]]
           }

# O que estamos tentar descobrir a qual pertence.
new_feature = [5, 7]


def k_nearest_neighbors(data, predict, k=5):
    """

    :param data: Dataset
    :param predict: Ponto que queremos classificar
    :param k:
    :return:
    """
    # Lista que armazenará a classe do ponto e a distância.
    distances = []

    for i in data:
        for j in data[i]:
            # Percorre os pontos, armazena na lista a classe e a distância até o ponto que queremos encontrar
            distances.append([i, sqrt((j[0] - predict[0]) ** 2 + (j[1] - predict[1]) ** 2)])

    # Com o quicksort ele ordena a lista pela ordem crescente de distâncias e depois armazena os 5 primeiros na var.
    common_sorted = sorted(distances, key=lambda distances: distances[1])[:5]
    counter = {} # {chave: valor}

    # percorre a lista ordenada para contar a quantidade de classes.
    for i in common_sorted:
        # Se a classe existir no contador, conta +1 para a classe, senão adiciona com o valor 1
        if i[0] in counter:
            counter[i[0]] += 1
        else:
            counter[i[0]] = 1

    # Variáveis para controlar qual é a classe com mais vizinhos
    qtd, bigger = 0, ""

    # Percorre o contador
    for i in counter:
        # Se o contador da classe for maior que a última, atribui às variáveis os valores da classe.
        if counter[i] > qtd:
            qtd, bigger = counter[i], i

    return bigger

print(k_nearest_neighbors(data=dataset, predict=new_feature))
