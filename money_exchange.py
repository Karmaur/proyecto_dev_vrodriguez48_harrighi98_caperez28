# The objective of the following code is to determine the amount on COP
# needed to exchange for a given amount in a different currency for remitance.

# Item 0: Importacion de librerias y clases
from cliente_remitente import ClienteRemitente
from cliente_destino import ClienteDestino
import requests
import xml.etree.ElementTree as ET

# Item 1: Importar monedas ISO
tree = ET.parse("ISO4217.xml")
root = tree.getroot()

# Item 2: Importar tasas de cambio
url = "https://api.exchangerate-api.com/v4/latest/COP"
datos = requests.get(url).json()

# Item 3: País y monedas ISO
paises_monedas = {}

# Item 4: Revisa los elementos de la ISO y almacena nombre, país y moneda
for elem in root.findall(".//CcyNtry"):
    pais_iso = elem.find("CtryNm")
    moneda_iso = elem.find("Ccy")
    nombre_iso = elem.find("CcyNm")

# Item 5: Solo incluye registros que estén completos(control de datos)
    if pais_iso is None or moneda_iso is None or nombre_iso is None:
        continue

    pais = pais_iso.text.split("(")[0].strip().upper()
    moneda = moneda_iso.text

# Item 6: Descarta monedas de uso especial
    if nombre_iso.get("IsFund") == "true":
        continue

# Item 7: Descarta monedas de uso especial
    if "Next day" in nombre_iso.text:
        continue

# Item 8: Solo la primera entrada para los países duplicados(control de datos)
    if pais not in paises_monedas:
        paises_monedas[pais] = moneda

# Item9 :Ingresar cliente remitente
print("=== INGRESAR DATOS CLIENTE REMITENTE ===")

nombre = input("Nombre: ")
apellido = input("Apellido: ")
pais = "Colombia"
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

# Item 10: Ingresar cliente destino
print("\n=== INGRESAR DATOS CLIENTE DESTINO ===")

nombre_dest = input("Nombre: ")
apellido_dest = input("Apellido: ")

# Item 11: Validación pais destino
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

# Item 12: Monedas disponibles
monedas = list(datos["rates"].keys())

# Item 13: pción moneda no disponible
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

# Item 14: Tasa del día
tasa_cambio = datos["rates"][moneda_destino]

# Item 15: Monto a enviar
print("La tasa del día para", moneda_destino, "es de:",
      round(1/tasa_cambio, 2), "COP por cada", moneda_destino)

while True:
    try:
        cantidad_remitente = input("¿Cuánto deseas enviar?")
        cantidad_remitente = float(cantidad_remitente.replace(",", "."))
        if cantidad_remitente < 20000:
            print("El monto minimo es de 20000 COP")

        elif cantidad_remitente > 13000000:
            print("El monto maximo es de 13000000 COP")

        else:
            break
    except ValueError:
        print("Entrada no válida. Por favor ingrese solo números enteros" +
              " o decimales. Ej: 150.98 ó 150,98")

# Item 16: Cálculo subtotal en COP
cantidad_destino = round(cantidad_remitente * tasa_cambio, 2)
print(cantidad_remitente, "COP equivalen a", cantidad_destino,
      moneda_destino, " antes de comisión e impuestos")

# Item 17: Calculo de impuesto y comisiones:
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
                        impuesto), 2)

# Item 18: Entrega de resultados
print("El total a pagar es de:", total_remitente, "COP")

# Finalizar transacción
remittance = input("¿Desea continuar con la transacción?")
if remittance.lower().strip() in ["sí", "si", "s"]:
    print("Usted será comunicado con un asesor para completar el envío de",
          cantidad_destino, moneda_destino, "a", destinatario1.nombre,
          destinatario1.apellido, "en", destinatario1.pais)
else:
    print("Transacción cancelada. Estaremos aquí para ayudarte cuando",
          "lo necesites.")
