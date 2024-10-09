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
        for i in range(len(conjuntoNumeros)-1):
            
            if (self.cromosoma[i] == 1): # Si el cromosoma indica que se selecciona entonces lo sumamos al total
                sumaTotal += conjuntoNumeros[i]

        if (sumaTotal > limite):
            self.aptitud = 0 # "Falló" por lo que no tomamos en cuenta su elección
        else:
            self.aptitud = sumaTotal # No se pasó por lo que es candidato a mejores

# =============== Funciones auxiliares =========================================
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

# ========== Prueba mieo =================================================

if (__name__ == "__main__"):
    limite = 80
    tamanoConjunto = 10
    tamanoPoblacion = 10

    conjuntoNumeros = generarConjuntoNumeros(tamanoConjunto, 1, 100)
    print(f"Conjunto de números usado: {conjuntoNumeros}")

    poblacion = generarPoblacionInicial(tamanoPoblacion, tamanoConjunto)

    # Prueba de una sola generación, pa ver sisirve
    for individuo in poblacion:
        individuo.calcularAptitud(conjuntoNumeros, limite)
        print(f"Cromosoma: {individuo.cromosoma}, Aptitud: {individuo.aptitud}")

