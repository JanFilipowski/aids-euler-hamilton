import csv
import os
import random
import time
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

def lista_nastepnikow(f):
    nastepniki = {}
    for k, line in enumerate(f):
        if k == 0:
            for i in range(int(line.split()[0])):
                nastepniki[i + 1] = []
            continue
        l = tuple(map(int, line.split()))
        if l[0] != l[1]:
            nastepniki[l[0]] += [l[1]]
    for keys in nastepniki:
        for n in list(nastepniki[keys]):
            if keys in nastepniki.get(n, []):
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
        if l[0] != l[1]:
            poprzedniki[l[1]] += [l[0]]
    for keys in poprzedniki:
        for n in list(poprzedniki[keys]):
            if keys in poprzedniki.get(n, []):
                poprzedniki[keys].remove(n)
                poprzedniki[n].remove(keys)
    return poprzedniki

def lista_braku_incydencji(f):
    nie_incydentni = {}
    for k, line in enumerate(f):
        if k == 0:
            wszystkie = list(range(1, int(line.split()[0]) + 1))
            for i in wszystkie:
                nie_incydentni[i] = wszystkie.copy()
            continue
        l = tuple(map(int, line.split()))
        if l[1] in nie_incydentni[l[0]]:
            nie_incydentni[l[0]].remove(l[1])
        if l[0] in nie_incydentni[l[1]]:
            nie_incydentni[l[1]].remove(l[0])
    return nie_incydentni

def macierz_grafu(f):
    LN = lista_nastepnikow(f)
    LP = lista_poprzednikow(f)
    LB = lista_braku_incydencji(f)
    LC = {}
    n = int(f[0].split()[0])
    for i in range(1, n+1):
        LC[i] = []
    for i in range(1, n+1):
        for j in range(1, n+1):
            if j not in LN[i] and j not in LP[i] and j not in LB[i]:
                LC[i] += [j]
    M = [[0] * (n + 4) for _ in range(n)]
    for keys in LN:
        if LN[keys]:
            for i in LN[keys]:
                idx = LN[keys].index(i)
                nxt = LN[keys][min(idx+1, len(LN[keys])-1)]
                M[keys-1][i-1] = nxt
            M[keys-1][n] = LN[keys][0]
    for keys in LP:
        if LP[keys]:
            for i in LP[keys]:
                idx = LP[keys].index(i)
                nxt = LP[keys][min(idx+1, len(LP[keys])-1)]
                M[keys-1][i-1] = n + nxt
            M[keys-1][n+1] = LP[keys][0]
    for keys in LB:
        if LB[keys]:
            for i in LB[keys]:
                idx = LB[keys].index(i)
                nxt = LB[keys][min(idx+1, len(LB[keys])-1)]
                M[keys-1][i-1] = -nxt
            M[keys-1][n+2] = LB[keys][0]
    for keys in LC:
        if LC[keys]:
            for i in LC[keys]:
                idx = LC[keys].index(i)
                nxt = LC[keys][min(idx+1, len(LC[keys])-1)]
                M[keys-1][i-1] = 2*n + nxt
            M[keys-1][n+3] = LC[keys][0]
    return M

def macierz_sasiedztwa(f):
    for k, line in enumerate(f):
        if k == 0:
            N = int(line.split()[0])
            M = [[0]*N for _ in range(N)]
            continue
        u, v = map(int, line.split())
        M[u-1][v-1] = 1
        M[v-1][u-1] = 1
    return M

# --- Hamiltonian Algorithms ---

def roberts_flores_ahg(matrix):
    n = len(matrix)
    visited = [False]*n
    Path = [0]*(n+1)
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
                    if Hamiltonian(i, depth+1):
                        Path[depth] = v
                        return True
        visited[v] = False
        count -= 1
        return False
    Path[0] = start
    if Hamiltonian(start, 0):
        return [x+1 for x in Path]
    else:
        return None

# Undirected Hamilton
liczba_odwiedzonych = 0
cykl_h = []
odwiedzone = []
k_var = 1

def hamilton_macierz_sasiedztwa(mat, w=1):
    global liczba_odwiedzonych, cykl_h, odwiedzone, k_var
    if not odwiedzone:
        odwiedzone = [0]*len(mat)
    odwiedzone[w-1] = 1
    liczba_odwiedzonych += 1
    for i in range(1, len(mat)+1):
        if mat[w-1][i-1] == 1:
            if i == 1 and liczba_odwiedzonych == len(mat):
                cykl_h.append(1)
                return True
            if odwiedzone[i-1] == 0:
                if hamilton_macierz_sasiedztwa(mat, i):
                    cykl_h.append(i)
                    return True
    odwiedzone[w-1] = 0
    liczba_odwiedzonych -= 1
    return False

