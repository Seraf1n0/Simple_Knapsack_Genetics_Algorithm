from flask import Flask, render_template, request
from genetic_algorithm import algoritmoGenetico

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html', respuesta=None)

@app.route('/generarSolucion', methods=['POST'])
def generarSolucion():
    tamanoPoblacion = int(request.form['tamanoPoblacion'])
    cantidadGeneraciones = int(request.form['cantidadGeneraciones'])
    valorMaximo = int(request.form['cantidadMaxima'])

    mejorSolucion, sumaMejorSolucion, generaciones = algoritmoGenetico(tamanoPoblacion, cantidadGeneraciones, valorMaximo)

    return render_template('main.html', respuesta=True, mejorSolucion=mejorSolucion, sumaMejorSolucion=sumaMejorSolucion, generaciones=generaciones)

if __name__ == '__main__':
    app.run(debug=True)