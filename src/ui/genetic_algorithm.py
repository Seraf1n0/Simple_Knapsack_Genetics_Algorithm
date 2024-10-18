import random

class Individuo:
    def __init__(self, cromosoma):
        self.cromosoma = cromosoma  # Esta será una lista 
        self.aptitud = 0     

    """
    Entrada: Conjunto de numeros aleatorio (o definido) y limite dado por la persona
    Funcionalidad: Hacemos la prueba viendo si con la elección se pasa del limite o no
    Salida: Se modifica la aptitud del individuo
    """
    def calcularAptitud (self, conjuntoNumeros, limite):
        sumaTotal = 0
        for i in range(len(conjuntoNumeros)-1):
            
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
PROB_CRUCE = 0.2 # Probabilidad de cruce del 30% (modificable)
PROB_MUTACION = 0.3 # Probabilidad de mutación del 50% debido a una cantidad de población baja y capacidad grande de fallar (puede depender del limite)      
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
    
#Aquí genero un subconjunto de tamaño aleatorio no mayor al de la población
def generarSubconjunto(poblacion):
    tamanioSubconjunto = random.randint(1, len(poblacion) -1)
    subconjunto = []
    #Ahora escojo elementos aleatorios de la población hasta completar el subconjunto
    i = 0
    while(i < tamanioSubconjunto):
        indiceAleatorio = random.randint(0, len(poblacion) -1) #Un índice que se encuentre dentro del rango
        #De momento creo que no es un problema que se repitan números
        elemento = poblacion[indiceAleatorio]
        subconjunto.append(elemento)
        i += 1
    return subconjunto

#Aquí sería ver si se pasa de la suma (retorno cero) o es menor o igual al valor que deseo maximizar
def funcionAdaptabilidad(individuo, limite):
    if(sum(individuo) <= limite):
        return sum(individuo)
    else:
        return 0

