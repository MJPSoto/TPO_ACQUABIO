from menues import menues as menu
from funciones import funcionesX as fx
import json
import re

RUTA = "JSON/mensajes.json"


def mensaje_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es valido o no

    pre: recive un string

    post: devuelve un booleno
    """
    #al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))

def volver_menu()-> None:
    """
    Pregunta si quiere volver al menú. Te lleva al menú principal si ingresa "y" y te lleva al menu mensajes
    si ingresa "n".

    pre: no recibe nada

    post: no devuelve nada
    """
    ok = input("¿Desea volver al menú principal? (y/n): ").lower()
    if ok == "y":
        menu.menu_principal()
    elif ok == "n":
        menu.menu_mensajes()
    else:
        print("Valor ingresado incorrecto")
        #si ingresa un valor ingorrecto vuelve a iniciar la función
        volver_menu()
    return None


def obtener_datos_mensaje() -> list[str]:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida

    pre: no recive nada

    post: devuelve una lista con los datos
    """
    while True:
        mensaje = []
        nuevo_mensaje = input("Ingrese nuevo mensaje: ")
        #verifico si el mensaje es valido y no es demasiado largo
        if mensaje_valido(nuevo_mensaje):
            try:
                dias = input("Ingrese la cantidad de días: ")
                #verifico que la cantidad de dias sea valida
                if int(dias) > 0 and int(dias) <= 100:
                    print(f"El mensaje es: {nuevo_mensaje}")
                    print(f"La cantidad de dias ingresados es: {dias}")
                    #verificación de que el mensaje ingresado es correcto
                    ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
                    if ok == "y":
                        mensaje = [dias, nuevo_mensaje]
                        return mensaje
                    elif ok == "n":
                        continue
                    else:
                        print("Valor ingresado incorrecto")
            except ValueError:
                print("Datos ingresados son incorrectos")
        else:
            print("El mensaje ingresado no es valido")
        return mensaje
    
    

def crear_mensaje() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: no recibe nada

    post: no devuelve nada
    """
    #leo el json y lo guardo en la variable mansajes
    mensajes = fx.leer_JSON(RUTA)
    nuevo_mensaje = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    try:    
        dias = nuevo_mensaje[0]
        #defino los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
        #copruebo si el mensaje ya existe
        if mensajes[0].get(dias) is None:
            #creo el mensaje nuevo
            mensajes[0][dias] = mensaje
            print("Mensaje cargado.")
        else:
            #compruebo si quiere reescribir el mensaje
            ok = input("El ID de mensaje ya existe quiere reemplazarlo (y/n): ").lower()
            if ok == "y":
                mensajes[0][dias] = mensaje
                ver_mensajes()
                print("Mensaje cargado.")
            else:
                #esto no se si dejarlo asi o volver a la carga de mensajes
                print("No se creó ningun mensaje...")
        #reescribo el json
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        menu.menu_mensajes()
    except IndexError as e:
        print(f"Error: {e}")
        crear_mensaje()
    return None


def actualizar_mensaje() -> None:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la dias
    que es la cantidad de dias, y si está modifica el mensaje

    pre: no recive nada

    port: no devuelve nada
    """
    ver_mensajes()
    #leo el json
    mensajes = fx.leer_JSON(RUTA)
    #obtengo el menssaje nuevo
    nuevo_mensaje = obtener_datos_mensaje()
    print(nuevo_mensaje)
    try: ############# verifica el uso del try, los try van donde sabes que va a fallar tu codigo 
        #defino los dias desde la lista devuelta en la linea anterior
        dias = nuevo_mensaje[0]
        #defino los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
        #comparo para ver si la dias(los dias) existen en el json
        while True:    
            if mensajes[0].get(dias) is None: #####################ojo el codigo flecha
                #compruebo si quiere crear el mensaje
                ok = input("El ID de mensaje no existe, desea crearlo (y/n): ").lower()
                if ok == "y":
                    mensajes[0][dias] = mensaje
                    print("mensaje cargado.")
                    break
                elif ok == "n": ########################## si ya comprobaste que no sea y no hace falta que vulvas a preguntar si es n
                    #esto no se si dejarlo asi o volver a la carga de mensajes##############
                    print("No se creó ningun mensaje...")
                    break
                else:
                    print("Opcion incorrecta")
            else:
                #actualizo el valor del mensaje
                mensajes[0][dias] = mensaje
                print("mensaje cargado.")
                break
        #vuelvo a cargar todo en el json
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        menu.menu_mensajes()
    except IndexError as e:
        print(f"Error: {e}")
        actualizar_mensaje()
    return None



def borrar_mensaje() -> None:
    """
    Lee el json encontrando el mensaje que se quiere borrar mediante el Id, vuelve a cargar
    el json con los mensajes excepto el eliminado.

    pre: no recive nada

    prost: no devuelve nada
    """
    ver_mensajes()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = input("Ingrese la cantidad de días: ") ######################## upa acá no puede dar error, cuando se castea un input y ese casteo no se puede hacer, eso genera un error
    #verifico que la cantidad de dias sea valida
    if not re.match("\b([1-9][0-9]{0,2})\b", dias):####################### trata de usar retorno rapido y no usar los ifs en flecha ######cambie el >1 <100 por una expresion regular
        return "Candidad de dias invalida"       
        
    #leo el json
    mensajes = fx.leer_JSON(RUTA)

    mensaje = mensajes[0].get(dias)
            
    #comparo para ver si la dias(los dias) existen en el json
    if mensaje is None:
    #si no encuentra ningun mensaje
        volver_menu()
        return "Mensaje no encontrado" ### tenemos que devolver cosas no printear cosas 

    print(mensaje)
    ok = input("Es este el mensaje que desea eliminar? (y/n): ").lower()
    if ok == "n":
        return "No se modificó ningun mensaje"        

    if ok != "y":
        volver_menu()
        return "Valor incorrecto"

    del mensajes[0][dias]
        
    # Vuelvo a cargar todo en el JSON
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    return "Mensaje eliminado."
        

def ver_mensajes() -> None:
    """
    Lee el json para imprimirlas en pantalla

    pre: no recive nada

    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    for key, value in mensajes[0].items():
        print(f"Dias: {key}- mensaje: {value}")
    volver_menu()
    return None


def ver_mensaje() -> None:
    """
    Busca un mensaje mediante el id, si lo encuentra lo mustra en pantalla

    pre: no recive nada

    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    try:
        dias = input("Ingrese la cantidad de días: ") ############################# lo mismo acá que en la anterior función 
        #verifico que la cantidad de dias sea valida
        if int(dias) > 0 and int(dias) <= 100: ##################### ojo con el codigo flecha
            #comparo para ver si la dias(los dias) existen en el json
            try:
                if mensajes[0].get(dias) is None:
                    print("Mensaje no encontrado")
                else:
                    print(f"Dias: {dias}- mensaje: {mensajes[0][dias]}")
            except KeyError as e:
                print(f"Error: {e}")
                menu.menu_mensajes()
        else:
            print("Cantidad de dias ingresada no valida.")
            volver_menu()
    except ValueError:
        print("El valor ingresado es invalido")
        volver_menu()
    except IndexError as e:
        print(f"Error: {e}")
        volver_menu()
    return None
