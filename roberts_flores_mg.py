from representation import macierz_grafu

def roberts_flores_ahg(matrix):
    """
    Szuka jednego cyklu Hamiltona w skierowanym multigrafie
    reprezentowanym macierzą grafu (AHG).
    Zwraca listę wierzchołków 1-based albo None.
    """
    n = len(matrix)
    visited = [False] * n
    Path = [0] * (n+1)
    start = 0
    count = 0

    def Hamiltonian(v, depth):
        nonlocal count
        visited[v] = True
        count += 1

        # Priorytetyzujemy sprawdzenie pierwszego następnika z macierzy grafu
        first = matrix[v][n+1]-1 if matrix[v][n+1] != 0 else 0
        order = [first] + [i for i in range(n) if i != first and i != v]


        for i in order:
            # w macierzy grafu krawędź v→i to wartość 1..n
            if 0 <= matrix[v][i] <= n or 2*n+1 <= matrix[v][i] <= 3*n:
                # jeśli wracamy do startu i odwiedziliśmy już wszystkie
                if i == start and count == n:
                    Path[depth] = v
                    Path[depth+1] = i
                    return True
                # jeśli nieodwiedzony, schodzimy w dół
                if not visited[i]:
                    if Hamiltonian(i, depth + 1):
                        Path[depth] = v
                        return True

        # cofamy stan
        visited[v] = False
        count -= 1
        return False

    # inicjalizacja
    for i in range(n):
        visited[i] = False
    Path[0] = start

    if Hamiltonian(start, 0):
        # przepisujemy na 1-based i zamykamy cykl
        return [x + 1 for x in Path]
    else:
        return None

if __name__ == '__main__':
    with open(input("Plik: "), "r") as f:
        plik = f.readlines()

    m = macierz_grafu(plik)
    print(roberts_flores_ahg(m))