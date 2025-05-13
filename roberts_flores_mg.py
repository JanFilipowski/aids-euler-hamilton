from representation import macierz_grafu

def roberts_flores_ahg(matrix):
    n = len(matrix)
    visited = [False] * n
    Path = [0] * (n+1)
    start = 0
    count = 0

    def Hamiltonian(v, depth):
        nonlocal count
        visited[v] = True
        count += 1

        first = matrix[v][n+1]-1 if matrix[v][n+1] != 0 else 0
        order = [first] + [i for i in range(n) if i != first and i != v]


        for i in order:
            if 0 <= matrix[v][i] <= n or 2*n+1 <= matrix[v][i] <= 3*n:
                if i == start and count == n:
                    Path[depth] = v
                    Path[depth+1] = i
                    return True
                    
                if not visited[i]:
                    if Hamiltonian(i, depth + 1):
                        Path[depth] = v
                        return True

        visited[v] = False
        count -= 1
        return False

    for i in range(n):
        visited[i] = False
    Path[0] = start

    if Hamiltonian(start, 0):
        return [x + 1 for x in Path]
    else:
        return None

if __name__ == '__main__':
    with open(input("Plik: "), "r") as f:
        plik = f.readlines()

    m = macierz_grafu(plik)
    print(roberts_flores_ahg(m))