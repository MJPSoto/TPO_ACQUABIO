
import datetime
from random import randint


def crear_nuevo_cliente():
    """aun se requiere agregar la fecha de instalacion y el conteo de dias para las alertas"""

    #se definiran las variables principales que posteriormente iran al csv
    nombre = input("Ingrse el nombre del cliente: ").lower
    telefono = int(input("Ingrese el teléfono del cliente: "))
    direccion = input("Ingrese la dirección del cliente: ").lower
    localidad = input("Ingrese la localidad del cliente: ").lower

    #tambien se definira la fecha de  la compra segun la fecha actual de ejecucion usando la libreria de datatime
    fecha_compra = datetime.datetime.now().strftime("%Y-%m-%d")
    id_cliente = randint(10000, 99999)
    
    #los valores seran cargados en un archivo csv
    with open("clientes.csv", "a+", newline='', encoding="utf-8") as file:
        writer = writer(file)
        writer.writerow([id_cliente, nombre, telefono, direccion, localidad, fecha_compra])

    print(f"Cliente {nombre} agregado correctamente con ID: {id_cliente}")


def actualizar_datos_cliente(cliente_id: int):
    """aun se requiere agregar la fecha de instalacion y su funcion de actualizarla dentro de la funcion"""
    filas = []
    encontrado = False

    # Leer todos los datos del archivo CSV
    with open("clientes.csv", "r", encoding="utf-8") as file:
        reader = reader(file)
        for fila in reader:
            if fila[0] == str(cliente_id):
                #se muestran los datos originales para que sea facil encontrar cual es el que debe ser actualizado
                print(f"Datos actuales del cliente con ID {cliente_id}:")
                print(f"Nombre completo: {fila[1]}")
                print(f"Teléfono: {fila[2]}")
                print(f"Dirección: {fila[3]}")
                print(f"Localidad: {fila[4]}")
                print(f"Fecha de compra: {fila[5]}")

                #se solicitan los nuevos valores o se mantienen los originales
                print("\nIngrese los nuevos datos (presiona enter para mantener los valores originales):")
                nombre = input(f"Nuevo nombre completo ({fila[1]}): ").lower or fila[1]
                telefono = input(f"Nuevo teléfono ({fila[2]}): ") or fila[2]
                direccion = input(f"Nueva dirección ({fila[3]}): ").lower or fila[3]
                localidad = input(f"Nueva localidad ({fila[4]}): ").lower() or fila[4]

                #la fecha de compra no se actualiza
                fecha_compra = fila[5]

                #se actualiza la fila con los nuevos valores
                fila = [cliente_id, nombre, telefono, direccion, localidad, fecha_compra]
                encontrado = True
            filas.append(fila)

    #en el caso de que el id no sea encontrado, se genera un error 
    if encontrado == False:
        print(f"Cliente con ID {cliente_id} no encontrado o inexistente")
        return
    
    #si todo se realizo correctamente, los datos son actualizados en el csv
    with open("clientes.csv", "w", newline='', encoding="utf-8") as file:
        writer = writer(file)
        writer.writerows(filas)

    print(f"Datos de cliente (ID {cliente_id}) actualizados correctamente")


def borrar_cliente(id_usaurio: int):
    """
    borrar cliente con ese id
    """
    pass

def mostrar_clientes():
    """
    Mostrar todos los datos de todos los clientes
    """
    pass

def ver_datos_cliente(id_usaurio: int):
    """
    Mostrar datos del cliente con ese id
    """
    pass