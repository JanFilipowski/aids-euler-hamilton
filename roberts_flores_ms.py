from representation import macierz_sasiedztwa
with open(input("Plik: "), "r") as f:
        plik = f.readlines()

m=macierz_sasiedztwa(plik)
liczba_odwiedzonych = 0
cykl = [0 for _ in range(len(m[0]))]
cykl[0]=1
odwiedzone = [0 for _ in range(len(m[0]))]
k=1

def hamilton_macierz_sasiedztwa(macierz,wierzcholek=1): 
    global liczba_odwiedzonych, cykl, odwiedzone, k
    odwiedzone[wierzcholek-1] = 1
    liczba_odwiedzonych+=1
    for i in range(1,len(macierz)+1):
        if macierz[wierzcholek-1][i-1] == 1:
            if i == 1 and liczba_odwiedzonych == len(macierz):
                cykl.append(1)
                return True
            if odwiedzone[i-1] == 0:
                if hamilton_macierz_sasiedztwa(macierz, i):
                    cykl[k]=i
                    k+=1
                    return True
    odwiedzone[wierzcholek-1] = 0
    liczba_odwiedzonych-=1
    return False


if hamilton_macierz_sasiedztwa(macierz_sasiedztwa(plik)) : print(cykl)
else : print("graf acykliczny")
            
 


