"""
ESTE EJEMPLO VA A ABARCAR
EL USO DE INPUT, LABELS Y BOTONES
PARA FAMILIARZZARSE QUE COSAS BASICAS
DE FUNCIONALIUDAD PODEMOS LOGRAR CON FLET
"""

import flet as ft

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola nombre"

        self.input_nombre = ft.TextField( hint_text="Ingresa tu nombre" )
        self.button_saludar = ft.Button( text="Saludar", on_click=self.handle_saludo )
        self.text_saludo = ft.Text( value="" )

        self.build()

    def build(self):
        self.page.add(
            self.input_nombre,
            self.button_saludar,
            self.text_saludo
        )
        self.page.update()

    def handle_saludo(self, e):
        nombre = (self.input_nombre.value or "").strip()
        if nombre:
            self.text_saludo.value = f"Hola, {nombre}"
        else:
            self.text_saludo.value = "Ingrese un nombre"
        self.page.update


if __name__ == "__main__":
    ft.app(target=App)