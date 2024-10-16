def ingresar_direccion():
    while True:
        try:
            direccion = input("Ingrese su direccion: ")
            if verificar_direccion(direccion):
                return direccion
        except Exception:
            print("Ingrese nuevamente su direccion.")
        
        
def verificar_direccion(direccion):
   patron = r"^[a-zA-Z0-9\s]+$"
   return bool(re.match(patron, direccion))


def ingresar_nombre() -> str:
    """En esta funcion verificamos si el nombre del cliente es valido

    Args:
        nombre (str): Ingreso nombre y apellido del cliente

    Returns:
        bool: retorno true si se cumplen las condiciones
    """
    while True:
        try:
            nombre = input("Ingrese su nombre y apellido: ")
            if verificar_nombre(nombre):
                return nombre
        except Exception:
            print("Error")
        
        
def verificar_nombre(nombre):
    nombre_valido = "[A-Za-z\s]{4,}$"
    return bool(re.match(nombre_valido, nombre))


def ingresar_telefono() -> str:
    """

    Returns:
        _type_: _description_
    """
    while True:
        try:
            telefono = input("Ingrese su numero de telefono. Ejemplo: 1122334455: ")
            if verificar_telefono(telefono):
                return telefono
        except ValueError:
            print("Error")            

    
def verificar_telefono(telefono:str) ->bool:
    """Esta funcion verifica si un numero es valido

    Args:
        telefono (int): le paso como parametro un numero que por lo menos tenga 10 digitos y sea positivo

    Returns:
        bool: retorna true si se cumple y false si no
    """
    if telefono.isdigit() and len(telefono) == 10:
        return True
    return False


def ingresar_fecha_compra():
    while True:
        try:
            anio = int(input("Ingrese su el anio de la compra: "))
            if anio > 2015:
                mes = int(input("Ingrese el mes de la compra: "))
                if mes >= 1 and mes <= 12:
                    dia = int(input("Ingrese el dia de la compra: "))
                    if dia >= 1 and dia <= 31:
                        fecha_compra = anio, mes, dia
                        if verificar_fecha_compra(anio, mes, dia):
                            return fecha_compra
        except ValueError:
            print("Ingrese solo datos numericos.")
                

def verificar_fecha_compra(anio, mes, dia) -> bool:
    """En esta funcion verifico si la fecha ingresada es valida

    Args:
        No recibe argumentos

    Returns:
        bool: retorno true si es valida
    """
    while True:
        fecha_compra = datetime.date(anio, mes, dia)
        if fecha_compra:
            return True
        else:
            print("Fecha invalida, ingrese nuevamente los datos")
            
            
def id_cliente() ->tuple:
    """Esta funcion lee el JSON y guarda los datos en una lista. Verifica si hay algun valor en "id"
    Si no lo hay, guardamos 0 en la lista, caso contrario, el mayor dato encontrado en "id".
    Retornamos

    Returns:
        bool: Retorna una tupla con el id
    """
    maximo = 0
    clientes = leer_JSON()
    lista_id = []
    numero_a_sumar = 1
    if "id" in clientes:
        lista_id.append(clientes["id"])
    maximo = max(lista_id, default=0)  # Valor por defecto si la lista está vacía
    print(clientes)
    return (maximo + numero_a_sumar)


def obtener_datos_cliente():
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """
    ide = id_cliente()
    nombre = ingresar_nombre()
    telefono = ingresar_telefono()
    direccion = ingresar_direccion()
    fecha_compra = ingresar_fecha_compra()
    
    nuevo_cliente = {
        "id": ide,
        "nombre": nombre,
        "telefono": telefono,
        "direccion": direccion,
        "fecha_compra": fecha_compra,
    }
    return nuevo_cliente