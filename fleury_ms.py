from representation import macierz_sasiedztwa

def is_eulerian(mat):
    N = len(mat)

    degrees = [sum(mat[i]) for i in range(N)]

    for deg in degrees:
        if deg % 2 != 0:
            return False

    start = -1
    for i, deg in enumerate(degrees):
        if deg > 0:
            start = i
            break

    if start == -1:
        return True

    visited = set()
    def dfs(u):
        for v in range(N):
            if mat[u][v] > 0 and v not in visited:
                visited.add(v)
                dfs(v)

    visited.add(start)
    dfs(start)

    for i, deg in enumerate(degrees):
        if deg > 0 and i not in visited:
            return False
    return True



def eulerian_cycle(matrix):
    
    if not is_eulerian(matrix):
        return None
    N = len(matrix)
    
    
    def count_reachable(mat, u):
        seen = set()
        def dfs_count(x):
            for y in range(N):
                if mat[x][y] > 0 and y not in seen:
                    seen.add(y)
                    dfs_count(y)
        seen.add(u)
        dfs_count(u)
        return len(seen)


    u = 0
    for i in range(N):
        if sum(matrix[i]) > 0:
            u = i
            break
    path = [u]
    
    total_edges = sum(sum(row) for row in matrix) // 2

    for _ in range(total_edges):
        for v in range(N):
            if matrix[u][v] > 0:
                
                matrix[u][v] -= 1
                matrix[v][u] -= 1
                
                reachable_after = count_reachable(matrix, u)
                
                matrix[u][v] += 1
                matrix[v][u] += 1
                
                if reachable_after == count_reachable(matrix, u) or sum(matrix[u]) == 1:
                    
                    matrix[u][v] -= 1
                    matrix[v][u] -= 1
                    u = v
                    path.append(u)
                    break
                    
    return [x + 1 for x in path]


if __name__ == '__main__':
    filename = input("Plik: ")
    with open(filename, "r") as f:
        lines = f.readlines()

    m = macierz_sasiedztwa(lines)
    cycle = eulerian_cycle(m)
    if cycle is None:
        print("Graf nie jest eulerowski")
    else:
        print(cycle)