# --- Eulerian Algorithms ---

# Directed Euler
def dfs_dir(u, visited, M):
    visited[u-1] = True
    for v in range(len(M[0]) - 4):
        if M[u-1][v] > 0 and not visited[v]:
            dfs_dir(v+1, visited, M)

def czy_most(u, v, M):
    n = len(M[0]) - 4
    visited_before = [False]*n
    dfs_dir(u, visited_before, M)
    temp = M[u-1][v-1]
    M[u-1][v-1] = 0
    M[v-1][u-1] = 0
    visited_after = [False]*n
    dfs_dir(u, visited_after, M)
    M[u-1][v-1] = temp
    M[v-1][u-1] = temp
    return visited_before != visited_after

def euler_macierz_grafu(start, M):
    cycle = []
    def recurse(u):
        nonlocal cycle
        cycle.append(u)
        next_bridge = None
        for i in range(len(M[0]) - 4):
            if (M[u-1][i] > 0 and M[u-1][i] <= len(M)) or M[u-1][i] > 2*len(M):
                if czy_most(u, i+1, deepcopy(M)):
                    next_bridge = i+1
                    continue
                M[u-1][i] = 0
                recurse(i+1)
                return
        if next_bridge:
            M[u-1][next_bridge-1] = 0
            recurse(next_bridge)
    recurse(start)
    return cycle

# Undirected Euler without check
def euler_undirected(mat):
    M = deepcopy(mat)
    N = len(M)
    def count_reachable(m, u):
        seen = set()
        def dfs(x):
            for y in range(N):
                if m[x][y] > 0 and y not in seen:
                    seen.add(y)
                    dfs(y)
        seen.add(u)
        dfs(u)
        return len(seen)
    u = next((i for i in range(N) if sum(M[i])>0), 0)
    cycle = [u+1]
    total_edges = sum(sum(row) for row in M)//2
    for _ in range(total_edges):
        for v in range(N):
            if M[u][v] > 0:
                M[u][v] -= 1
                M[v][u] -= 1
                ra = count_reachable(M, u)
                M[u][v] += 1
                M[v][u] += 1
                if ra == count_reachable(M, u) or sum(M[u]) == 1:
                    M[u][v] -= 1
                    M[v][u] -= 1
                    u = v
                    cycle.append(u+1)
                    break
    return cycle

# --- Generators ---

def gen_directed_ham(n, s):
    total = n*(n-1)
    E = max(round(s/100*total), n)
    perm = list(range(1, n+1))
    random.shuffle(perm)
    edges = [(i, perm[i-1]) for i in range(1, n+1)]
    extra = E - n
    while extra>0:
        u,v = random.sample(range(1, n+1), 2)
        edges.append((u,v))
        extra-=1
    return edges

def gen_directed_rand(n, s):
    total = n*(n-1)
    E = int(s/100*total)
    pairs = [(u,v) for u in range(1,n+1) for v in range(1,n+1) if u!=v]
    return random.sample(pairs, min(E,len(pairs)))

def gen_directed_eul(n, s):
    total = n*(n-1)
    E = max(round(s/100*total), n)
    perm = list(range(1, n+1))
    random.shuffle(perm)
    edges = [(i, perm[i-1]) for i in range(1, n+1)]
    extra = E - n
    while extra>1:
        u,v = random.sample(range(1,n+1),2)
        edges.extend([(u,v),(v,u)])
        extra-=2
    if extra==1:
        u,v = random.sample(range(1,n+1),2)
        edges.append((u,v))
    return edges

def gen_undirected_ham(n, s):
    total = n*(n-1)//2
    E = max(round(s/100*total), n)
    edges = [(i, i+1) for i in range(1,n)]
    edges.append((n,1))
    extra = E - n
    possible = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1) if (u,v) not in edges]
    random.shuffle(possible)
    edges.extend(possible[:extra])
    return edges

def gen_undirected_rand(n, s):
    total = n*(n-1)//2
    E = int(s/100*total)
    pairs = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1)]
    return random.sample(pairs, min(E,len(pairs)))

