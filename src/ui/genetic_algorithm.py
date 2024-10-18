import random

#Constantes para el algoritmo genetico
PROB_CRUCE = 0.2 
PROB_MUTACION = 0.3 

"""
Entradas: Tamaño del conjunto a generar, un limite inferior y uno superior para realizar la generación de subconjuntos
Funcionalidad: Genera un conjunto con valores aleatorios pero dentro del límite establecido
Salida: Lista (conjunto de números)
"""
def generarConjuntoNumeros (tamano, minimo, maximo):
    conjunto = []
    iterador = 0
    while(iterador < tamano):
        elemento = random.randint(minimo, maximo)
        conjunto.append(elemento)
        iterador +=1
    print(conjunto)
    return conjunto

    
"""
Entrada: El conjunto de elementos que forman la población generada aleatoriamente de forma previa
Funcionalidad: Generar un subconjunto de tamaño aleatorio y con elementos aleatorios de la población
Salida: Una lista
"""
def generarSubconjunto(poblacion):
    mitadPoblacion = len(poblacion) //2
    limiteInferior = random.randint(1, mitadPoblacion)
    tamanioSubconjunto = random.randint(limiteInferior, len(poblacion) -1)
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

"""
Entrada: individuo, es una de las sublistas de números que conforman una generación
         limite, es el valor máximo que podría dar la suma de todos los elementos que conforman el individuo
Funcionalidad: Sumar todos los elementos de la lista para verificar si el valor se pasa del máximo que se desea alcanzar
               Esto es con el objetivo de en el algoritmo genético utilizar el resultado de esta función para ordenar los miembros de una generación
               desde el más cercano al valor a máximizar a los más lejanos o que se pasan del límite
Salida: 0 en caso de que el valor de la suma de todos los elementos que conforman al individuo sea mayor que el límite
        El valor de la suma de todos los elementos que conforman el individuo en caso de que este sea menor o igual al límite
"""
def funcionAdaptabilidad(individuo, limite):
    if(sum(individuo) <= limite):
        return sum(individuo)
    else:
        return 0

"""
Entrada: padre1 y padre2. Ambos son los mejores miembros de la generación
Funcionalidad: Generar un cruce entre ambos en para obtener un hijo que tenga similitud con ambos padres
Salida: El hijo generado en caso de realizarse el cruce o el padre1 en caso de que no se realice el cruce
"""
def cruce(padre1, padre2):
    if random.random() < PROB_CRUCE:
        puntoDeCruce = random.randint(0, len(padre1) - 1)
        hijo = padre1[:puntoDeCruce] + padre2[puntoDeCruce:]
        return hijo
    else:
        #No cruzo, retorno el padre 1 porque es el mejor
        return padre1

"""
Entrada: Un miembro de la generación para intentar mutarlo
Funcionalidad: Cambiar alguno de los valores que forman al individuo por otro aleatorio para dar más variedad a la generación
Salida: El individuo mutado en caso de hacerse la operación o el original si no se hizo nada 
"""
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
Salida: Todos los elementos de la salida son para utilizarlos en la interfaz gráfica
"""
def algoritmoGenetico (tamanioConjunto, generaciones, valorMaximo):
    mejorSolucion = []
    sumaMejorSolucion= 0
    conjuntoNumeros = generarConjuntoNumeros(tamanioConjunto, 1, valorMaximo) #Prueba con ese rango
    todasGeneraciones = [] # Almacenamos la cada generacion en un pesudoObjeto

    subconjuntos = []
    for i in range(len(conjuntoNumeros)):
        subconjuntos += [generarSubconjunto(conjuntoNumeros)]
    #Ahora voy haciendo las generaciones
    for generacion in range(generaciones):
        #Generar los subconjuntos
        #Ahora tendría que ordenarlos revisando cuál es el mejor subconjunto y así sucesivamente
        subconjuntos.sort(key=lambda x: funcionAdaptabilidad(x, valorMaximo), reverse=True) #Con esto los ordeno por adaptabilidad. Tendría que poner al que tiene la mejor de primero y así sucesivamente

        
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
        
        #Añado un elemento aleatorio en cada generación para evitar lo más posible casos donde nunca se encuentra una solución
        #Este elemento podría ser mejor que alguno de los hijos generados y ayude a crear una siguiente generación mejor
        #Por la aleatoriedad del algoritmo es imposible evitar que en algún momento no pueda generar una respuesta. La idea es minimizar las ocasiones en que esto suceda
        subconjuntoAleatorio = generarSubconjunto(conjuntoNumeros)
        subconjuntos.append(subconjuntoAleatorio)

        subconjuntos = nuevosSubconjuntos #Los subconjuntos de la nueva generación se ponen en los actuales para operar con ellos
    return mejorSolucion, sumaMejorSolucion, todasGeneraciones, conjuntoNumeros
        

