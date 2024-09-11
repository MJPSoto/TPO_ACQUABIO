import os
from tabulate import tabulate

def crear_archivo_productos():
    file = open("archivo_productos.csv", "a+", encoding="utf-8")
    for value in dict_productos.values():
        cadena = ",".join(value) + "\n"
        file.write(cadena)
    return None


def crear_nuevo_cliente():
    "Nombre completo"
    "Telefono"
    "Dirección"
    "Localidad"
    "fecha de compra"
    "fecha instalación"
    """
    fecha de compra --> fecha actual de ejecución
    pasaron 3 dias 
    pasaron 30 dias 
    tomar la fecha de compra si la localidad es afuera de la costa 
    en caso contrario tomar la fecha de instalación

    generar un numero aleatorio de 5 digitos para el usuario

    investigar json 
    csv 
    diccionarios 
    listas de listas 
    """
    pass


def actualizar_datos_cliente(id_usaurio: int):
    """
    actualizar datos del cliente con ese id
    {
        16573: {nombre, telefono, dirección....etc}
    }
    """
    pass


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