def gen_undirected_eul(n, s):
    total = n*(n-1)//2
    E = max(round(s/100*total), n)
    edges = [(i, i+1) for i in range(1,n)]
    edges.append((n,1))
    extra = E - n
    possible = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1) if (u,v) not in edges]
    random.shuffle(possible)
    idx=0
    while extra>1 and idx<len(possible)-1:
        edges.extend([possible[idx], possible[idx+1]])
        idx+=2; extra-=2
    return edges

# --- Measurement Wrappers ---

def measure_ham_dir(matrix):
    start = time.perf_counter(); _ = roberts_flores_ahg(matrix); return time.perf_counter()-start

def measure_ham_und(matrix):
    global liczba_odwiedzonych, cykl_h, odwiedzone, k_var
    liczba_odwiedzonych = 0; cykl_h = []; odwiedzone = []; k_var = 1
    start = time.perf_counter(); _ = hamilton_macierz_sasiedztwa(matrix); return time.perf_counter()-start

def measure_eul_dir(matrix):
    start = time.perf_counter(); _ = euler_macierz_grafu(1, matrix); return time.perf_counter()-start

def measure_eul_und(matrix):
    start = time.perf_counter(); _ = euler_undirected(matrix); return time.perf_counter()-start

# --- Experiment Setup ---
# --- Parametry eksperymentu ---
nodes       = list(range(10, 151, 10))        # wartości n: 10,20,...,150
saturations = [10,20,30,40,50,60,70,80,90]     # wartości s%

csv_path = 'measurements.csv'
# Usuń plik, jeśli istnieje, i napisz nagłówek
if os.path.exists(csv_path):
    os.remove(csv_path)
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['graph','algorithm','cyclic','n','s','time'])

# --- Definicja kombinacji do wykonania ---
jobs = []
for n in nodes:
    for s in saturations:
        # AHG: directed Hamiltonian (cyclic/acyclic)
        jobs.append(("directed","AHG", True,  n, s))
        jobs.append(("directed","AHG", False, n, s))
        # AEG: directed Euler (cyclic/acyclic)
        jobs.append(("directed","AEG", True,  n, s))
        jobs.append(("directed","AEG", False, n, s))
        # AHS: undirected Hamiltonian
        jobs.append(("undirected","AHS", True,  n, s))
        jobs.append(("undirected","AHS", False, n, s))
        # AES: undirected Euler
        jobs.append(("undirected","AES", True,  n, s))
        jobs.append(("undirected","AES", False, n, s))

# --- Worker wykonujący pojedyncze zadanie ---
def run_job(job):
    graph, alg, cyclic, n, s = job

    # 1) wygeneruj krawędzie wg typu
    if graph=="directed":
        if   alg=="AHG": edges = gen_directed_ham(n,s)   if cyclic else gen_directed_rand(n,s)
        elif alg=="AEG": edges = gen_directed_eul(n,s)   if cyclic else gen_directed_rand(n,s)
    else:
        if   alg=="AHS": edges = gen_undirected_ham(n,s) if cyclic else gen_undirected_rand(n,s)
        elif alg=="AES": edges = gen_undirected_eul(n,s) if cyclic else gen_undirected_rand(n,s)

    # 2) stwórz odpowiednią macierz
    lines = [f"{n}\n"] + [f"{u} {v}\n" for u,v in edges]
    if graph=="directed":
        M = macierz_grafu(lines)
    else:
        M = macierz_sasiedztwa(lines)

    # 3) zmierz czas
    start = time.perf_counter()
    if   graph=="directed" and alg=="AHG": _ = roberts_flores_ahg(M)
    elif graph=="directed" and alg=="AEG": _ = euler_macierz_grafu(1, M)
    elif graph=="undirected" and alg=="AHS": 
        global liczba_odwiedzonych, cykl_h, odwiedzone
        liczba_odwiedzonych=0; cykl_h=[]; odwiedzone=[]
        _ = hamilton_macierz_sasiedztwa(M)
    elif graph=="undirected" and alg=="AES": _ = euler_undirected(M)
    elapsed = time.perf_counter() - start

    return [graph, alg, cyclic, n, s, elapsed]

# --- Uruchamiamy wątkowo ze wsparciem tqdm ---
max_workers = os.cpu_count() or 4
with ThreadPoolExecutor(max_workers=max_workers) as pool:
    futures = [pool.submit(run_job, job) for job in jobs]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Eksperymenty"):
        result = future.result()
        # zapisujemy od razu do CSV
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result)

print("Gotowe! Wyniki w:", csv_path)
