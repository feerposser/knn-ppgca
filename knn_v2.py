"""
1 - Espessura de Clump
2 - Uniformidade do tamanho das células
3 - Uniformidade do formato das células
4 - Adesão marginal
5 - Tamanho único das células epiteliais
6 - Núcleos nús
7 - Cromatina suave
8 - Nucleoli Normal
9 - Mitoses
::::::::::::::::::::::::::::::::::::::::: 10 - Classe (2: benigno, 4: maligno)
"""
import time
import csv
from math import sqrt

start_time = time.time()
classificar = [3, 3, 6, 3, 8, 9, 1, 1, 2]


def conta_malignos_benignos(lista_cancer):
    conta_maligno, conta_benigno = 0, 0
    for cancer in lista_cancer:
        if cancer.classe == "Maligno":
            conta_maligno += 1
        else:
            conta_benigno += 1

    return conta_maligno, conta_benigno


def porcentagens_malignos_benignos(lista_cancer):
    malignos, benignos = conta_malignos_benignos(lista_cancer)
    soma = malignos + benignos
    malignos = malignos * 100 / soma
    benignos = benignos * 100 / soma

    return "Malignos: %.2f\nBenignos: %.2f" % (malignos, benignos)


class Cancer:
    """
    
    """

    def __init__(self, dados):
        self.dados = []

        # Para todos os índices da linha, com exceção do último(classe), faz casting para inteiro e insere em uma lista
        for i in dados[:-1]:
            self.dados.append(int(i))

        # Com o último índice(classe) usa a função tipo_classe que retorna por extenso o tipo de cancer.
        self.classe = self.tipo_classe(dados[-1:][0])

    def tipo_classe(self, classe):
        if int(classe) == 2:
            return "Benigno"

        return "Maligno"


class PontoDistancia:
    """
    Implementa os dados de distância.
    No atributo 'distancia' finaliza a fórmula aplicando a raiz quadrada.
    """

    def __init__(self, cancer, distancia):
        self.classe = cancer.classe
        self.distancia = sqrt(distancia)
        self.dados = cancer.dados


def distancia_euclidica(cancer):
    """
    Calcula a distância euclídica
    :param cancer: objeto do tipo Cancer
    :return: Objeto do tipo PontoDistancia(classe, distancia, dados)
    """
    soma = 0
    for i in range(0, 9):
        soma += (cancer.dados[i] - classificar[i]) ** 2

    return PontoDistancia(cancer, soma)


def k_classificacao(distancias):
    """
    Realiza a classificação através dos vizinhos mais comuns
    :param distancias: Lista de classes.
    :return: tupla com o número de ocorrências e o nome da classe.
    """
    # classificador = {}
    # maior_numero, maior_classe = 0, ""

    if distancias.count("Maligno") >= distancias.count("Benigno"):
        return distancias.count("Maligno"), "Maligno"
    else:
        return distancias.count("Benigno"), "Benigno"

    # for i in distancias:
    #     if i in classificador:
    #         classificador[i] += 1
    #     else:
    #         classificador[i] = 1
    #
    # for i in classificador:
    #     if classificador[i] > maior_numero:
    #         maior_numero, maior_classe = classificador[i], i

    # return maior_numero, maior_classe


def k_regressao(distancias):
    predicao = [1, 2, 3, 4, 5, 6, 7, 8, "?", 4]
    index_predicao = predicao.index("?")
    # print("index:", index_predicao)
    soma = 0
    for i in range(0, len(distancias)):
        soma += distancias[i][index_predicao]

    return soma//len(distancias)


def k_nearest_neighbor(lista_cancer, metodo="c", k=5):
    """
    Realiza o algoritmo
    :param lista_cancer: lista com elementos do tipo Cancer
    :param metodo: c = classificação, r = regressão
    :param k: número de vizinhos
    :return: resultado da classificação ou da regressão
    """

    distancias = []  # Lista para armazenar os objetos do tipo PontoDistancia
    for cancer in lista_cancer:
        # Para cada item da lista, encontra a distância euclídica e armazena o resultado que está no Obj PontoDistancia
        # na lista. PontoDistancia(classe="", distancia=0.0, classe="")
        distancias.append(distancia_euclidica(cancer))

    # Ordena a lista distancias a partir do atributo distancia dos objetos e recupera apenas os primeiros k valores.
    distancias = sorted(distancias, key=lambda distancias: distancias.distancia)[:k]

    # print([classes.dados for classes in distancias])

    if metodo == "c":
        return k_classificacao([classes.classe for classes in distancias])
    elif metodo == "r":
        return k_regressao([classes.dados for classes in distancias])

# Lê o arquivo csv
arquivo = csv.reader(open('breast-cancer-wisconsin_final.csv'), delimiter=';')

lista_cancer = []

# Para cada linha do arquivo de dataset
for linha in arquivo:
    # Armazena um objeto do tipo Cancer na lista
    lista_cancer.append(Cancer(linha))

print(porcentagens_malignos_benignos(lista_cancer))

print(k_nearest_neighbor(lista_cancer, metodo="c"))
print("--- %s  seconds ---" % (time.time() - start_time))