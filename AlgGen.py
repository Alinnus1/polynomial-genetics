import random
import math as m
from math import floor
import copy

Increment = 0
g = open("file.out","a")

class Cromozon:
    """ Definitia clasei cromozom in care imi stochez informatiile referitoare la un individ si pe care o folosesc pentru a afisa coresponzutor informatiile.
    """
    
    def __init__(self,listCr,nr):
        self.listCr = listCr
        self.number = nr
        self.cromz = formatList(listCr)
        self.x = calculX(listCr)
        self.f = calculPoly(self.x)
        self.prob = 0
        self.incrucisare = False

    def set_number(self,nr):
        self.number = nr


    def __repr__(self):
        string = ""
        string += str(self.number)
        string +=": "
        string += str(self.cromz)
        string +=" x= "
        string += str(floor((self.x) * 10**prec)/(10**prec))
        string +=" f="
        string += str(self.f)
        if (self.incrucisare):
            string += f"<{probRec} participa"
        return string
    
def read(input_file):
    """O functie simpla pentru citirea informatiilor din fisierul input
    """
    
    f = open(input_file,"r")
    file_content = (f.readlines())#dimPop, domFun, 
    info = [float(x.strip()) for x in file_content]
    return info

def printPoly():
    """O functie simpla pentru afisarea polinomului dupa ce au fost citite datele de intrare
    """
    print(f"{coef4}*x^3 + {coef3}*x^2 + {coef2}*x + {coef1}")

def calculPoly(x):
    """O functie care preia din scopul global coeficientii polinomului si care primeste un x pentru care este calculat valoarea polinomului
    """
    list = [coef1,coef2,coef3,coef4]
    ans = 0
    for n,a in enumerate(list):
        ans += a*(x**n)
    return ans

def calculCrom():
    """O functie simpla care preia din scopul global l (lungimea sirului/cromozomului de forma '10010..') si care genereaz un sir coresponzuator aleator.
    """
    list = [random.choice([0,1]) for i in range(int(l))]
    return list

def formatList(lista):
    """O functie simpla care se ocupa de formatarea listei cromozomului pentru a putea fi citita. de ex 100110110011010111100
    """
    x=""
    for i in lista:
        x += str(i)
    return x

def calculX(list):
    """O functie care pe baza rezultatului functiei "calculCrom" ne ofera valoarea individului.
    """
    x = formatList(list)
    x = int(str(x),2)
    x = ((domFunU - domFunL)/(2**(int(l)) - 1))*x + domFunL
    return x

def generateFrstPop(dimPop):
    """O functie care imi genereaza prima populatie folosindu-se de clasa Cromozom si de functia calculCrom.
    """
    population = []
    for i in range(int(dimPop)):
        population.append(Cromozon(calculCrom(),i+1))

    return population

def printPop(population):
    """O functie care se ocupa de afisarea unei populatii in fisierul out
    """
    global Increment
    for i in population:
        print(i, end="\n")
        if (Increment == 0):
            g.write(str(i))
            g.write("\n")

def calcPerfPop(population):
    """O functie care calculeaza suma performantelor indivizilor dintr-o populatie data.
    """
    suma = 0
    for i in population:
        suma += i.f 
    return suma

def calcIntervProb(population):
    """O functie care genereaza probabilititatile cumulutate si care returneaza intervalele pentru selectie.
    """
    suma = calcPerfPop(population)
    
    listProbs = [0]
    tempSum = 0
    for i in population:
        tempSum += i.f/suma
        listProbs.append(tempSum)
    

    if (listProbs[-1]>1.0):
        listProbs[-1] = 0.9999999999999999
    return listProbs

def printPopProbs(population):
    """O functie care se ocupa de asignarea si afisarea probabilitatilor de selectie pnetru fiecare cromozom 
    """
    suma = calcPerfPop(population)
    global Increment

    for i in population:
        if (Increment == 0):
            #print(f"cromozon {str(i.number)} probabilitate {str(i.f/suma)}")
            g.write(f"\n cromozon {str(i.number)} probabilitate {str(i.f/suma)}")
        i.prob = i.f/suma

def randomBit():
    """O functie care returneaza un numar random din intervalul [0,1)
    """
    f = random.random()
    return f

indexat = 0
def searchIntv(val,array,begin,end):
    """O functie care se cauta binar intervalul potrivit pentru un cromozom dat si returneaza indexul elemtnului pe care trebuie sa l selectam.
    """
    # begin = 0
    # end = len(array) -1
    if (begin >= end):
        return -1

    mid = int((begin + end)/2)
    if (array[mid] > val):
        return searchIntv(val,array,begin,mid)
    index = searchIntv(val,array,mid+1,end)
    if (index == -1):

        # print ([array[mid],array[mid+1]])
        # return (mid+1)
        global indexat
        indexat = mid+1
    return indexat

