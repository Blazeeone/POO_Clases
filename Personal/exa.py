"""Crear un CRUD personal"""

# Creacion de clase Usuario
class Usuario:
    def __init__(
            self,
            nombre: str,
            apellido: str,
            email: str,
            edad: int,
            nacionalidad: str
    ):
        self.nombre: str = nombre
        self.apellido: str = apellido 
        self.email: str = email
        self.edad: int = edad
        self.nacionalidad: str = nacionalidad

# Lista para lamacenar objetos instanciados de "class Ususario:"
usuarios: list [Usuario] = []

# Definir funcion de un ususario existente
def usuario_existente(nuevo_usuario: Usuario) -> bool:
    for usuario in usuarios:
        if (
            usuario.nombre == nuevo_usuario.nombre
            and usuario.apellido == nuevo_usuario.apellido
            and usuario.email == nuevo_usuario.email
            and usuario.edad == nuevo_usuario.edad
            and usuario.nacionalidad == nuevo_usuario.nacionalidad
        ):
            return True 
        return False

# Definir funcion de crear usuario
def create_usuario():
    nombre = str(input("Ingrese su nombre: "))
    apellido = str(input("Ingrese su apellido: "))
    email = str(input("Ingrese su correo (ej alberto@email.com): "))
    edad = int(input("Ingrese su edad: "))
    nacionalidad = str(input("Inngrese su nacionalidad: "))
    nuevo_usuario = Usuario(nombre, apellido, email, edad, nacionalidad)

    if not usuario_existente(nuevo_usuario):
        usuarios.append(nuevo_usuario)
        print("Usuario creado correctamente !!")

# Definir funcion de leer usuario
def read_usuario():
    for usuario in usuarios:
        print(usuario)

# Definir funcion de actualizar usuario
def update_usuario():
    nombre_busqueda = str(input("Ingrese el nombre: "))
    apellido_busqueda = str(input("Ingrese el apellido: "))
    for usuario in usuarios:
        if usuario.nombre == nombre_busqueda and usuario.apellido == apellido_busqueda:
            while True:
                print(" Editar el usuario ")

 
# Definir funcion de eliminar usuario
def delete_usuario():
    nombre_busqueda = str(input("Ingrese el nombre: "))
    apellido_busqueda = str(input("Ingrese el apellido: "))
    for usuario in usuarios:
        if usuario.nombre == usuario.nombre and usuario.apellido == usuario.apellido:
            usuarios.remove(usuario)
            print(f"Usuario con nombre y apellido {nombre_busqueda, apellido_busqueda} eliminado exitosamente!!")
        print(f"Usuario con nombre {nombre_busqueda} y apellido {apellido_busqueda} no encontrada")

# Menu de CRUD
print("===========================\n¡ Hola Bienvenido al CRUD !")

def menu():
    while True:
        print("""===========================
    ------ MENU CRUD ------
    1. Crear usuario
    2. Leer usuarios
    3. Actualizar persona
    4. Eliminar persona
    0. Salir
    """)    
        opcion = input("Selecione una opción:")
    
        if opcion == "1":
            create_usuario()
        elif opcion == "2":
            read_usuario()
        elif opcion == "3":
            update_usuario()
        elif opcion == "4":
            delete_usuario()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion invalida :( - Intente nuevamente!")

menu()