import os
from tabulate import tabulate
from random import randint
import datetime

def crear_archivo_productos():
    file = open("archivo_productos.csv", "a+", encoding="utf-8")
    for value in dict_productos.values():
        cadena = ",".join(value) + "\n"
        file.write(cadena)
    return None


def crear_nuevo_cliente():
    #se definiran las variables principales que posteriormente iran a el diccionario
    nombre = input("Ingrse el nombre del cliente: ").lower
    telefono = int(input("Ingrese el teléfono del cliente: "))
    direccion = input("Ingrese la dirección del cliente: ").lower
    localidad = input("Ingrese la localidad del cliente: ").lower

    #tambien se definira la fecha de  la compra segun la fecha actual de ejecucion usando la libreria de datatime
    fecha_compra = datetime.datetime.now().strftime("%Y-%m-%d")

    #se genera un numero aleatorio de 5 cifras que servira como id unico del
    id_cliente = random.randint(10000, 99999)
    
    #los valores seran cargados en un archivo csv
    with open("clientes.csv", "a+", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([cliente_id, nombre, telefono, direccion, localidad, fecha_compra])

    print(f"Cliente {nombre} agregado correctamente con ID: {cliente_id}")

def actualizar_datos_cliente(cliente_id = int):
    filas = []
    encontrado = False

    # Leer todos los datos del archivo CSV
    with open("clientes.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
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
        writer = csv.writer(file)
        writer.writerows(filas)

    print(f"Datos de cliente (ID {cliente_id}) actualizados correctamente")


def borrar_cliente(id_usaurio: int):
    """
    borrar cliente con ese id
    """
    pass


def ver_datos_cliente(id_usaurio: int):
    """
    Mostrar datos del cliente con ese id
    """
    pass

def mostrar_clientes():
    """
    Mostrar todos los datos de todos los clientes
    """
    pass


def crear_nuevo_mensaje():
    """
    Se repíte lo mismo de arriba 
    id mensaje --> generado aleatoriamente  
    cantidad de dias 
    mensaje 
    """
    pass


def actualizar_mensaje(id_mensaje: int):
    """
    Actualizar mensaje con ese id
    """
    pass


def borrar_mensaje(id_mensaje: int):
    """
    Borrar mensaje con ese id
    """
    pass


def ver_mensajes():
    """
    Ver todos los mensajes disponibles
    """
    pass


dict_productos = {
    110: ["Sal", "8000", "25kg"],
    111: ["filtro de carbón activado", "17500", "mini"],
    112: ["filtro de carbón activado", "50000", "xl"],
    113: ["filtro de carbón activado", "112500", "jumbo"],
    114: ["filtro de carbón activado", "8000", "BIG BLUE"],
    115: ["filtro de sedimentos", "5000", "mini"],
    116: ["filtro de sedimentos", "10000", "xl"],
    117: ["filtro de sedimentos", "17500", "jumbo"],
    118: ["filtro de sedimentos", "43750", "BIG BLUE"],
    119: ["filtro de carbón granular", "23000", "mini"],
    120: ["resina", "190000", "25Ls"],
}

def clear_console() -> None:
    """
    contrato: esta función limpia la consola
    pre: esta función no obtiene ningun parametro
    post: esta función no devuelve nada None
    """
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu(key) -> None:
    for i, value in enumerate(dict_opciones[key]):
        print(f"{i+1}. {value}")
    return None


def main():
    clear_console()
    logo_menu = [["Sistema de avisos ACQUABIO"], [""], ["by Cocucha"]]
    print(tabulate(logo_menu, tablefmt="fancy_grid", colalign=("center",)))
    while True:
        try:
            print(
                tabulate(
                    [[f"{i+1}. {valor}" for i, valor in enumerate(dict_opciones[1])]],
                    tablefmt="fancy_grid",
                )
            )
            opcion = int(input("Seleccione una de las opciones: "))
            break
        except ValueError as e:
            print(f"Error {e}")
    # validación correcta
    match opcion:
        case 1:
            # desplegar segundo menu
            print(
                tabulate(
                    [[f"{i+1}. {valor}" for i, valor in enumerate(dict_opciones[2])]],
                    tablefmt="fancy_grid",
                )
            )
            pass
        case 2:
            # desplegar tercer menu
            print(
                tabulate(
                    [[f"{i+1}. {valor}" for i, valor in enumerate(dict_opciones[3])]],
                    tablefmt="fancy_grid",
                )
            )
            pass
        case _:
            print("La opción no existe")

# variables globales
amplitud = 5
longitud = 40
velocidad = 0.1
dict_opciones = {
    1: ["Administrar clientes", "Administrar mensajes"],
    2: [
        "Ingresar un nuevo cliente",
        "Actualizar datos de un cliente",
        "Borrar un cliente",
        "Ver datos de un cliente",
    ],
    3: [
        "Ingresar nuevo mensaje",
        "Actualizar un mensaje",
        "Borrar un mensaje",
        "Ver todos los mensajes",
    ],
}

if __name__ == "__main__":
    main()
