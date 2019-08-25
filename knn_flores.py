import random, time
import matplotlib.pyplot as plt
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D

start_time = time.time()


class Flor:
    """
    01 Bug:.........alta, poucas pétalas
    02 Exception:...baixa, muitas pétalas
    03 Loop:........baixa, poucas pétalas
    04 Call:........alta, muitas pétalas
    05 Kernel:......nem muito alta nem muito baixa, nem poucas nem muitas pétalas
    """

    def __init__(self, altura, petalas, raio_petala, classe=""):
        self.altura = altura
        self.petalas = petalas
        self.classe = classe
        self.raio_petala = raio_petala


class PontoDistancia:

    def __init__(self, distancia, flor):
        self.classe = flor.classe
        self.distancia = sqrt(distancia)
        self.altura = flor.altura
        self.petalas = flor.petalas
        self.raio_petala = flor.raio_petala


class KNearestNeighbor:

    flores = {'Bug': [], 'Exception': [], 'Loop': [], 'Call': [], 'Kernel': []}
    flor_teste = Flor

    def __init__(self, metodo="c"):
        self.gera_flores()

        self.metodo = metodo

        if metodo == "c":
            self.flor_teste.raio_petala = round(random.uniform(1.0, 5.0), 2)
        self.flor_teste.altura = round(random.uniform(1.0, 15.0), 2)
        self.flor_teste.petalas = random.randint(1, 10)
        self.flor_teste.classe = "Teste"

        print("Flor teste:")
        print("\tpetalas:", self.flor_teste.petalas)
        print("\taltura:", self.flor_teste.altura)
        if metodo == "c":
            print("\traio das pétalas:", self.flor_teste.raio_petala)

        if metodo == "c":
            self.dataset_3d()
        else:
            self.grafico_flores()

    def escolhe_flor(self, especie):

        if especie == "Bug":
            return (round(random.uniform(7.5, 15.0), 2),
                    random.randint(1, 5),
                    round(random.uniform(6.0, 9.0), 2))
        elif especie == "Exception":
            return (round(random.uniform(1.0, 7.5), 2),
                    random.randint(5, 10),
                    round(random.uniform(3.0, 6.0), 2))
        elif especie == "Loop":
            return (round(random.uniform(1.0, 7.5), 2),
                    random.randint(1, 5),
                    round(random.uniform(3.0, 6.0), 2))
        elif especie == "Call":
            return (round(random.uniform(7.5, 15.0), 2),
                    random.randint(5, 10),
                    round(random.uniform(6.0, 9.0), 2))
        elif especie == "Kernel":
            return (round(random.uniform(5.0, 10.0), 2),
                    random.randint(4, 7),
                    round(random.uniform(5.0, 7.0), 2))

    def gera_flores(self):
        for flor in self.flores:
            for i in range(0, random.randint(28, 40)):
                altura, petala, raio_petala = self.escolhe_flor(flor)
                self.flores[flor].append(Flor(altura=altura, petalas=petala, classe=flor, raio_petala=raio_petala))

    def mostra_flores(self):
        for flor in self.flores:
            print("Flor", flor)
            print("Instancias", len(self.flores[flor]))
            for i in self.flores[flor]:
                print('\t', i.classe)
                print('\t', i.altura)
                print('\t', i.petalas)
            print('\n\n')

    def mostra_flores_estatistica(self):
        contador = {}
        total_flores = 0

        for i in self.flores:
            contador[i] = [len(self.flores[i])]
            total_flores += len(self.flores[i])

        for i in contador:
            porcentagem = contador[i][0] * 100 / total_flores
            contador[i].append(round(porcentagem, 2))

        print("Dataset:", contador)

    def grafico_flores(self):
        cores = ['r', 'darkblue', 'darkgreen', 'gold', 'black']
        counter = 0
        for i in self.flores:
            cor = cores[counter]
            counter += 1
            x, y = [], []
            for j in self.flores[i]:
                x.append(j.petalas)
                y.append(j.altura)
            plt.scatter(x, y, color=cor, marker="o", s=20, label=i)

        plt.scatter(self.flor_teste.petalas, self.flor_teste.altura, color="deeppink", marker="o", s=200)
        plt.xlabel("Pétalas")
        plt.ylabel("Altura")
        plt.legend()
        plt.show()

    def dataset_3d(self):

        cores = ['r', 'darkblue', 'darkgreen', 'gold', 'black']
        counter = 0

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        t_altura = []
        t_petalas = []
        t_raio_petala = []

        for especie in self.flores:
            t_altura.clear()
            t_petalas.clear()
            t_raio_petala.clear()
            for flor in self.flores[especie]:
                t_altura.append(flor.altura)
                t_petalas.append(flor.petalas)
                t_raio_petala.append(flor.raio_petala)

            ax.scatter(t_petalas, t_altura, t_raio_petala, marker="o", color=cores[counter], label=especie)
            counter += 1

        if self.metodo == "c":
            ax.scatter(self.flor_teste.petalas, self.flor_teste.altura, self.flor_teste.raio_petala, marker="o",
                       color="deeppink", label="Teste", s=200)

        ax.set_xlabel('Pétalas')
        ax.set_ylabel('Altura')
        ax.set_zlabel('Raio petala')
        ax.legend()
        plt.show()

    def distancia_euclidiana(self, flor):
        distancia = (flor.altura - self.flor_teste.altura) ** 2 +\
                    (flor.petalas - self.flor_teste.petalas) ** 2

        if self.metodo == "c":
            distancia += (flor.raio_petala - self.flor_teste.raio_petala) ** 2

        return PontoDistancia(distancia=distancia, flor=flor)

    def knn_classificacao(self, classes):
        contador = {}
        quantidade, classe = 0, 0

        for i in classes:
            if i.classe in contador:
                contador[i.classe] += 1
            else:
                contador[i.classe] = 1

        print('contador:', contador)

        for item in contador:
            if contador[item] > quantidade:
                quantidade = contador[item]
                classe = item

        return classe, quantidade

    def knn_regressao(self, flores):
        soma = 0
        print("Raios das pétalas vizinhas:", [flor.raio_petala for flor in flores])
        for flor in flores:
            soma += flor.raio_petala

        return round(soma / len(flores), 2)

    def k_nearest_neighbor(self, k=5):
        distancias = []

        for especie in self.flores:
            for flor in self.flores[especie]:
                distancias.append(self.distancia_euclidiana(flor))

        self.grafico_flores()

        distancias = sorted(distancias, key=lambda distancias: distancias.distancia)[:k]
        print("classe, distancia, altura, qtd petalas, raio petalas\n",
              [(d.classe, d.distancia, d.altura, d.petalas, d.raio_petala) for d in distancias])

        t_altura = [d.altura for d in distancias]
        t_petalas = [d.petalas for d in distancias]
        t_raio_petala = [d.raio_petala for d in distancias]


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(t_petalas, t_altura, t_raio_petala, marker="o")

        if self.metodo == "c":
            ax.scatter(self.flor_teste.petalas, self.flor_teste.altura, self.flor_teste.raio_petala, marker="o",
                       color="deeppink", s=200)

        ax.set_xlabel('Pétalas')
        ax.set_ylabel('Altura')
        ax.set_zlabel('Raio petala')
        ax.legend()
        plt.show()

        if self.metodo == "c":
            classificacao = self.knn_classificacao([classes for classes in distancias])
            print("Classificação:", classificacao)
        elif self.metodo == "r":
            raio_petala = self.knn_regressao([flores for flores in distancias])
            self.flor_teste.raio_petala = raio_petala
            print("Regressão de raio de petala:", raio_petala)


knn = KNearestNeighbor(metodo="r")
# print("--- %s  seconds ---" % (time.time() - start_time))
knn.mostra_flores_estatistica()
knn.k_nearest_neighbor()
knn.grafico_flores()