def searchCromz(population,index):
    """O functie care imi returneaza cromozomul aflat la pozitia index dintr-o populatie data.
    """
    for i in population:
        if i.number == index:
            # print(i.prob)
            return i

def elitistSel(population):
    """O functie care gaseste cel mai bun cromozom dintr-o populatie si imi returneaza probabilitatea de selectie a acestuia.
    """
    if(not population):
        return 0
    x = population.pop()

    return max(x.prob,elitistSel(population))

def selection(population):
    """O functie care se ocupa de procesul de selectie
    """
    global Increment
    # dau populatia
    # calculez suma pentru populatia resepctiva # calc perfpop
    total = calcPerfPop(population)
    # fac porbabilatitile cumulate calcIntervprob
    q = calcIntervProb(population)
    if(Increment == 0):
        g.write("\n" + str(q) + "\n")
    intermPop = []
    printPopProbs(population)
    populationcopy = copy.deepcopy(population)
    best = elitistSel(populationcopy)
    # selectie etilista
    #print(best)
    
    for i in population:
        if i.prob == best:
            intermPop.append(i)
            break
    print(f"->> {intermPop}")
    if (Increment == 0):
        g.write(f"\n ->> {intermPop}")

    for i in range(0,int(dimPop)-1):
        # aleg un random bit
        rand = randomBit()
        index = searchIntv(rand,q,0,len(q)-1)
        intermCrom = searchCromz(population,index)
        #print(f"u={rand} selectam cromozomul {intermCrom.number}")
        if (Increment == 0):
            g.write(f"\n u={rand} selectam cromozomul {intermCrom.number}")
        intermPop.append(intermCrom)
    return intermPop

def setcrctnumber(population):
    """O functie simpla care imi reface ordinea cromozomilor.
    """
    populationcopy = []
    for c,i in enumerate(population):
        intermCr = Cromozon(i.listCr,c+1)
        populationcopy.append(intermCr)
    return populationcopy

def incr(population):
    """O functie care imi marcheaza dintr-o populatie indivizii care sunt ready for crossing-over
    """
    for i in population:
        bit = randomBit()
        if (bit<probRec):
            i.incrucisare = True

    return population
        
