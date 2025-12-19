# 1. Paso: Importar Flet
import flet as ft

# 2. Paso: Clase principal de la aplicacion 
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola Mundo"
        # Siempre como ultima linea de __init__
        self.build()
    # Metodo principal para agregar elementos
    # En mi pagina/aplicacion
    def build(self):
        self.page.add(
            ft.Text("Hola Mundo!!")        
        )

# 3. paso: Inicializzamos la app
if __name__ == "__main__":
    ft.app(target=App)