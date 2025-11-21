"""
CRUD
---
CREATE : crear un nuevo registro
Read: Leer registro/s
Update: Actualizar un registro existente
Delete: Eliminar un registro existente
"""
"""
Glorasario
----
* pass
Palabra reservada para que Python no exija el mínimo necesario para el funcionamiento de la funcion/metodo.

* IDE
Viene de la palabra Integrated Development Environment que significa Entorno de Desarrollo Integrado, que son 
los editores de código que normalmente usamos para programar en informática.

* lint o linter
Es el encargado de vigilar que la sintaxis del código IDE sea correcta y te sugiere
en funcion de este.
"""
from datetime import date

# Primero, debemos crear una clase
class Persona:
    #Definir como se inicializa
    def __init__(
            self,
            rut,
            digito_verificador: str,
            nombres: str,
            apellido: str,
            fecha_nacimiento: date,
            cod_area: int,
            telefono: int
    ):
        
    
        
        self.rut: int = rut
        self.digito_verificador: str = digito_verificador
        self.nombres: str = nombres
        self.apellidos: str = apellido
        self.fecha_nacimiento: date = fecha_nacimiento
        self.cod_area: int = cod_area
        self.telefono: int = telefono    

    def __str__(self):
        return f"""
                Rut: {self.rut}-{self.digito_verificador}
                Nombre Completo: {self.nombres} {self.apellidos}
                Fecha de nacimiento: {self.fecha_nacimiento}
                Teléfono: +{self.cod_area} {self.telefono}
                """

# Creamos una lista para almacenar varios objetos instanciados de la clase Persona
personas: list [Persona] = []


def persona_existente(nueva_persona: Persona) -> bool:
    for persona in personas:
        if persona.rut == nueva_persona.rut:
            print(f"La persona con rut: {persona.rut}-{persona.digito_verificador} ya existe.")
            return True
    print("Persona no existente.")
    return False

def create_persona():
    rut = int(input("Ingrese el RUT (sin dígito verificador): "))
    digito_verificador = input("Ingrese el dígito verificador: ")
    nombres = input("Ingrese los nombres: ")
    apellidos = input("Ingrese los apellidos: ")
    
    dia_nacimiento = int(input("Ingrese el día de nacimiento (1-31): "))
    mes_nacimiento = int(input("Ingrese el mes de nacimiento (1-12): "))
    anio_nacimiento = int(input("Ingrese el año de nacimiento (YYYY): "))
    fecha_nacimiento_input = date(anio_nacimiento, mes_nacimiento, dia_nacimiento)
    cod_area = int(input("Ingrese el código de área: "))
    telefono = int(input("Ingrese el número de teléfono: ")) 
    
    nueva_persona = Persona(
        rut,
        digito_verificador,
        nombres,
        apellidos,
        fecha_nacimiento_input,
        cod_area,
        telefono
    )

    if not persona_existente(nueva_persona):
        personas.append(nueva_persona)
        print("Persona creada exitosamente.")

def read_persona():
    for persona in personas:
        print("="*20)
        print(persona)
        print("="*20)

def update_persona():
    rut_busqueda = int(input("Ingresa el rut sin dígito verificador (ej: 12345678): "))
    for persona in personas:
        if persona.rut == rut_busqueda:
            while True:
                print(
                f"""
                ===========================
                || Edición de personas ||
                ===========================
                1. Rut: {persona.rut}
                2. Dígito verificador: {persona.digito_verificador}
                3. Nombres: {persona.nombres}
                4. Apellidos: {persona.apellidos}
                5. Fecha de nacimiento: {persona.fecha_nacimiento}
                6. Código de área: {persona.cod_area}
                7. Teléfono: {persona.telefono}
                0. No seguir modificando.
                """
                )
                opcion = input("¿Qué dato quieres modificar?: ")

                if opcion == "1":
                    nuevo_rut = int(input("Ingresa el nuevo rut (sin dígito verificador): "))
                    persona.rut = nuevo_rut
                    
                elif opcion == "2":
                    nuevo_digito_verificador = input("Ingresa el nuevo dígito verificador: ")
                    persona.digito_verificador = nuevo_digito_verificador
                
                elif opcion == "3": 
                    nuevos_nombres = input("Ingresa los nuevos nombres: ")
                    persona.nombres = nuevos_nombres    
                
                elif opcion == "4":
                    nuevos_apellidos = input("Ingresa los nuevos apellidos: ")
                    persona.apellidos = nuevos_apellidos    
                
                elif opcion == "5":
                    anio = int(input("Ingresa el año de nacimiento (YYYY): "))
                    mes = int(input("Ingresa el mes de nacimiento (1-12): "))
                    dia = int(input("Ingresa el día de nacimiento (1-31): "))
                    persona.fecha_nacimiento = date(anio, mes, dia)
                
                elif opcion == "6":
                    nuevo_cod_area = int(input("Ingresa el nuevo código de área: "))
                    persona.cod_area = nuevo_cod_area
                
                elif opcion == "7":
                    nuevo_telefono = int(input("Ingresa el nuevo teléfono: "))
                    persona.telefono = nuevo_telefono
                
                elif opcion == "0":
                    print("Edición finalizada.")
                    break
                
                else:
                    print("Opción no válida.")

def delete_persona():
    rut_busqueda = int(input("Ingresa el rut sin dígito verificador (ej: 12345678): "))
    for persona in personas:
        if persona.rut == persona.rut:
            personas.remove(persona)
            print(f"Persona con rut {rut_busqueda} eliminada exitosamente.")
    print(f"persona con rut {rut_busqueda} no encontrada.")
    input("Presiona Enter para continuar...")        
            

def menu():
    while True:
        print("""
        ==========================
        ||       MENÚ CRUD      ||
        ==========================
        1. Crear persona
        2. Leer personas
        3. Actualizar persona
        4. Eliminar persona
        0. Salir
        """)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            create_persona()
        elif opcion == "2":
            read_persona()
        elif opcion == "3":
            update_persona()
        elif opcion == "4":
            delete_persona()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

print(
      "?\nBienvenido al sistema CRUD de personas.")
menu()