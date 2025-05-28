from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🧠 Servidor de lectura de inventario funcionando."

@app.route('/procesar', methods=['POST'])
def procesar():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se ha enviado ninguna imagen."}), 400

    imagen = Image.open(request.files['imagen'].stream)
    texto = pytesseract.image_to_string(imagen)

    objetos_detectados = {}
    palabras = texto.lower().splitlines()

    objetos_validos = [
        "ganzua", "ganzua2", "polvos", "termita", "cuchillo", "maria",
        "mariaemp", "ziploc", "bidon", "cobre", "hierro", "goma", "chatarra",
        "fertilizante", "oxidadas", "aluminio", "acero", "cristal", "cogollos",
        "radio", "dinero"
    ]

    for linea in palabras:
        for obj in objetos_validos:
            if obj in linea:
                cantidad = ''.join(filter(str.isdigit, linea))
                cantidad = int(cantidad) if cantidad else 0
                objetos_detectados[obj] = objetos_detectados.get(obj, 0) + cantidad

    return jsonify(objetos_detectados)