def incrApply(population):
    """O functie care aplica incrucisarea. Mai intai sunt izolati cromozomii care trebuie incrucisati iar apoi se trateaza toate cazurile posibile si se efectueaza incrucisarea cromozomilor 2 cate 2 sau in cazul in care numarul de cromozomi de incrucisat este impar 3.
    """
    global Increment
    realPopulation=[]
    incrPop = []
    for i in population:
        interm = copy.deepcopy(i)
        if i.incrucisare :
            incrPop.append(interm)
        else:
            realPopulation.append(interm)

    lungime = len(realPopulation[0].listCr)

    if (len(incrPop) % 2 == 0):
        for i in range(0,len(incrPop),2):
            randomx = random.randrange(0,lungime+1) # pentru ca e exlusiv al doilea parametru
            fstlistcr = incrPop[i].listCr
            sndlistcr = incrPop[(i+1)].listCr
            
            fstnewlistcr = fstlistcr[0:randomx] + sndlistcr[randomx:]
            sndnewlistcr = sndlistcr[0:randomx] + fstlistcr[randomx:]

            print(f"\n Recombinare dintre cromozomii {incrPop[i].number} si {incrPop[(i+1)].number} \n {formatList(fstlistcr)} {formatList(sndlistcr)} punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)}")

            realPopulation.append(Cromozon(fstnewlistcr,3))
            realPopulation.append(Cromozon(sndnewlistcr,4))
    else:
        if (len(incrPop) > 3):
            for i in range(0 , len(incrPop) - 3, 2):
                randomx = random.randrange(0,lungime+1) # pentru ca e exlusiv al doilea parametru
                fstlistcr = incrPop[i].listCr
                sndlistcr = incrPop[(i+1)].listCr
                
                fstnewlistcr = fstlistcr[0:randomx] + sndlistcr[randomx:]
                sndnewlistcr = sndlistcr[0:randomx] + fstlistcr[randomx:]

                #print(f"Recombinare dintre cromozomii {incrPop[i].number} si {incrPop[(i+1)].number} \n {formatList(fstlistcr)} {formatList(sndlistcr)} punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)}")
                if (Increment == 0):
                    g.write(f"\n Recombinare dintre cromozomii {incrPop[i].number} si {incrPop[(i+1)].number} \n {formatList(fstlistcr)} {formatList(sndlistcr)} punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)}")
                realPopulation.append(Cromozon(fstnewlistcr,3))
                realPopulation.append(Cromozon(sndnewlistcr,4))

            randomx = random.randrange(0,lungime +1)

            fstlistcr = incrPop[-3].listCr
            sndlistcr = incrPop[-2].listCr
            thrlistcr = incrPop[-1].listCr

            fstnewlistcr = fstlistcr[0:randomx] + sndlistcr[randomx:]
            sndnewlistcr = sndlistcr[0:randomx] + thrlistcr[randomx:]
            thrnewlistcr = thrlistcr[0:randomx] + fstlistcr[randomx:]

            #print(f"Recombinare dintre cromozomii {incrPop[-3].number} , {incrPop[(-2)].number} si {incrPop[-1].number}\n {formatList(fstlistcr)} {formatList(sndlistcr)} {formatList(thrlistcr)}  punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)} {formatList(thrnewlistcr)}")
            if (Increment == 0):
                g.write(f"\n Recombinare dintre cromozomii {incrPop[i].number} si {incrPop[(i+1)].number} \n {formatList(fstlistcr)} {formatList(sndlistcr)} punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)}")

            realPopulation.append(Cromozon(fstnewlistcr,3))
            realPopulation.append(Cromozon(sndnewlistcr,4))
            realPopulation.append(Cromozon(thrnewlistcr,5))
        elif (len(incrPop) == 3):
            randomx = random.randrange(0,lungime +1)

            fstlistcr = incrPop[-3].listCr
            sndlistcr = incrPop[-2].listCr
            thrlistcr = incrPop[-1].listCr

            fstnewlistcr = fstlistcr[0:randomx] + sndlistcr[randomx:]
            sndnewlistcr = sndlistcr[0:randomx] + thrlistcr[randomx:]
            thrnewlistcr = thrlistcr[0:randomx] + fstlistcr[randomx:]

            #print(f"Recombinare dintre cromozomii {incrPop[-3].number} , {incrPop[(-2)].number} si {incrPop[-1].number}\n {formatList(fstlistcr)} {formatList(sndlistcr)} {formatList(thrlistcr)}  punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)} {formatList(thrnewlistcr)}")
            if (Increment == 0):
                g.write(f"\n Recombinare dintre cromozomii {incrPop[-3].number} , {incrPop[(-2)].number} si {incrPop[-1].number}\n {formatList(fstlistcr)} {formatList(sndlistcr)} {formatList(thrlistcr)}  punct {randomx}\n Rezultat {formatList(fstnewlistcr)} {formatList(sndnewlistcr)} {formatList(thrnewlistcr)}")

            realPopulation.append(Cromozon(fstnewlistcr,3))
            realPopulation.append(Cromozon(sndnewlistcr,4))
            realPopulation.append(Cromozon(thrnewlistcr,5))


    return realPopulation

def mutationApply(population):
    """O functie care aplica procesul de mutatie si care imi updateaza cromozomul care a suferit mutatie.
    """
    global Increment
    #print(f"Probabilitatea de mutatie pentru fiecare gena {probMut} \n Au fost modificati cromozonii:") 
    if (Increment == 0):
        g.write(f"\n Probabilitatea de mutatie pentru fiecare gena {probMut} \n Au fost modificati cromozonii: \n")
    for i in population:
        bit = randomBit()
        if (bit<probMut):
            if(Increment == 0):
                g.write(str(i.number) + '\n')
            randomx = random.randrange(0,len(i.listCr))
            i.listCr[randomx] = 1 - i.listCr[randomx]
            i.cromz = formatList(i.listCr)
            i.x = calculX(i.listCr)
            i.f = calculPoly(i.x)

    return population

dimPop,domFunL,domFunU,coef1,coef2,coef3,coef4,prec,probRec,probMut,nrSteps = [0,0,0,0,0,0,0,0,0,0,0]

dimPop,domFunL,domFunU,coef1,coef2,coef3,coef4,prec,probRec,probMut,nrSteps = read("file.in")
print (dimPop,domFunL,domFunU,coef1,coef2,coef3,prec,probRec,probMut,nrSteps)
l = m.log2((domFunU - domFunL)*(10**prec))


printPoly()
x= generateFrstPop(dimPop)
printPop(x)
temp = x

for i in range(int(nrSteps)):
    temp = selection(temp)
    temp = setcrctnumber(temp)
    temp = incr(temp)
    temp = incrApply(temp)
    temp = setcrctnumber(temp)
    temp = mutationApply(temp)
    printPop(temp)
    g.write("\n" + str(calcPerfPop(temp)/dimPop) )
    Increment +=1

printPop(x)