def lista_nastepnikow(f):
    nastepniki = {}

    for k, line in enumerate(f):
        if k == 0:
            for i in range(int(line.split()[0])):
                nastepniki[i + 1] = []
            continue
        l = tuple(map(int, line.split()))
        if l[0] != l[1]: nastepniki[l[0]] += [l[1]]

    # usuwanie cykli
    for keys in nastepniki:
        for n in nastepniki[keys]:
            if keys in nastepniki[n]:
                nastepniki[keys].remove(n)
                nastepniki[n].remove(keys)

    return nastepniki


def lista_poprzednikow(f):
    poprzedniki = {}

    for k, line in enumerate(f):
        if k == 0:
            for i in range(int(line.split()[0])):
                poprzedniki[i + 1] = []
            continue
        l = tuple(map(int, line.split()))
        if l[0] != l[1]: poprzedniki[l[1]] += [l[0]]

    # usuwanie cykli
    for keys in poprzedniki:
        for n in poprzedniki[keys]:
            if keys in poprzedniki[n]:
                poprzedniki[keys].remove(n)
                poprzedniki[n].remove(keys)

    return poprzedniki


def lista_braku_incydencji(f):
    nie_incydentni = {}

    for k, line in enumerate(f):
        if k == 0:
            wszystkie_wierzcholki = []
            for i in range(int(line.split()[0])):
                wszystkie_wierzcholki.append(i + 1)
            for i in range(int(line.split()[0])):
                nie_incydentni[i + 1] = wszystkie_wierzcholki.copy()
            continue
        l = tuple(map(int, line.split()))

        if l[1] in nie_incydentni[l[0]]: nie_incydentni[l[0]].remove(int(l[1]))
        if l[0] in nie_incydentni[l[1]]: nie_incydentni[l[1]].remove(int(l[0]))

    return nie_incydentni


def macierz_grafu(f):
    LN = lista_nastepnikow(f)
    LP = lista_poprzednikow(f)
    LB = lista_braku_incydencji(f)
    LC = {}

    dlugosc = int(f[0].split()[0])
    # tworzenie listy cykli
    for i in range(dlugosc):
        LC[i + 1] = []
    for i in range(1, dlugosc + 1):
        for j in range(1, dlugosc + 1):
            if j not in LN[i] and j not in LP[i] and j not in LB[i]: LC[i] += [j]

    macierz = [[0] * (dlugosc + 4) for _ in range(dlugosc)]

    for keys in LN:
        if LN[keys]:
            for i in LN[keys]:
                macierz[keys - 1][i - 1] = LN[keys][min(LN[keys].index(i) + 1, len(LN[keys]) - 1)]
            macierz[keys - 1][dlugosc] = LN[keys][0]

    for keys in LP:
        if LP[keys]:
            for i in LP[keys]:
                macierz[keys - 1][i - 1] = dlugosc + LP[keys][min(LP[keys].index(i) + 1, len(LP[keys]) - 1)]
            macierz[keys - 1][dlugosc + 1] = LP[keys][0]

    for keys in LB:
        if LB[keys]:
            for i in LB[keys]:
                macierz[keys - 1][i - 1] = -1 * LB[keys][min(LB[keys].index(i) + 1, len(LB[keys]) - 1)]
            macierz[keys - 1][dlugosc + 2] = LB[keys][0]

    for keys in LC:
        if LC[keys]:
            for i in LC[keys]:
                macierz[keys - 1][i - 1] = 2 * dlugosc + LC[keys][min(LC[keys].index(i) + 1, len(LC[keys]) - 1)]
            macierz[keys - 1][dlugosc + 3] = LC[keys][0]

    return macierz


def macierz_sasiedztwa(f):
    matrix = []
    for k, line in enumerate(f):
        if k == 0:
            N = int(line.split()[0])
            matrix = [[0] * N for _ in range(N)]
            continue
        l = tuple(map(int, line.split()))

        matrix[l[0]-1][l[1]-1] = 1
        matrix[l[1]-1][l[0]-1] = 1

    return matrix


if __name__ == "__main__":

    def print2d(m):
        for i in m:
            for j in i:
                print(j, end="\t")
            print()


    with open(input("Plik: "), "r") as f:
        plik = f.readlines()

    print(lista_nastepnikow(plik))
    # print2d(macierz_sasiedztwa(plik))
    print(lista_poprzednikow(plik))
    print(lista_braku_incydencji(plik))
    m = macierz_grafu(plik)
    print2d(m)
    m = macierz_sasiedztwa(plik)
    print2d(m)
