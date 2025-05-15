import sys
import copy
sys.setrecursionlimit(10**6)



def print2d(m):
    for i in m:
        for j in i:
            print(j, end="\t")
        print()

def czy_euler(macierz):
     
    n=len(macierz[0])-4
    for i in range(n):
        wej=0
        wyj=0
        for j in range(n):
                if macierz[i][j]>0 and macierz[i][j]<=n:
                    wyj+=1
                if macierz[i][j]>n and macierz[i][j]<=2*n:
                    wej+=1
        if wyj != wej : return False
    

    visited = [False]*n
    dfs(1,visited,macierz)
    if False in visited : return False
    return True
               
def dfs(u, visited, macierz):
    visited[u-1] = True
    
    for v in range(len(macierz[0])-4):
        if macierz[u-1][v] > 0 and not visited[v]:
            dfs(v+1, visited, macierz)

def czy_most(u, v, macierz):
    n = len(macierz[0])-4
    
    visited_before = [False] * n
    dfs(u, visited_before, macierz)
    count_before = sum(visited_before)
    
    temp = macierz[u-1][v-1]
    macierz[u-1][v-1] = 0
    temp2 = macierz[u-1][v-1]
    macierz[v-1][u-1] = 0
    
    visited_after = [False] * n
    dfs(u, visited_after, macierz)
    count_after = sum(visited_after)
    
    macierz[u-1][v-1] = temp
    macierz[v-1][u-1] = temp2

    print("Tempy: ", temp, temp2, macierz[u-1][v-1])

    if visited_after != visited_before : return True
    return False

def euler_macierz_grafu(wierzcholek):
    global macierz,cykl
    n=len(macierz[0])-4
    most=0
    for i in range(len(macierz[0])-4):
        print(macierz[i])
    print("wierzcholek : ",wierzcholek)
    print(cykl)
    cykl.append(wierzcholek)
    for i in range(n):
           if (macierz[wierzcholek-1][i] > 0 and macierz[wierzcholek - 1][i]<=n) or macierz[wierzcholek - 1][i]>2*n:
                 print2d(macierz)
                 if czy_most(wierzcholek,i+1,macierz):
                      print2d(macierz)
                      most = i+1
                      print("most = ",most)
                      continue
                 macierz[wierzcholek-1][i] =0
                 return euler_macierz_grafu(i+1)
    if most != 0 : 
        macierz[wierzcholek - 1][most-1]=0
        return euler_macierz_grafu(most)

    
                 

    
from representation import macierz_grafu
with open(input("Plik: "), "r") as f:
    plik = f.readlines()
macierz = macierz_grafu(plik)
cykl=[]

if czy_euler(macierz):
    euler_macierz_grafu(1)
    if cykl[0] != cykl[-1] : cykl.append(cykl[0])
    print(cykl)
else:
    print("graf nie jest eulerowski")






