from flask import Flask, render_template, request
from genetic_algorithm import algoritmoGenetico

#Para generar la aplicación
app = Flask(__name__)

#Página principal que no carga ningún resultado
@app.route('/')
def main():
    return render_template('main.html', respuesta=None)

#Con esta se muestra la solución al algoritmo
@app.route('/generarSolucion', methods=['POST'])
def generarSolucion():
    tamanoPoblacion = int(request.form['tamanoPoblacion'])
    cantidadGeneraciones = int(request.form['cantidadGeneraciones'])
    valorMaximo = int(request.form['cantidadMaxima'])

    mejorSolucion, sumaMejorSolucion, generaciones, poblacion = algoritmoGenetico(tamanoPoblacion, cantidadGeneraciones, valorMaximo)

    return render_template('main.html', respuesta=True, mejorSolucion=mejorSolucion, sumaMejorSolucion=sumaMejorSolucion, generaciones=generaciones, tamanoPoblacion = str(tamanoPoblacion), cantidadGeneraciones= str(cantidadGeneraciones), valorMaximo = str(valorMaximo), listaPoblacion = poblacion)

if __name__ == '__main__':
    app.run(debug=True)