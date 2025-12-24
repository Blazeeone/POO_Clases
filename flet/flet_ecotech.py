from ecotech import Auth, Database, Finance, History
from dotenv import load_dotenv
import flet as ft
import os
import datetime
import time

load_dotenv()

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Financial"
        
        # --- 1. CONFIGURACIÓN DE FUENTES (Google Fonts) ---
        self.page.fonts = {
            "Montserrat": "https://fonts.gstatic.com/s/montserrat/v25/JTUSjIg1_i6t8kCHKm459Wlhyw.woff2",
            "OpenSans": "https://fonts.gstatic.com/s/opensans/v34/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS-muw.woff2"
        }
        
        # --- 2. TEMA ---
        self.page.theme = ft.Theme(font_family="OpenSans")
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800
        
        # Colores
        self.col_bg = "#0f172a"         
        self.col_card = "#1e293b"       
        self.col_primary = "#6366f1"    
        self.col_input_bg = "#334155"   
        self.col_text_h = "#f8fafc"     
        self.col_text_p = "#cbd5e1"     
        self.col_border = "#475569"     
        
        self.page.bgcolor = self.col_bg
        
        # Sesión
        self.current_user_id = None
        self.current_username = None
        
        print("Iniciando Ecotech...")
        
        # DB
        self.db = Database(
            username=os.getenv("ORACLE_USERNAME"), 
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )

        try:
            self.db.create_all_tables()
            print("Conexión DB: Exitosa.")
        except Exception as error:
            # Ignoramos error si la tabla ya existe
            pass

        self.finance = Finance()
        
        # Iniciar App
        self.page_login() 

    # --- UTILIDAD: INPUTS ---
    def get_input(self, label, icon, is_password=False):
        return ft.TextField(
            label=label,
            password=is_password,
            can_reveal_password=is_password,
            prefix_icon=icon,
            border_radius=12,
            bgcolor=self.col_input_bg,
            color=ft.Colors.WHITE,
            border_color=ft.Colors.TRANSPARENT,
            text_size=14,
            label_style=ft.TextStyle(color=self.col_text_p, size=12),
            cursor_color=self.col_primary
        )

    # --- UTILIDAD: BOTÓN PRIMARIO ---
    def get_primary_button(self, text, action):
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Text(text, size=14, weight="bold", font_family="Montserrat", color=ft.Colors.WHITE),
                on_click=action,
                bgcolor=ft.Colors.TRANSPARENT,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=15
                ),
                width=300,
            ),
            gradient=ft.LinearGradient(
                colors=[self.col_primary, "#4f46e5"],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.3, self.col_primary), offset=ft.Offset(0, 5))
        )

    # ==========================
    # PANTALLA 1: REGISTRO
    # ==========================
    def page_register(self):
        self.page.clean()
        
        self.input_username = self.get_input("Usuario", ft.Icons.PERSON_OUTLINE)
        self.input_password = self.get_input("Contraseña", ft.Icons.LOCK_OUTLINE, is_password=True)
        self.text_status = ft.Text(size=12, weight="bold")
        
        content = ft.Column([
            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=60, color=self.col_primary),
            ft.Text("Nueva Cuenta", size=28, weight="bold", font_family="Montserrat", color=self.col_text_h),
            ft.Text("Comienza tu gestión financiera hoy.", size=13, color=self.col_text_p),
            
            ft.Container(height=30),
            
            self.input_username,
            ft.Container(height=15),
            self.input_password,
            
            ft.Container(height=30),
            
            self.get_primary_button("CREAR CUENTA", self.handle_register),
            
            ft.Container(height=20),
            self.text_status,
            
            ft.Container(height=20),
            ft.Divider(color=self.col_border),
            ft.TextButton(
                content=ft.Text("Volver al Login", color=self.col_text_p),
                on_click=lambda e: self.page_login()
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.page.add(
            ft.Container(
                content=content,
                padding=40,
                alignment=ft.alignment.center,
                expand=True
            )
        )
        self.page.update()

    def handle_register(self, e):
        user = self.input_username.value
        pwd = self.input_password.value
        
        if not user or not pwd:
            self.text_status.value = "⚠️ Completa los campos"
            self.text_status.color = ft.Colors.AMBER
            self.page.update()
            return

        res = Auth.register(self.db, user, pwd)
        self.text_status.value = res["message"]
        self.text_status.color = ft.Colors.GREEN_400 if res["success"] else ft.Colors.RED_400
        self.page.update()

    # ==========================
    # PANTALLA 2: LOGIN
    # ==========================
    def page_login(self):
        self.page.clean()
        
        self.input_username = self.get_input("Usuario", ft.Icons.PERSON)
        self.input_password = self.get_input("Contraseña", ft.Icons.LOCK, is_password=True)
        self.text_status = ft.Text(size=12, weight="bold", color=ft.Colors.RED_400)

        content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.SHOW_CHART, size=50, color=ft.Colors.WHITE),
                padding=20,
                bgcolor=self.col_primary,
                border_radius=50,
                shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.4, self.col_primary))
            ),
            ft.Container(height=20),
            
            # CORRECCIÓN: Eliminado letter_spacing para evitar error
            ft.Text("ECOTECH", size=32, weight="bold", font_family="Montserrat", color=self.col_text_h),
            ft.Text("Financial Solutions", size=14, color=self.col_primary, weight="bold"),
            
            ft.Container(height=40),
            
            self.input_username,
            ft.Container(height=15),
            self.input_password,
            
            ft.Container(height=30),
            
            self.get_primary_button("ACCEDER", self.handle_login),
            
            ft.Container(height=20),
            self.text_status,
            
            ft.Container(height=30),
            ft.Row(
                [
                    ft.Text("¿Eres nuevo?", size=13, color=self.col_text_p),
                    ft.TextButton(
                        content=ft.Text("Regístrate", color=self.col_primary, weight="bold"),
                        on_click=lambda e: self.page_register()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.page.add(
            ft.Container(
                content=content,
                padding=40,
                alignment=ft.alignment.center,
                expand=True
            )
        )
        self.page.update()

    def handle_login(self, e):
        user = self.input_username.value
        pwd = self.input_password.value

        res = Auth.login(self.db, user, pwd)
        
        if res["success"]:
            self.current_user_id = res["user_id"]
            self.current_username = user
            self.page_main_menu()
        else:
            self.text_status.value = "Credenciales incorrectas"
            self.page.update()

    # ==========================
    # PANTALLA 3: DASHBOARD
    # ==========================
    def page_main_menu(self):
        self.page.clean()
        
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Bienvenido,", color=self.col_text_p, size=13),
                    ft.Text(f"{self.current_username}", color=self.col_text_h, size=22, weight="bold", font_family="Montserrat")
                ]),
                ft.Container(
                    content=ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ft.Colors.WHITE, on_click=lambda e: self.page_login(), tooltip="Cerrar Sesión"),
                    bgcolor=ft.Colors.WHITE10,
                    border_radius=10
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(25),
        )

        def menu_card(icon, title, subtitle, action, color_grad):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=35, color=ft.Colors.WHITE),
                    ft.Container(height=10),
                    ft.Text(title, size=16, weight="bold", color=ft.Colors.WHITE, font_family="Montserrat"),
                    ft.Text(subtitle, size=11, color=ft.Colors.WHITE70),
                ], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.START),
                
                width=160, height=180,
                padding=20,
                border_radius=20,
                gradient=ft.LinearGradient(
                    colors=color_grad,
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right
                ),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK, offset=ft.Offset(0, 5)),
                on_click=action,
                ink=True 
            )

        self.page.add(
            ft.Column([
                header,
                ft.Container(
                    content=ft.Column([
                        ft.Text("Resumen", size=18, weight="bold", color=self.col_text_h, font_family="Montserrat"),
                        ft.Container(height=20),
                        
                        ft.Row([
                            menu_card(
                                ft.Icons.CURRENCY_EXCHANGE, 
                                "Cotizar", 
                                "Mercado en vivo", 
                                lambda e: self.page_indicador_menu(),
                                [self.col_primary, "#818cf8"] 
                            ),
                            menu_card(
                                ft.Icons.HISTORY, 
                                "Historial", 
                                "Tus registros", 
                                lambda e: self.page_history_menu(),
                                ["#334155", "#475569"] 
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Container(height=30),
                        
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.SECURITY, color=self.col_primary),
                                ft.Column([
                                    ft.Text("Conexión Segura", weight="bold", size=12, color=self.col_text_h),
                                    ft.Text("Base de datos Oracle encriptada", size=11, color=self.col_text_p)
                                ])
                            ], spacing=15),
                            bgcolor=self.col_card,
                            border_radius=15,
                            padding=20,
                            border=ft.border.all(1, self.col_border)
                        )
                    ]),
                    padding=25
                )
            ])
        )
        self.page.update()

    # ==========================
    # PANTALLA 4: COTIZADOR
    # ==========================
    def page_indicador_menu(self):
        self.page.clean()
        
        app_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=self.col_text_h, on_click=lambda e: self.page_main_menu()),
                ft.Text("Nueva Cotización", size=18, weight="bold", font_family="Montserrat", color=self.col_text_h)
            ]),
            padding=ft.padding.only(top=20, left=10, bottom=10)
        )

        self.dd_indicador = ft.Dropdown(
            label="Moneda / Indicador",
            options=[
                ft.dropdown.Option("uf"),
                ft.dropdown.Option("dolar"),
                ft.dropdown.Option("euro"),
                ft.dropdown.Option("utm"),
            ],
            value="dolar",
            bgcolor=self.col_input_bg,
            color=ft.Colors.WHITE,
            border_radius=12,
            border_color=self.col_border,
            focused_border_color=self.col_primary,
            text_size=14,
            label_style=ft.TextStyle(color=self.col_text_p),
        )
        
        self.input_fecha = ft.TextField(
            label="Fecha de Consulta", 
            hint_text="Ej: 20-12-2024",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500), 
            value=datetime.datetime.now().strftime("%d-%m-%Y"),
            bgcolor=self.col_input_bg,
            color=ft.Colors.WHITE,
            border_radius=12,
            border_color=self.col_border,
            focused_border_color=self.col_primary,
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            text_size=14,
            label_style=ft.TextStyle(color=self.col_text_p)
        )

        self.text_resultado = ft.Text(value="---", size=36, weight="bold", color=self.col_primary, font_family="Montserrat")
        self.loading_bar = ft.ProgressBar(width=150, color=self.col_primary, bgcolor=self.col_card, visible=False)

        # Botón Guardar - SIMPLIFICADO para evitar errores
        self.btn_guardar = ft.ElevatedButton(
            "Guardar Cotización", 
            disabled=True, 
            on_click=self.handle_save_history,
            icon=ft.Icons.SAVE,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            width=280,
            height=45
        )
        
        self.last_val = 0.0
        self.last_ind = ""
        self.last_date = ""

        main_card = ft.Container(
            content=ft.Column([
                self.dd_indicador,
                ft.Container(height=15),
                self.input_fecha,
                
                ft.Container(height=30),
                
                self.get_primary_button("CONSULTAR VALOR", self.handle_consultar_api),
                
                ft.Container(height=30),
                self.loading_bar,
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Valor del mercado", size=12, color=self.col_text_p),
                        self.text_resultado,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    border=ft.border.all(1, self.col_border),
                    border_radius=15,
                    width=300,
                    bgcolor=self.col_bg 
                ),
                
                ft.Container(height=20),
                self.btn_guardar
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            padding=30,
            bgcolor=self.col_card,
            border_radius=20,
            border=ft.border.all(1, self.col_border),
            margin=20
        )

        self.page.add(ft.Column([app_bar, main_card]))
        self.page.update()

    def handle_consultar_api(self, e):
        ind = self.dd_indicador.value
        fecha = self.input_fecha.value
        
        self.loading_bar.visible = True
        self.text_resultado.value = "..."
        self.btn_guardar.disabled = True
        self.page.update()
        time.sleep(0.5)

        res = self.finance.get_indicator(ind, fecha)
        
        self.loading_bar.visible = False
        
        if res["success"]:
            valor = res["valor"]
            self.text_resultado.value = f"${valor}"
            self.last_val = valor
            self.last_ind = ind
            self.last_date = fecha
            
            # --- RESET DEL BOTÓN ---
            self.btn_guardar.disabled = False
            self.btn_guardar.text = "Guardar Cotización"
            self.btn_guardar.icon = ft.Icons.SAVE
            self.btn_guardar.bgcolor = ft.Colors.GREEN_600
        else:
            self.text_resultado.value = "Error"
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {res.get('message')}"), bgcolor=ft.Colors.RED_900)
            self.page.snack_bar.open = True
        
        self.page.update()

    def handle_save_history(self, e):
        if self.current_user_id:
            ok = History.save_query(self.db, self.current_user_id, self.last_ind, self.last_val, self.last_date)
            if ok:
                self.page.snack_bar = ft.SnackBar(ft.Text("Cotización registrada"), bgcolor=ft.Colors.GREEN_800)
                self.page.snack_bar.open = True
                self.btn_guardar.disabled = True 
                self.btn_guardar.text = "Guardado"
                self.btn_guardar.icon = ft.Icons.CHECK_CIRCLE
                self.btn_guardar.bgcolor = ft.Colors.GREY_800 # Visualmente desactivado
                self.page.update()
            else:
                 self.page.snack_bar = ft.SnackBar(ft.Text("Error de conexión BD"), bgcolor=ft.Colors.RED_900)
                 self.page.snack_bar.open = True
                 self.page.update()

    # ==========================
    # PANTALLA 5: HISTORIAL
    # ==========================
    def page_history_menu(self):
        self.page.clean()
        
        app_bar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=self.col_text_h, on_click=lambda e: self.page_main_menu()),
                ft.Text("Historial de Operaciones", size=18, weight="bold", font_family="Montserrat", color=self.col_text_h)
            ]),
            padding=ft.padding.only(top=20, left=10, bottom=10)
        )

        datos = History.get_history(self.db, self.current_user_id)
        
        rows = []
        if datos:
            for d in datos:
                rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Container(
                            content=ft.Text(str(d[0]).upper(), weight="bold", color=self.col_primary, size=11),
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            bgcolor=ft.Colors.with_opacity(0.1, self.col_primary),
                            border_radius=6,
                            border=ft.border.all(1, self.col_primary)
                        )),
                        ft.DataCell(ft.Text(f"${d[1]}", weight="bold", color=ft.Colors.GREEN_400, font_family="OpenSans")),
                        ft.DataCell(ft.Text(str(d[2]), size=12, color=self.col_text_p)),
                    ])
                )
        else:
            rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("Sin registros")), ft.DataCell(ft.Text("-")), ft.DataCell(ft.Text("-"))]))

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("TIPO", weight="bold", color=self.col_text_p, size=11)),
                ft.DataColumn(ft.Text("VALOR", weight="bold", color=self.col_text_p, size=11)),
                ft.DataColumn(ft.Text("FECHA", weight="bold", color=self.col_text_p, size=11)),
            ],
            rows=rows,
            border=ft.border.all(1, self.col_border),
            vertical_lines=ft.border.BorderSide(1, self.col_card),
            heading_row_color=self.col_card,
            column_spacing=15,
            data_row_min_height=50
        )

        self.page.add(
            ft.Column([
                app_bar,
                ft.Container(
                    content=ft.Column([
                        ft.Text("Últimos Movimientos", size=14, color=self.col_text_p),
                        ft.Container(height=10),
                        ft.Container(
                            content=data_table, 
                            border_radius=15, 
                            bgcolor=self.col_card, 
                            padding=10,
                            border=ft.border.all(1, self.col_border)
                        ),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20,
                    expand=True
                )
            ], expand=True)
        )
        self.page.update()

# ==========================
# MAIN
# ==========================
def main(page: ft.Page):
    app = App(page)

if __name__ == "__main__":
    ft.app(target=main)