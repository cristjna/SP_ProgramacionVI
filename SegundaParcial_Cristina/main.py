import flet as ft 
from contact_manager import ContactManager
from fpdf import FPDF
import pandas as pd
import datetime

# Clase para crear un PDF con un encabezado y pie de página personalizados
class PDF(FPDF):
    def header(self):
        # Configura la fuente y el texto del encabezado
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos', 0, 1, 'C')  # Crea una celda para el título

    def footer(self):
        # Configura la posición del pie de página y el texto
        self.set_y(-15)  # Establece la posición vertical
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')  # Muestra el número de página


# Clase que define la interfaz de usuario principal
class FormUi(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page  # Guarda la página de Flet
        self.data = ContactManager()  # Inicializa el gestor de contactos
        self.selected_row = None  # Variable para almacenar la fila seleccionada

        # Definición de colores para la interfaz
        color_principal = "#030311"
        color_secundario = "#00a992"
        color_fondo = "#1a1a2e"

        # Creación de campos de entrada para datos de contacto
        self.name = ft.TextField(label="Nombre", border_color=color_secundario)
        self.age = ft.TextField(label="Edad", border_color=color_secundario,
                                input_filter=ft.NumbersOnlyInputFilter(),
                                max_length=2)
        self.email = ft.TextField(label="Correo", border_color=color_secundario)
        self.phone = ft.TextField(label="Telefono", border_color=color_secundario,
                                  input_filter=ft.NumbersOnlyInputFilter(),
                                  max_length=9)
        
        # Campo de búsqueda por nombre
        self.searh_field = ft.TextField(
                            suffix_icon=ft.icons.SEARCH,
                            label="Buscar por el nombre",
                            border=ft.InputBorder.UNDERLINE,
                            border_color=color_secundario,
                            label_style=ft.TextStyle(color=color_secundario),
                            on_change=self.searh_data,
                        )     
      
        # Definición de la tabla para mostrar los contactos
        self.data_table = ft.DataTable(
                            expand=True,
                            border=ft.border.all(2, color_secundario),
                            data_row_color={ft.MaterialState.SELECTED: color_secundario, ft.MaterialState.PRESSED: color_principal},
                            border_radius=10,
                            show_checkbox_column=True,
                            columns=[
                                ft.DataColumn(ft.Text("Nombre", color=color_secundario, weight="bold")),
                                ft.DataColumn(ft.Text("Edad", color=color_secundario, weight="bold")),
                                ft.DataColumn(ft.Text("Correo", color=color_secundario, weight="bold"), numeric=True),
                                ft.DataColumn(ft.Text("Telefono", color=color_secundario, weight="bold"), numeric=True),
                            ],
                        )        
        
        self.show_data()  # Muestra los datos iniciales en la tabla

        # Definición del contenedor del formulario
        self.form = ft.Container(
            bgcolor=color_fondo,
            border_radius=10,
            col=4,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Ingrese sus datos",
                            size=40,
                            text_align="center",
                            font_family="sans-serif"),
                    self.name,
                    self.age,
                    self.email,
                    self.phone,
                    ft.Container(
                        content=ft.Row(
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                # Botón para guardar un contacto
                                ft.TextButton(text="Guardar",
                                              icon=ft.icons.SAVE,
                                              icon_color=color_principal,
                                              style=ft.ButtonStyle(color=color_fondo, bgcolor=color_secundario),
                                              on_click=self.add_data,
                                              ),
                                # Botón para actualizar un contacto
                                ft.TextButton(text="Actualizar",
                                              icon=ft.icons.UPDATE,
                                              icon_color=color_principal,
                                              style=ft.ButtonStyle(color=color_fondo, bgcolor=color_secundario),
                                              on_click=self.update_data,
                                              ),    
                                # Botón para borrar un contacto
                                ft.TextButton(text="Borrar",
                                              icon=ft.icons.DELETE,
                                              icon_color=color_principal,
                                              style=ft.ButtonStyle(color=color_fondo, bgcolor=color_secundario),
                                              on_click=self.delete_data,
                                              ),                          
                            ]
                        )
                    )
                ]
            )
        )

        # Definición del contenedor de la tabla
        self.table = ft.Container(
            bgcolor=color_fondo,
            border_radius=10,
            padding=10,
            col=8,
            content=ft.Column(   
                expand=True,           
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                self.searh_field,
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=self.edit_flied_text,
                                    icon_color=color_secundario,
                                ),
                                ft.IconButton(tooltip="Descargar en PDF",
                                              icon=ft.icons.PICTURE_AS_PDF,
                                              icon_color=color_secundario,
                                              on_click=self.save_pdf,
                                              ),     
                                ft.IconButton(tooltip="Descargar en EXCEL",
                                              icon=ft.icons.SAVE_ALT,
                                              icon_color=color_secundario,
                                              on_click=self.save_excel,
                                              ),  
                            ]
                        ),
                    ),

                    # Contenedor para mostrar la tabla de contactos
                    ft.Column(
                        expand=True, 
                        scroll="auto",
                        controls=[
                        ft.ResponsiveRow([
                            self.data_table
                            ]),  # Muestra la tabla de datos
                        ]
                    )
                ]
            )
        )

        # Combinación del formulario y la tabla en un contenedor responsivo
        self.conent = ft.ResponsiveRow(
            controls=[
                self.form,
                self.table
            ]
        )
    
    def show_data(self):
        # Muestra los contactos en la tabla
        self.data_table.rows = []  # Limpia las filas existentes
        for x in self.data.get_contacts():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,  # Maneja la selección de filas
                    cells=[
                        ft.DataCell(ft.Text(x[1])),  # Nombre
                        ft.DataCell(ft.Text(str(x[2]))),  # Edad
                        ft.DataCell(ft.Text(x[3])),  # Correo
                        ft.DataCell(ft.Text(str(x[4]))),  # Teléfono
                    ]
                )
            )
        self.update()  # Actualiza la tabla en la interfaz

    def add_data(self, e):
        # Agrega un nuevo contacto a la base de datos
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value)
        
        # Verifica que todos los campos estén llenos
        if len(name) and len(age) and len(email) and len(phone) > 0:
            contact_exists = False
            # Comprueba si el contacto ya existe
            for row in self.data.get_contacts():
                if row[1] == name:
                    contact_exists = True
                    break

            if not contact_exists:  # Si el contacto no existe, lo agrega
                self.clean_fields()  # Limpia los campos
                self.data.add_contact(name, age, email, phone)  # Agrega el contacto
                self.show_data()  # Actualiza la tabla
            else:
                print("El contacto ya existe en la base de datos.")
        print("Escriba sus datos")  # Mensaje para el usuario

    def get_index(self, e):
        # Obtiene el índice de la fila seleccionada en la tabla
        if e.control.selected:
           e.control.selected = False
        else: 
            e.control.selected = True  # Cambia la selección
        name = e.control.cells[0].content.value  # Obtiene el nombre del contacto
        for row in self.data.get_contacts():
            if row[1] == name:
                self.selected_row = row  # Almacena la fila seleccionada
                break
        self.update()  # Actualiza la interfaz

    def edit_flied_text(self, e):
        # Rellena los campos de entrada con los datos del contacto seleccionado
        try: 
            self.name.value = self.selected_row[1]
            self.age.value = self.selected_row[2]
            self.email.value = self.selected_row[3]
            self.phone.value = self.selected_row[4]   
            self.update()  # Actualiza la interfaz
        except TypeError:
            print("Error")  # Manejo de errores

    def update_data(self,e):
        # Actualiza el contacto seleccionado con nuevos datos
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value)

        # Verifica que todos los campos estén llenos
        if len(name) and len(age) and len(email) and len(phone) > 0:
            self.clean_fields()  # Limpia los campos
            self.data.update_contact(self.selected_row[0], name, age, email, phone)  # Actualiza el contacto
            self.show_data()  # Actualiza la tabla

    def delete_data(self, e):
        # Elimina el contacto seleccionado
        self.data.delete_contact(self.selected_row[1])  # Elimina el contacto
        self.show_data()  # Actualiza la tabla

    def searh_data(self, e):
        # Filtra los contactos según el texto de búsqueda
        search = self.searh_field.value.lower()
        name = list(filter(lambda x: search in x[1].lower(), self.data.get_contacts()))  # Filtra por nombre
        self.data_table.rows = []  # Limpia las filas
        if not self.searh_field.value == "":
            if len(name) > 0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,  # Maneja la selección
                            cells=[
                                ft.DataCell(ft.Text(x[1])),  # Nombre
                                ft.DataCell(ft.Text(str(x[2]))),  # Edad
                                ft.DataCell(ft.Text(x[3])),  # Correo
                                ft.DataCell(ft.Text(str(x[4]))),  # Teléfono
                            ]
                        )
                    )
                    self.update()  # Actualiza la tabla
        else:
            self.show_data()  # Si no hay búsqueda, muestra todos los datos

    def clean_fields(self):
        # Limpia los campos de entrada
        self.name.value = ""
        self.age.value = ""
        self.email.value = ""
        self.phone.value = ""      
        self.update()  # Actualiza la interfaz

    def save_pdf(self, e):
        # Guarda los contactos en un archivo PDF
        pdf = PDF()
        pdf.add_page()  # Agrega una página al PDF
        column_widths = [10,40, 20, 80, 40]  # Anchos de las columnas
        # Agregar filas a la tabla
        data = self.data.get_contacts()  # Obtiene los contactos
        header = ("ID", "NOMBRE", "EDAD", "CORREO", "TELEFONO")  # Encabezado
        data.insert(0, header)  # Agrega el encabezado a los datos
        for row in data:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)  # Crea las celdas en el PDF
            pdf.ln()  # Salto de línea
        file_name =  datetime.datetime.now()  # Crea un nombre de archivo basado en la fecha y hora
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)  # Guarda el archivo PDF

    def save_excel(self, e):
        # Guarda los contactos en un archivo Excel
        file_name =  datetime.datetime.now()  # Crea un nombre de archivo basado en la fecha y hora
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        contacts = self.data.get_contacts()  # Obtiene los contactos
        df = pd.DataFrame(contacts, columns=["ID", "Nombre", "Edad", "Correo", "Teléfono"])  # Crea un DataFrame
        df.to_excel(file_name, index=False)  # Guarda el DataFrame como un archivo Excel

    def build(self):
        # Construye la interfaz de usuario
        return self.conent

# Función principal que se ejecuta al iniciar la aplicación
def main(page: ft.Page):
    page.bgcolor = "#0e5252"  # Color de fondo principal
    page.title = "CRUD SQLite"  # Título de la ventana
    page.window_min_width = 1100  # Ancho mínimo de la ventana
    page.window_min_height = 500  # Altura mínima de la ventana
    form_ui = FormUi(page)  # Crea la instancia de la interfaz
    form_ui.data.close_connection()  # Cierra la conexión a la base de datos
    page.add(FormUi(page))  # Agrega la interfaz a la página

# Llama a la función principal para iniciar la aplicación
ft.app(main)
