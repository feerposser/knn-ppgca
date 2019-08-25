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
from random import randint

start_time = time.time()


class Cancer:

    def __init__(self, dados):
        self.dados = []

        for i in dados[:-1]:
            self.dados.append(int(i))

        self.classe = self.tipo_classe(dados[-1:][0])

    @staticmethod
    def tipo_classe(classe):
        if int(classe) == 2:
            return "Benigno"

        return "Maligno"


class PontoDistancia:

    def __init__(self, cancer, distancia):
        self.classe = cancer.classe
        self.distancia = sqrt(distancia)
        self.dados = cancer.dados


class KNearestNeighbor:

    def __init__(self, lista_cancer):
        self.valores = lista_cancer

    def k_nearest_neighbor(self, k, instancia, metodo="c"):
        distancias = []

        for i in self.valores:
            distancias.append(self.distancia_euclidiana(instancia=instancia, ponto=i))

        distancias = sorted(distancias, key=lambda distancias: distancias.distancia)[:k]

        if metodo == "c":
            return self.k_classificacao([classes.classe for classes in distancias])
        elif metodo == "r":
            return self.k_regressao([classes.dados for classes in distancias])

    @staticmethod
    def distancia_euclidiana(instancia, ponto):
        soma = 0
        for i in range(0, len(instancia)):
            soma += (ponto.dados[i] - instancia[i]) ** 2

        return PontoDistancia(ponto, soma)

    @staticmethod
    def k_regressao(distancias):
        predicao = [1, 2, 3, 4, 5, 6, 7, 8, "?", 4]
        index_predicao = predicao.index("?")
        soma = 0
        for i in range(0, len(distancias)):
            soma += distancias[i][index_predicao]

        return soma // len(distancias)

    @staticmethod
    def k_classificacao(distancias):
        if distancias.count("Maligno") >= distancias.count("Benigno"):
            return distancias.count("Maligno"), "Maligno"
        # elif distancias.count("Maligno") >= distancias.count("Benigno"):
        #     print("eitaaaaaa poooooorraaa")
        #     import time
        #     time.sleep(10000000)
        else:
            return distancias.count("Benigno"), "Benigno"


class ValidacaoCruzada:
    k_validacao = {}
    lista_cancer = []

    def __init__(self):
        arquivo = csv.reader(open('breast-cancer-wisconsin_final.csv'), delimiter=';')
        self.limpa_k_validacao()

        for linha in arquivo:
            self.lista_cancer.append(Cancer(linha))

    def limpa_k_validacao(self):
        self.k_validacao = {"Malignos": {}, "Benignos": {}}

    def separa_para_validacao(self, porcent_malignos=30, porcent_benignos=30):
        total_malignos, total_benignos = self.conta_malignos_benignos()
        malignos, benignos = [], []
        validacao_malignos, validacao_benignos = [], []

        for cancer in self.lista_cancer:
            if cancer.classe == "Maligno":
                malignos.append(cancer)
            else:
                benignos.append(cancer)

        for i in range(0, total_malignos * porcent_malignos // 100):
            validacao_malignos.append(malignos.pop(randint(0, len(malignos)-1)))

        for i in range(0, total_benignos * porcent_benignos // 100):
            validacao_benignos.append(benignos.pop(randint(0, len(benignos)-1)))

        return validacao_malignos, validacao_benignos

    # @staticmethod
    def melhor_resultado(self):
        print("Malignos")
        for k in self.k_validacao["Malignos"]:
            print("%s: \n\tAcertos: %s\n\tErros: %s" % (k, self.k_validacao["Malignos"][k]["Acertos"],
                                                        self.k_validacao["Malignos"][k]["Erros"]))

        print("\n\nBenignos")
        for k in self.k_validacao["Benignos"]:
            print("%s: \n\tAcertos: %s\n\tErros: %s" % (k, self.k_validacao["Benignos"][k]["Acertos"],
                                                        self.k_validacao["Benignos"][k]["Erros"]))

    def validacao_cruzada(self):
        validacao_malignos, validacao_benignos = self.separa_para_validacao()
        knn = KNearestNeighbor(self.lista_cancer)
        self.limpa_k_validacao()
        k = 3
        tamanho_maximo_k = len(self.lista_cancer) // 3

        try:
            if len(self.lista_cancer) > 5:

                while True:
                    if k >= tamanho_maximo_k:
                        print("K:", k, "tamanho máximo de k:", tamanho_maximo_k)
                        break

                    if k not in self.k_validacao["Malignos"]:
                        self.k_validacao["Malignos"][k] = {"Acertos": 0, "Erros": 0}
                    if k not in self.k_validacao["Benignos"]:
                        self.k_validacao["Benignos"][k] = {"Acertos": 0, "Erros": 0}

                    for i in validacao_malignos:
                        # print("\n%s MALIGNOS" % k)
                        # print("\n\t", i.dados)
                        resultado = knn.k_nearest_neighbor(k=k, instancia=i.dados)
                        # print("\tOriginal:", i.classe, "\n\tResultado:", resultado)
                        if resultado[1] == i.classe:
                            # print("\tAcertou")
                            self.k_validacao["Malignos"][k]["Acertos"] += 1
                        else:
                            # print("\tErrou")
                            self.k_validacao["Malignos"][k]["Erros"] += 1
                        # print("\tAcertos: %s \n\tErros: %s" % (self.k_validacao["Malignos"][k]["Acertos"],
                            # self.k_validacao["Malignos"][k]["Erros"]))

                    for i in validacao_benignos:
                        # print("\n%s BENIGNOS" % k)
                        # print("\t", i.dados)
                        resultado = knn.k_nearest_neighbor(k=k, instancia=i.dados)
                        # print("\tOriginal:", i.classe, "Resultado:", resultado)
                        if resultado[1] == i.classe:
                            # print("\tAcertou")
                            self.k_validacao["Benignos"][k]["Acertos"] += 1
                        else:
                            # print("\tErrou")
                            self.k_validacao["Benignos"][k]["Erros"] += 1
                        # print("\tAcertos: %s \n\tErros: %s" % (self.k_validacao["Malignos"][k]["Acertos"],
                            # self.k_validacao["Malignos"][k]["Erros"]))
                    k += 2

            else:
                raise Exception("Valores insuficientes. Mínimo: 5. Valores atuais:" + str(len(self.lista_cancer)))
        except Exception as e:
            print("Erro:", repr(e))
        finally:
            print("Fim")
            # self.melhor_resultado()
            # print("valor de k", k, "Melhores resultados", self.k_validacao)


    def conta_malignos_benignos(self):
        conta_maligno, conta_benigno = 0, 0
        for cancer in self.lista_cancer:
            if cancer.classe == "Maligno":
                conta_maligno += 1
            else:
                conta_benigno += 1

        print("Malignos:", conta_maligno)
        print("Benignos:", conta_benigno)

        return conta_maligno, conta_benigno

    def porcentagens_malignos_benignos(self):
        malignos, benignos = self.conta_malignos_benignos()
        soma = malignos + benignos
        malignos = malignos * 100 / soma
        benignos = benignos * 100 / soma

        return "Malignos: %.2f\nBenignos: %.2f" % (malignos, benignos)

validacao = ValidacaoCruzada()
print(validacao.porcentagens_malignos_benignos())
validacao.validacao_cruzada()

print("--- %s  seconds ---" % (time.time() - start_time))
