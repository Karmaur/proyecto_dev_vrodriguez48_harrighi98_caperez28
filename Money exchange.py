# The objective of the following code is to determine the amount on COP
# needed to exchange for a given amount in a different currency for remitance.
from cliente_remitente import ClienteRemitente
from cliente_destino import ClienteDestino
import requests
import xml.etree.ElementTree as ET

# Importar monedas ISO
tree = ET.parse("ISO4217.xml")
root = tree.getroot()

# Importar tasas de cambio
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

# Ingresar cliente remitente
print("=== INGRESAR DATOS CLIENTE REMITENTE ===")

nombre = input("Nombre: ")
apellido = input("Apellido: ")
pais = input("País: ")
correo = input("Correo: ")
documento = input("Documento: ")
telefono = input("Teléfono: ")
ciudad = input("Ciudad: ")
ocupacion = input("Ocupación: ")
ingreso = input("Tipo de ingreso: ")

cliente1 = ClienteRemitente(
    nombre,
    apellido,
    pais,
    correo,
    documento,
    telefono,
    ciudad,
    ocupacion,
    ingreso
)

# Ingresar cliente destino
print("\n=== INGRESAR DATOS CLIENTE DESTINO ===")

nombre_dest = input("Nombre: ")
apellido_dest = input("Apellido: ")

# Validación pais destino
while True:
    pais_dest = input("País: ").strip().upper()
    if pais_dest in paises_monedas:
        moneda_destino = paises_monedas[pais_dest]
        break
    print("País inválido. Intenta nuevamente.")

telefono_dest = input("Teléfono: ")
correo_dest = input("Correo: ")

destinatario1 = ClienteDestino(
    nombre_dest,
    apellido_dest,
    pais_dest,
    telefono_dest,
    correo_dest
)

# Monedas disponibles
monedas = list(datos["rates"].keys())

# Opción moneda no disponible
while True:
    if moneda_destino in monedas:
        break
    else:
        moneda_destino = input(
            "Actualmente no manejamos esta moneda ¿Te gustaría enviar " +
            "dolares o euros a " + pais_dest + "? (USD o EUR): "
            ).upper()

        if moneda_destino == "USD":
            break
        elif moneda_destino == "EUR":
            break
        else:
            print("No podemos enviar ", moneda_destino, "a ", pais_dest)

# Tasa del día
tasa_cambio = datos["rates"][moneda_destino]

# Monto a enviar
print("La tasa del día para", moneda_destino, "es de:",
      round(1/tasa_cambio, 2), "COP por cada", moneda_destino)

while True:
    try:
        cantidad_destino = input("¿Cuánto deseas enviar?")
        cantidad_destino = float(cantidad_destino.replace(",", "."))
        if cantidad_destino < 20000:
            print("El monto minimo es de 20000 COP.")

        else:
            break
    except ValueError:
        print("Entrada no válida. Por favor ingrese solo números enteros" +
              " o decimales. Ej: 150.98 ó 150,98")

# Cálculo subtotal en COP
cantidad_remitente = round(cantidad_destino * tasa_cambio, 2)
print(cantidad_destino, "COP equivalen a", cantidad_remitente,
      moneda_destino, " antes de comisión e impuestos")
# Cuatro por mil
gravamen_mf = round(cantidad_remitente * 0.004, 2)
print("El 4x1000 es de:", gravamen_mf, "COP")

# Comisión
comision = round(cantidad_remitente * 0.05, 2)
print("La comisión es de:", comision, "COP")

# IVA
impuesto = round(comision * 0.19, 2)
print("El IVA sobre la comisión es de:", impuesto, "COP")

# Total a pagar
total_remitente = round((cantidad_remitente + gravamen_mf + comision +
                        impuesto)/tasa_cambio, 2)

# Entrega de resultados
print("El total a pagar es de:", total_remitente, "COP")

