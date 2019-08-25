
class T:
    v = ""

    def __init__(self, v):
        self.v = v

    def alterv(self, v):
        self.v += v

x = T('x')
y = T('y')

print(x.v)
print(y.v)

x.alterv('xx')
print(20*'--')
print(x.v)
print(y.v)

print(50*"==")

b = [1,2,3,4,5]
print(b[:-1])

print(100*'!')

for i in range(8, 10):
    print(i, end="")

print(50*"!!!")

testelista = ["a", "b"]
# testelista.remove("a")
print(testelista)

while testelista:
    print(testelista)
    testelista.pop(0)
testelista2 = []
for i in testelista2:
    print('....',testelista2)

print(20*"ordenar listas adjacentes")

class Teste:
    def __init__(self):
        self.adj = [["alto", 15], ['tijuca', 20], ['araras', 5]]

    def s(self, lista):
        return sorted(lista, key=lambda lista:lista[1])

    def gg(self):

        return self.s(self.adj)

blab = Teste()
print(blab.gg())