#Cruzo ambos
#En caso de ser listas de tamaños diferentes genero un número aleatorio entre ambas
def cruce(padre1, padre2):
    if random.random() < PROB_CRUCE:
        #Verifico si el tamaño de las listas es diferente
        subconjunto = []
        if(len(padre1) == len(padre2)):
            #Si el largo de la lista es impar entonces tengo que sumarle 1
            if(len(padre1) %2 != 0):
                cantidadElementosPadre1 = (len(padre1) //2) +1 #Con esto completo y me queda del mismo tamaño
                cantidadElementosPadre2 = len(padre1) //2
                #Ahora agrego los elementos del padre 1 al nuevo subconjunto. Da igual el orden en que lo haga porque no altera el valor de la suma
                for i in range(cantidadElementosPadre1):
                    indiceAleatorio = random.randint(0, len(padre1) -1)
                    subconjunto.append(padre1[indiceAleatorio])
                
                #Agrego los elementos del padre 2
                for i in range(cantidadElementosPadre2):
                    indiceAleatorio = random.randint(0, len(padre2) -1)
                    subconjunto.append(padre2[indiceAleatorio])

                #Retorno el subconjunto
                return subconjunto
            else:
                #El largo de la lista no es impar
                mitad = len(padre1) // 2
                for i in range(mitad):
                    #Agrego elemento del padre 1
                    indiceAleatorio = random.randint(0, len(padre1) -1)
                    subconjunto.append(padre1[indiceAleatorio])

                    #Agrego elemento del padre 2
                    indiceAleatorio = random.randint(0, len(padre2) -1)
                    subconjunto.append(padre2[indiceAleatorio])
                #Retorno el subconjunto
                return subconjunto
        else:
            #El largo de ambos padres es diferente, entonces genero un aleatorio entre ambos largos
            if(len(padre1) > len(padre2)):
                largoAleatorio = random.randint(len(padre2), len(padre1))
            else:
                largoAleatorio = random.randint(len(padre1), len(padre2))
            
            #Verifico si el aleatorio es par o impar
            if(largoAleatorio % 2 == 0):
                #Es par, entonces agrego la misma cantidad de elementos de ambos padres
                for i in range(largoAleatorio//2):
                    #Agrego elemento del padre 1
                    indiceAleatorio = random.randint(0, len(padre1) -1)
                    subconjunto.append(padre1[indiceAleatorio])

                    #Agrego elemento del padre 2
                    indiceAleatorio = random.randint(0, len(padre2) -1)
                    subconjunto.append(padre2[indiceAleatorio])
                #Retorno el subconjunto
                return subconjunto
            else:
                #El largo aleatorio es impar
                cantidadElementosPadre1 = (largoAleatorio //2) +1 #Con esto completo y me queda del mismo tamaño
                cantidadElementosPadre2 = largoAleatorio //2
                #Ahora agrego los elementos del padre 1 al nuevo subconjunto. Da igual el orden en que lo haga porque no altera el valor de la suma
                for i in range(cantidadElementosPadre1):
                    indiceAleatorio = random.randint(0, len(padre1) -1)
                    subconjunto.append(padre1[indiceAleatorio])
                
                #Agrego los elementos del padre 2
                for i in range(cantidadElementosPadre2):
                    indiceAleatorio = random.randint(0, len(padre2) -1)
                    subconjunto.append(padre2[indiceAleatorio])

                #Retorno el subconjunto
                return subconjunto
    else:
        #No cruzo, retorno el padre 1 porque es el mejor
        return padre1

def mutacion(individuo):
    if random.random() < PROB_MUTACION:
        #Hago la mutación. Cambio un índice de forma aleatoria por un valor aleatorio también
        indiceAleatorio = random.randint(0, len(individuo) -1)
        valorAleatorio = random.randint(0, max(individuo)) #El valor va a estar entre 0 y el más grande de la lista
        individuo[indiceAleatorio] = valorAleatorio
        return individuo
    else:
        return individuo
""" 
Entradas: None
Funcionalidad: Es el algoritmo principal que maneja los resultados finales por cada generación
Salida: No definido
"""
def algoritmoGenetico (tamanioPoblacion, tamanioConjunto, generaciones, valorMaximo):
    limiteP = 1000
    mejorSolucion = []
    sumaMejorSolucion= 0
    poblacion = generarPoblacionInicial(tamanioPoblacion, tamanioConjunto)
    conjuntoNumeros = generarConjuntoNumeros(tamanioConjunto, 1, valorMaximo) #Prueba con ese rango
    todasGeneraciones = [] # Almacenamos la cada generacion en un pesudoObjeto

    for individuo in poblacion: #Para calcular la aptitud de cada individuo de la población que no cambia
        individuo.calcularAptitud(conjuntoNumeros, limiteP) 
    
    #De momento no lo voy a ordenar por aptitud porque le saco aletoriedad
    subconjuntos = []
    for i in range(len(conjuntoNumeros)):
        subconjuntos += [generarSubconjunto(conjuntoNumeros)]
    #Ahora voy haciendo las generaciones
    for generacion in range(generaciones):
        #Generar los subconjuntos
        #Ahora tendría que ordenarlos revisando cuál es el mejor subconjunto y así sucesivamente
        subconjuntos.sort(key=lambda x: funcionAdaptabilidad(x, valorMaximo), reverse=True) #Con esto los ordeno por adaptabilidad. Tendría que poner al que tiene la mejor de primero y así sucesivamente

        # agarramos al mejor de la generación y lo almacenamos en la lista como un pesudoobjeto
        
        #Ahora tendría que ver si el mejor de esta generación es mejor que la solución anterior para guardarlo
        if(sum(subconjuntos[0]) > sumaMejorSolucion and sum(subconjuntos[0]) <= valorMaximo): #Si la suma del mejor subconjunto es mayor que el mejor valor actual y menor o igual que el que quiero maximizar entonces la guardo
            mejorSolucion = subconjuntos[0].copy()
            sumaMejorSolucion = sum(subconjuntos[0])
            todasGeneraciones.append({'generacion': generacion+1, 'subconjunto': mejorSolucion, 'suma': sumaMejorSolucion})

        
        #Ahora tendría que hacer el cruce y la mutación. Los padres van a ser los dos mejores de la generación actual
        nuevosSubconjuntos = []
        for i in range(len(conjuntoNumeros)): 
            #Genero elementos. Primero con el cruce
            padre1, padre2 = subconjuntos[0], subconjuntos[1]
            individuoCruzado = cruce(padre1, padre2)
            #Ahora al individuo cruzado intento aplicarle la mutación
            individuoCruzado = mutacion(individuoCruzado)
            #Agrego el nuevo individuo al subconjunto
            nuevosSubconjuntos.append(individuoCruzado)
            #Agrego el subconjuntoNuevo a la lista de nuevosSubconjuntos

        subconjuntos = nuevosSubconjuntos #Los subconjuntos de la nueva generación se ponen en los actuales para operar con ellos
    return mejorSolucion, sumaMejorSolucion, todasGeneraciones
        

