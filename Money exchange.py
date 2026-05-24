# The objective of the following code is to determine the amount on COP
# needed to exchange for a given amount in a different currency for remitance.

# Importar monedas ISO
import xml.etree.ElementTree as ET
tree = ET.parse("ISO4217.xml")
root = tree.getroot()

# Importar tasas de cambio
import requests
url = "https://api.exchangerate-api.com/v4/latest/COP"
datos = requests.get(url).json()

# País y monedas ISO
paises_monedas = {}

# Revisa los elementos de la ISO y almacena nombre, país y moneda
for elem in root.findall(".//CcyNtry"):
    pais_iso = elem.find("CtryNm")
    moneda_iso = elem.find("Ccy")
    nombre_iso = elem.find("CcyNm")

# Solo incluye registros que estén completos(control de datos)
    if pais_iso is None or moneda_iso is None or nombre_iso is None:
        continue

    pais = pais_iso.text.split("(")[0].strip().upper()
    moneda = moneda_iso.text

# Descarta monedas de uso especial
    if nombre_iso.get("IsFund") == "true":
        continue

# Descarta monedas de uso especial
    if "Next day" in nombre_iso.text:
        continue

# Solo la primera entrada para los países duplicados(control de datos)
    if pais not in paises_monedas:
        paises_monedas[pais] = moneda

# Monedas disponibles
monedas = list(datos["rates"].keys())

# Entrada país de destino
while True:
    try:
        pais_destino = input(
            "¿A qué país deseas enviar dinero?"
            ).upper()
        if pais_destino in paises_monedas:
            moneda_destino = paises_monedas[pais_destino]
            break
        else:
            print("País inválido, por favor asegurate de ingresar el nombre del país")
    except ValueError:
        print("Ingrese solo carácteres alfabeticos.")

# Entrada país de destino
while True:
    if moneda_destino in monedas:
        break
    else:
        moneda_destino = input(
            "Actualmente no manejamos esta moneda ¿Te gustaría enviar dolares o euros a "
            + pais_destino + "? (USD o EUR): "
            ).upper()

        if moneda_destino == "USD":
            break
        elif moneda_destino == "EUR":
            break
        else:
            print("No podemos enviar ", moneda_destino, "a ", pais_destino)
        
# Tasa del día
tasa_cambio = datos["rates"][moneda_destino]

# Monto a enviar
print("La tasa del día para", moneda_destino, "es de:",
      round(1/tasa_cambio, 2), "COP por cada", moneda_destino)

while True:
    try:
        cantidad_destino = input("¿Cuánto deseas enviar?")
        cantidad_destino = float(cantidad_destino.replace(",", "."))
        if cantidad_destino > 0:
            break
        else:
            print("La cantidad a enviar debe ser un número positivo.")
    except ValueError:
        print("Entrada no válida. Por favor ingrese solo números enteros" +
              " o decimales. Ej: 150.98 ó 150,98")

# Cálculo subtotal en COP
cantidad_remitente = round(cantidad_destino * tasa_cambio, 2)
print(cantidad_destino, "COP equivalen a", cantidad_remitente,
      moneda_destino, " antes de comisión e impuestos")

# Cuatro por mil
gravamen_mf = round(cantidad_remitente * 0.004, 2)

# Comisión
comision = round(cantidad_remitente * 0.05, 2)

# IVA
impuesto = round(comision * 0.19, 2)

# Total a pagar
total_remitente = round((cantidad_remitente + gravamen_mf + comision +
                        impuesto)/tasa_cambio, 2)
print("El total a pagar es de:", total_remitente, "COP")