import random

class Individuo:
    def __init__(self, cromosoma):
        self.cromosoma = cromosoma  # Esta será una lista 
        self.aptitud = 0     

    """
    Entrada: Conjunto de numeros aleatorio (o definido) y limite dado por la persona
    Funcionalida: Hacemos la prueba viendo si con la elección se pasa del limite o no
    Salida: Se modifica la aptitud del individuo
    """
    def calcularAptitud (self, conjuntoNumeros, limite):
        sumaTotal = 0
        for i in range(len(conjuntoNumeros)):
            
            if (self.cromosoma[i] == 1): # Si el cromosoma indica que se selecciona entonces lo sumamos al total
                sumaTotal += conjuntoNumeros[i]

        if (sumaTotal > limite):
            self.aptitud = 0 # "Falló" por lo que no tomamos en cuenta su elección
        else:
            self.aptitud = sumaTotal # No se pasó por lo que es candidato a mejores


# =============== Funciones auxiliares =========================================
#Constantes para el algoritmo genetico
TAMANO_POBLACION = 20
TAMANO_CONJUNTO = 10
GENERACIONES = 50
PROB_CRUCE = 0.3 # Probabilidad de cruce del 30% (modificable)
PROB_MUTACION = 0.5 # Probabilidad de mutación del 50% debido a una cantidad de población baja y capacidad grande de fallar (puede depender del limite)      
LIMITE = 70 # De momento esto sería para pruebas

"""
Entradas: Tamaño del conjunto a generar, un limite inferior y uno superior para realizar la generación de subconjuntos
Funcionalidad: Genera un conjunto con valores aleatorios pero dentro del límite establecido
Salida: Lista (conjunto de números)
"""
def generarConjuntoNumeros (tamano, minimo, maximo):
    conjunto = []

    for i in range(tamano):
        conjunto.append(random.randint(minimo, maximo))
    return conjunto

"""
Entradas: Tamaño del cromosoma a generar (mismo tamaño del conjunto de números)
Funcionalidad: Generar un cromosoma con 1s y 0s para cada individuo
Salida: Cromosoma generado
"""
def generarCromosoma (tamano):
    cromosoma = []
    for i in range(tamano):
        cromosoma.append(random.randint(0,1)) # 1: Toma el numero, 0: No lo toma
    return cromosoma


"""
Entradas: tamaño de la población y el tamaño del cromosomas (el mismo tamaño del conjunto)
Funcionalidad: Genera una población inicial de individuos cada uno con un cromosoma unico
Salida: La población generada
"""
def generarPoblacionInicial (tamano, tamanoCromosoma):
    poblacion = []

    for i in range(tamano):
        cromosoma = []
        # Generar el cromosomas de cada individuo
        cromosoma = generarCromosoma(tamanoCromosoma)
        poblacion.append(Individuo(cromosoma))
    return poblacion

"""
Entradas: población a ordenar
Funcionalidad: ordenar la población por medio de su aptitud. Los que tengan más alto este valor irán de primero
Salida: La población ordenada
"""
def ordenarPorAptitud(poblacion):
    largo = len(poblacion)
    if largo > 1:
        #Poner los menores que el pivote a la izquierda y los mayores a la derecha
        pivote = poblacion[(largo-1) //2]
        menores = []
        mayores = []
        poblacion = poblacion[0:((largo-1) //2)] + poblacion[((largo-1) //2)+1:]
        largo = (len(poblacion)) 
        for i in range(largo):
            if(poblacion[i].aptitud < pivote.aptitud):
                menores += [poblacion[i]]
            elif(poblacion[i].aptitud >= pivote.aptitud):
                mayores += [poblacion[i]]
        return ordenarPorAptitud(mayores) + [pivote] + ordenarPorAptitud(menores)
        #return ordenarPorAptitud(menores) + [pivote] + ordenarPorAptitud(mayores)
    else:
        return poblacion

"""
Entradas: Poblacion a ordenar
Funcionalidad: Seleccionar unicamente la primer mitada de los mejores, utilizando la función ordenarPorAptitud
Salida: Población de mejores aptitudes
"""
def seleccionarMejores(poblacion):
    poblacionOrdenada = ordenarPorAptitud(poblacion)
    poblacionOrdenada = poblacionOrdenada.reverse() # Asi los mejoles van a estar al inicio (si se ordena de menor a mashor)
    # Agraramos solamente la primer mitad de los mejores
    return poblacion[:len(poblacion)//2]

def cruce(padre1, padre2):
    #Magia negra (No es el cruce xd)
    hijo1 = padre1
    hijo2 = padre2
    return hijo1, hijo2

"""
Entradas: None
Funcionalidad: Es el algoritmo principal que maneja los resultados finales por cada generación
Salida: No definido
"""
def algoritmoGenetico ():
    poblacion = generarPoblacionInicial(TAMANO_POBLACION, TAMANO_CONJUNTO)
    conjuntoNumeros = generarConjuntoNumeros(TAMANO_CONJUNTO, 1, 100)

    mejorGlobal = None  # Mejor solución hasta el momento, inicia en none por si queremos meter individo o solo un numero

    for generacion in range(GENERACIONES):
    
        # Calculams la aptitud de cada individio de la poblacion actual
        for individuo in poblacion:
            individuo.calcularAptitud(conjuntoNumeros, LIMITE)

        # Tomamos unicamente un pequeño porcentaje de los individuos de aptidud menor al limite
        mejores = seleccionarMejores(poblacion) # Retorna una lista de individupps

        mejorGeneracion = mejores[0]
        if ((mejorGlobal is None) or (mejorGeneracion.aptitud > mejorGlobal.aptitud)): # En caso de que sea la primera generación o bien haya habido un cambio, lo reasignamos
            mejorGlobal = mejorGeneracion

        print(f"Generación: {generacion}  Mejor solución actual: {mejorGlobal}")

        nuevaPoblacion = []
        while len(nuevaPoblacion) < TAMANO_POBLACION:
            padre1, padre2 = random.sample(mejores, 2)
            if (random.random() < PROB_CRUCE):
                hijo1, hijo2 = cruce(padre1, padre2)
                nuevaPoblacion.append(hijo1)
                nuevaPoblacion.append(hijo2)
            else:
                # Si no cae en la probabikdad, mantenemos los padres en la generación
                nuevaPoblacion.append(padre1)
                nuevaPoblacion.append(padre2)

        for individuo in nuevaPoblacion:
            #Sería por cada individuo nuevo ver si puede ser mutado incluso usar la miutacion para el cromosoma
            #mutacion(individuo)
            1=1 # para que no de error el for

        poblacion = nuevaPoblacion


# ========== Prueba mieo =================================================

if (__name__ == "__main__"):
    limite = 1000
    tamanoConjunto = 15
    tamanoPoblacion = 50

    conjuntoNumeros = generarConjuntoNumeros(tamanoConjunto, 1, 100)
    print(f"Conjunto de números usado: {conjuntoNumeros}")

    poblacion = generarPoblacionInicial(tamanoPoblacion, tamanoConjunto)

    # Prueba de una sola generación, pa ver sisirve
    for individuo in poblacion:
        individuo.calcularAptitud(conjuntoNumeros, limite)
        print(f"Cromosoma: {individuo.cromosoma}, Aptitud: {individuo.aptitud}")

