import sqlite3  # Importa el módulo sqlite3 para manejar bases de datos SQLite.

class ContactManager:
    def __init__(self):
        # Inicializa la conexión a la base de datos 'data.db'.
        # El parámetro check_same_thread=False permite que la conexión sea utilizada desde diferentes hilos.
        self.connection = sqlite3.connect("data.db", check_same_thread=False)

    def add_contact(self, name, age, email, phone):
        # Agrega un nuevo contacto a la base de datos.
        query = '''INSERT INTO datos (NOMBRE, EDAD, CORREO, TELEFONO) 
                   VALUES (?, ?, ?, ?)'''  # Consulta SQL para insertar datos.
        self.connection.execute(query, (name, age, email, phone))  # Ejecuta la consulta con los valores proporcionados.
        self.connection.commit()  # Guarda los cambios en la base de datos.

    def get_contacts(self):
        # Recupera todos los contactos de la base de datos.
        cursor = self.connection.cursor()  # Crea un cursor para ejecutar consultas.
        query = "SELECT * FROM datos"  # Consulta SQL para seleccionar todos los registros.
        cursor.execute(query)  # Ejecuta la consulta.
        contacts = cursor.fetchall()  # Obtiene todos los resultados de la consulta.
        return contacts  # Retorna la lista de contactos.

    def delete_contact(self, name):
        # Elimina un contacto de la base de datos por su nombre.
        query = "DELETE FROM datos WHERE NOMBRE = ?"  # Consulta SQL para eliminar un registro.
        self.connection.execute(query, (name,))  # Ejecuta la consulta con el nombre proporcionado.
        self.connection.commit()  # Guarda los cambios en la base de datos.

    def update_contact(self, contact_id, name, age, email, phone):
        # Actualiza un contacto existente en la base de datos.
        query = '''UPDATE datos SET NOMBRE = ?, EDAD = ?, CORREO = ?, TELEFONO = ?
                   WHERE ID = ?'''  # Consulta SQL para actualizar un registro.
        self.connection.execute(query, (name, age, email, phone, contact_id))  # Ejecuta la consulta con los nuevos valores.
        self.connection.commit()  # Guarda los cambios en la base de datos.
        #return self.connection.total_changes  # Opcional: retorna el número total de cambios realizados.

    def close_connection(self):
        # Cierra la conexión a la base de datos.
        self.connection.close()  # Cierra la conexión.
        print("cerrar")  # Imprime un mensaje de cierre.
