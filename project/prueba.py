from tkinter import ttk
from tkinter import *
import datetime
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Servicios')
        # Crear una variable tiempo
        time = datetime.datetime.now().date()
        self.time = time

        # Creando un frame contenedor
        frame = LabelFrame(self.wind, text='Registrar cliente')
        frame.grid(row=0, column=0, columnspan=3, padx=20)

        # Ingresar datos
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        Label(frame, text='Direccion: ').grid(row=2, column=0)
        self.address = Entry(frame)
        self.address.grid(row=2, column=1)

        Label(frame, text='Telefono: ').grid(row=3, column=0)
        self.phone = Entry(frame)
        self.phone.grid(row=3, column=1)

        Label(frame, text='Correo: ').grid(row=4, column=0)
        self.mail = Entry(frame)
        self.mail.grid(row=4, column=1)

        Label(frame, text='Horario: ').grid(row=5, column=0)
        self.schedule = Entry(frame)
        self.schedule.grid(row=5, column=1)

        # Botones
        ttk.Button(frame, text='Agregar cliente', command=self.add_client).grid(row=6, columnspan=2, sticky=W + E)
        ttk.Button(frame, text='Modificar cliente', command=self.edit_client).grid(row=7, columnspan=2, sticky=W + E)
        ttk.Button(frame, text='Eliminar cliente', command=self.delete_client).grid(row=8, columnspan=2, sticky=W + E)

        # Campo de búsqueda
        Label(self.wind, text='Buscar cliente: ').grid(row=9, column=0)
        self.search_name = Entry(self.wind)
        self.search_name.grid(row=9, column=1)
        self.search_name.bind('<KeyRelease>', self.dynamic_search)  # Detectar escritura en tiempo real

        # Botón de búsqueda
        ttk.Button(self.wind, text='Buscar', command=self.search_client).grid(row=9, column=2)

        # Inserto una tabla
        self.tree = ttk.Treeview(height=10, columns=('direccion', 'telefono', 'correo', 'horario'))
        self.tree.grid(row=10, column=0, columnspan=3)

        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('direccion', text='Direccion', anchor=CENTER)
        self.tree.heading('telefono', text='Telefono', anchor=CENTER)
        self.tree.heading('correo', text='Correo', anchor=CENTER)
        self.tree.heading('horario', text='Horario', anchor=CENTER)

        self.get_clients()

        # Asociar el evento de doble clic con la función on_double_click
        self.tree.bind('<Double-1>', self.on_double_click)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_clients(self):
        # Limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener datos ordenados alfabéticamente por nombre
        query = 'SELECT * FROM clientes ORDER BY name ASC'
        db_rows = self.run_query(query)
        self.clients_list = db_rows.fetchall()  # Guardar los clientes en una lista
        for row in self.clients_list:
            self.tree.insert('', 0, text=row[0], values=row[1:])

    def validation(self):
        return len(self.name.get()) != 0

    def add_client(self):
        if self.validation():
            query = 'INSERT INTO clientes (name, address, phone, mail, shedule) VALUES (?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.address.get(), self.phone.get(), self.mail.get(), self.schedule.get())
            self.run_query(query, parameters)
            self.get_clients()
        else:
            print("Error: El nombre es obligatorio")

    def delete_client(self):
        try:
            selected_item = self.tree.selection()[0]
            name = self.tree.item(selected_item)['text']
            query = 'DELETE FROM clientes WHERE name = ?'
            self.run_query(query, (name,))
            self.get_clients()
        except IndexError:
            print("Error: No se seleccionó ningún cliente")

    def edit_client(self):
        try:
            selected_item = self.tree.selection()[0]
            name = self.tree.item(selected_item)['text']
            old_data = self.tree.item(selected_item)['values']

            # Colocar datos seleccionados en las entradas
            self.name.delete(0, END)
            self.name.insert(0, name)

            self.address.delete(0, END)
            self.address.insert(0, old_data[0])

            self.phone.delete(0, END)
            self.phone.insert(0, old_data[1])

            self.mail.delete(0, END)
            self.mail.insert(0, old_data[2])

            self.schedule.delete(0, END)
            self.schedule.insert(0, old_data[3])

            # Añadir botón de "Guardar cambios" para confirmar la actualización
            self.update_btn = ttk.Button(self.wind, text='Guardar cambios', command=lambda: self.update_client(name))
            self.update_btn.grid(row=11, columnspan=2, sticky=W + E)

        except IndexError:
            print("Error: No se seleccionó ningún cliente")

    def update_client(self, old_name):
        # Obtener los valores ingresados en los campos
        new_name = self.name.get()
        new_address = self.address.get()
        new_phone = self.phone.get()
        new_mail = self.mail.get()
        new_schedule = self.schedule.get()

        # Query base para la actualización
        query = 'UPDATE clientes SET '

        # Crear dinámicamente la query según los campos que no están vacíos
        parameters = []

        if new_name:
            query += 'name = ?, '
            parameters.append(new_name)
        if new_address:
            query += 'address = ?, '
            parameters.append(new_address)
        if new_phone:
            query += 'phone = ?, '
            parameters.append(new_phone)
        if new_mail:
            query += 'mail = ?, '
            parameters.append(new_mail)
        if new_schedule:
            query += 'shedule = ? '
            parameters.append(new_schedule)

        # Eliminar la coma final si hay campos a actualizar
        query = query.rstrip(', ')

        # Añadir la cláusula WHERE para asegurarnos de actualizar el cliente correcto
        query += 'WHERE name = ?'
        parameters.append(old_name)

        # Si hay algo que actualizar, ejecutamos la query
        if parameters:
            self.run_query(query, parameters)
            self.get_clients()
            # Eliminar el botón de "Guardar cambios" después de actualizar
            self.update_btn.grid_remove()
        else:
            print("Error: No hay campos para actualizar")

    def dynamic_search(self, event):
        search_term = self.search_name.get().lower()

        # Limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Filtrar los clientes en base al término de búsqueda
        filtered_clients = [client for client in self.clients_list if client[0].lower().startswith(search_term)]

        # Insertar los clientes filtrados en la tabla
        for client in filtered_clients:
            self.tree.insert('', 0, text=client[0], values=client[1:])

        # Seleccionar automáticamente si hay solo un resultado
        if len(filtered_clients) == 1:
            self.tree.selection_set(self.tree.get_children()[0])
            self.tree.see(self.tree.get_children()[0])

    def search_client(self):
        search_term = self.search_name.get().lower()
        found_clients = [client for client in self.clients_list if client[0].lower().startswith(search_term)]

        # Si solo hay un cliente encontrado, seleccionarlo
        if len(found_clients) == 1:
            records = self.tree.get_children()
            for element in records:
                if self.tree.item(element)['text'].lower() == found_clients[0][0].lower():
                    self.tree.selection_set(element)
                    self.tree.see(element)
                    return

        print("Cliente no encontrado")

    def save_machine_info(self, client_name, machine, model, voltage):
        # Obtener el ID del cliente basado en su nombre
        query = 'SELECT id FROM clientes WHERE name = ?'
        client_id = self.run_query(query, (client_name,)).fetchone()

        if client_id:
            # Insertar la nueva fotocopiadora en la tabla fotocopiadoras
            query = 'INSERT INTO fotocopiadoras (cliente_id, maquina, modelo, voltaje) VALUES (?, ?, ?, ?)'
            parameters = (client_id[0], machine, model, voltage)
            self.run_query(query, parameters)
            # print(f'Fotocopiadora guardada para {client_name}')
        else:
            print(f'Cliente {client_name} no encontrado')

    def on_double_click(self, event):
        # Obtener el cliente seleccionado
        selected_item = self.tree.selection()[0]
        selected_client = self.tree.item(selected_item)['text']

        # Mostrar detalles del cliente
        # print(f'Detalles del cliente: {selected_client}')
        
        # Llamar a la ventana o formulario para mostrar las máquinas
        self.show_machine_form(selected_client)

    def show_machine_form(self, client_name):
        # Crear una nueva ventana para ingresar y mostrar detalles de la máquina
        machine_window = Toplevel(self.wind)
        machine_window.title(f'Fotocopiadoras para {client_name}')

        # Crear un Treeview para mostrar las fotocopiadoras existentes
        machine_tree = ttk.Treeview(machine_window, columns=('modelo', 'voltaje', 'numero_serie'), height=10)
        machine_tree.grid(row=0, column=0, columnspan=4)

        machine_tree.heading('#0', text='Máquina', anchor=CENTER)
        machine_tree.heading('modelo', text='Modelo', anchor=CENTER)
        machine_tree.heading('voltaje', text='Voltaje', anchor=CENTER)
        machine_tree.heading('numero_serie', text='Número de Serie', anchor=CENTER)

        # Obtener las fotocopiadoras del cliente
        self.populate_machine_tree(client_name, machine_tree)

        # Vincular el evento de doble clic a la función on_double_click_machine
        machine_tree.bind('<Double-1>', lambda event: self.on_double_click_machine(client_name, machine_tree))

        # Campos para añadir nueva fotocopiadora
        Label(machine_window, text='Máquina: ').grid(row=1, column=0)
        machine = Entry(machine_window)
        machine.grid(row=1, column=1)

        Label(machine_window, text='Modelo: ').grid(row=2, column=0)
        model = Entry(machine_window)
        model.grid(row=2, column=1)

        Label(machine_window, text='Voltaje: ').grid(row=3, column=0)
        voltage = Entry(machine_window)
        voltage.grid(row=3, column=1)

        Label(machine_window, text='Número de Serie: ').grid(row=4, column=0)
        serial_number = Entry(machine_window)
        serial_number.grid(row=4, column=1)

        # Botón para guardar los datos de la máquina
        Button(machine_window, text='Guardar', command=lambda: self.save_machine_info(client_name, machine.get(), model.get(), voltage.get(), serial_number.get(), machine_tree)).grid(row=5, columnspan=2, sticky=W + E)

        # Botón para modificar el equipo seleccionado
        Button(machine_window, text='Modificar', command=lambda: self.modify_machine(machine_tree, client_name)).grid(row=6, column=0, sticky=W + E)

        # Botón para eliminar el equipo seleccionado
        Button(machine_window, text='Eliminar', command=lambda: self.delete_machine(machine_tree, client_name)).grid(row=6, column=1, sticky=W + E)


    def modify_machine(self, machine_tree, client_name):
        try:
            # Obtener el equipo seleccionado
            selected_item = machine_tree.selection()[0]
            selected_machine = machine_tree.item(selected_item, 'text')
            selected_model = machine_tree.item(selected_item, 'values')[0]
            selected_voltage = machine_tree.item(selected_item, 'values')[1]
            selected_serial = machine_tree.item(selected_item, 'values')[2]  # Número de serie

            # Crear una nueva ventana para modificar los detalles de la máquina
            modify_window = Toplevel(self.wind)
            modify_window.title(f'Modificar {selected_machine}')

            Label(modify_window, text='Máquina: ').grid(row=0, column=0)
            machine_entry = Entry(modify_window)
            machine_entry.insert(0, selected_machine)
            machine_entry.grid(row=0, column=1)

            Label(modify_window, text='Modelo: ').grid(row=1, column=0)
            model_entry = Entry(modify_window)
            model_entry.insert(0, selected_model)
            model_entry.grid(row=1, column=1)

            Label(modify_window, text='Voltaje: ').grid(row=2, column=0)
            voltage_entry = Entry(modify_window)
            voltage_entry.insert(0, selected_voltage)
            voltage_entry.grid(row=2, column=1)

            Label(modify_window, text='Número de Serie: ').grid(row=3, column=0)
            serial_entry = Entry(modify_window)
            serial_entry.insert(0, selected_serial)
            serial_entry.grid(row=3, column=1)

            # Botón para guardar los cambios
            Button(modify_window, text='Guardar cambios', command=lambda: self.update_machine(client_name, selected_serial, machine_entry.get(), model_entry.get(), voltage_entry.get(), serial_entry.get(), machine_tree, modify_window)).grid(row=4, columnspan=2, sticky=W + E)

        except IndexError:
            print("Error: No se seleccionó ningún equipo para modificar")



    def update_machine(self, client_name, old_serial, new_machine, new_model, new_voltage, new_serial, machine_tree, modify_window):
        # Obtener el ID del cliente basado en su nombre
        query = 'SELECT id FROM clientes WHERE name = ?'
        client_id = self.run_query(query, (client_name,)).fetchone()

        if client_id:
            # Actualizar la información de la fotocopiadora en la base de datos usando el número de serie como identificador único
            query = 'UPDATE fotocopiadoras SET maquina = ?, modelo = ?, voltaje = ?, numero_serie = ? WHERE cliente_id = ? AND numero_serie = ?'
            parameters = (new_machine, new_model, new_voltage, new_serial, client_id[0], old_serial)
            self.run_query(query, parameters)

            # Actualizar el Treeview en tiempo real
            self.populate_machine_tree(client_name, machine_tree)

            # Cerrar la ventana de modificación
            modify_window.destroy()

            # print(f'Fotocopiadora actualizada para {client_name}')
        else:
            print(f'Cliente {client_name} no encontrado')



    def delete_machine(self, machine_tree, client_name):
        try:
            # Obtener el equipo seleccionado
            selected_item = machine_tree.selection()[0]
            selected_serial = machine_tree.item(selected_item, 'values')[2]  # Número de serie

            # Obtener el ID del cliente basado en su nombre
            query = 'SELECT id FROM clientes WHERE name = ?'
            client_id = self.run_query(query, (client_name,)).fetchone()

            if client_id:
                # Eliminar el equipo basado en el número de serie
                query = 'DELETE FROM fotocopiadoras WHERE cliente_id = ? AND numero_serie = ?'
                self.run_query(query, (client_id[0], selected_serial))

                # Actualizar el Treeview en tiempo real
                self.populate_machine_tree(client_name, machine_tree)

                # print(f'Equipo con número de serie {selected_serial} eliminado para {client_name}')
            else:
                print(f'Cliente {client_name} no encontrado')

        except IndexError:
            print("Error: No se seleccionó ningún equipo para eliminar")


    def populate_machine_tree(self, client_name, machine_tree):
        # Limpiar la tabla
        records = machine_tree.get_children()
        for element in records:
            machine_tree.delete(element)

        # Obtener el ID del cliente basado en su nombre
        query = 'SELECT id FROM clientes WHERE name = ?'
        client_id = self.run_query(query, (client_name,)).fetchone()

        if client_id:
            # Obtener los equipos de ese cliente
            query = 'SELECT maquina, modelo, voltaje, numero_serie FROM fotocopiadoras WHERE cliente_id = ?'
            machines = self.run_query(query, (client_id[0],))

            for machine in machines:
                machine_tree.insert('', 'end', text=machine[0], values=(machine[1], machine[2], machine[3]))


    def save_machine_info(self, client_name, machine, model, voltage, serial_number, machine_tree):
        # Obtener el ID del cliente basado en su nombre
        query = 'SELECT id FROM clientes WHERE name = ?'
        client_id = self.run_query(query, (client_name,)).fetchone()

        if client_id:
            # Insertar la nueva fotocopiadora en la tabla fotocopiadoras
            query = 'INSERT INTO fotocopiadoras (cliente_id, maquina, modelo, voltaje, numero_serie) VALUES (?, ?, ?, ?, ?)'
            parameters = (client_id[0], machine, model, voltage, serial_number)
            self.run_query(query, parameters)

            # Actualizar el Treeview en tiempo real
            self.populate_machine_tree(client_name, machine_tree)

            # print(f'Fotocopiadora guardada para {client_name}')
        else:
            print(f'Cliente {client_name} no encontrado')

    def on_double_click_machine(self, client_name, machine_tree):
        try:
            # Verificar si hay un elemento seleccionado
            selected_items = machine_tree.selection()
            if not selected_items:
                print("Error: No se seleccionó ninguna fotocopiadora para ver los servicios")
                return

            # Obtener el equipo seleccionado
            selected_item = selected_items[0]
            selected_values = machine_tree.item(selected_item, 'values')
            
            print(f"Valores seleccionados: {selected_values}")

            if len(selected_values) < 3:
                print("Error: El equipo seleccionado no tiene suficientes columnas de datos.")
                return

            selected_serial = selected_values[2]  # Número de serie
            print(f"Selected serial: {selected_serial}")

            # Crear una nueva ventana para mostrar el historial de servicios
            service_window = Toplevel(self.wind)
            service_window.title(f'Servicios para la fotocopiadora con número de serie {selected_serial}')

            # Mostrar el historial de servicios en una tabla
            service_tree = ttk.Treeview(service_window, columns=('fecha', 'cambio_toner', 'cambio_ur_dr', 'cambio_fusor', 'contador', 'trabajo_realizado', 'observaciones'), show='headings')
            service_tree.grid(row=0, column=0, columnspan=2)

            service_tree.heading('fecha', text='Fecha', anchor=CENTER)
            service_tree.heading('cambio_toner', text='Cambio Tóner', anchor=CENTER)
            service_tree.heading('cambio_ur_dr', text='Cambio UR/DR', anchor=CENTER)
            service_tree.heading('cambio_fusor', text='Cambio Fusor', anchor=CENTER)
            service_tree.heading('contador', text='Contador', anchor=CENTER)
            service_tree.heading('trabajo_realizado', text='Trabajo Realizado', anchor=CENTER)
            service_tree.heading('observaciones', text='Observaciones', anchor=CENTER)

            # Llenar la tabla con el historial de servicios
            self.populate_service_tree(selected_serial, service_tree)

            # Botón para agregar un pedido de servicio
            Button(service_window, text='Agregar Pedido de Servicio', command=lambda: self.open_service_request_window(client_name, selected_serial)).grid(row=1, columnspan=2, sticky=W + E)

        except Exception as e:
            print(f"Error inesperado: {e}")
    def open_service_request_window(self, client_name, serial):
        # Crear una ventana para ingresar el pedido de servicio
        request_window = Toplevel(self.wind)
        request_window.title(f'Agregar Pedido de Servicio para {client_name}')

        # Etiqueta y entrada para el problema manifestado
        Label(request_window, text='Problema Manifestado:').grid(row=0, column=0)
        problem_entry = Text(request_window, height=4, width=30)
        problem_entry.grid(row=0, column=1)

        # Botón para guardar el pedido de servicio
        Button(request_window, text='Guardar Pedido', command=lambda: self.save_service_request(
            client_name, serial, problem_entry.get("1.0", "end-1c"), request_window)).grid(row=1, columnspan=2, sticky=W + E)
    
    def save_service_request(self, client_name, serial, problem_description, request_window):
        try:
            # Consulta para obtener la dirección, modelo y voltaje del equipo desde la base de datos
            query = "SELECT direccion, modelo, voltaje FROM equipos WHERE serial = ?"
            parameters = (serial,)
            result = self.run_query(query, parameters)

            if result:
                # Obtener la dirección, modelo y voltaje del primer resultado de la consulta
                direccion, modelo, voltaje = result[0]

                # Crear el nombre del archivo
                filename = f"{client_name}_pedido_servicio.txt"

                # Escribir la información en el archivo
                with open(filename, "w") as file:
                    file.write(f"Cliente: {client_name}\n")
                    file.write(f"Dirección: {direccion}\n")
                    file.write(f"Modelo del Equipo: {modelo}\n")
                    file.write(f"Voltaje: {voltaje}\n")
                    file.write(f"Problema Manifestado: {problem_description}\n")
                    file.write("Trabajo Realizado: \n")

                # Mostrar un mensaje de éxito
                print(f"Pedido de servicio guardado en el archivo {filename}")

                # Cerrar la ventana de pedido de servicio
                request_window.destroy()
            else:
                print(f"No se encontró información para el número de serie {serial}")
                request_window.destroy()

        except Exception as e:
            print(f"Error al guardar el pedido de servicio: {e}")

        
    def populate_service_tree(self, serial, service_tree):
    # Limpiar la tabla antes de llenarla
        for item in service_tree.get_children():
            service_tree.delete(item)

        try:
            # Supongamos que tienes una base de datos SQLite y una tabla llamada "servicios"
            query = "SELECT fecha_servicio, cambio_toner, cambio_ur_dr, cambio_fusor, contador, trabajo_realizado, observaciones FROM servicios WHERE numero_serie = ?"
            parameters = (serial,)

            # Ejecutar la consulta y obtener los datos
            rows = self.run_query(query, parameters)

            # Insertar los datos en la tabla
            for row in rows:
                service_tree.insert('', 'end', values=row)

        except Exception as e:
            print(f"Error al llenar la tabla de servicios: {e}")
    
    
    def delete_service_info(self, serial, service_tree):
        try:
            # Obtener el servicio seleccionado
            selected_item = service_tree.selection()[0]
            selected_date = service_tree.item(selected_item, 'values')[0]  # Fecha del servicio

            # Consulta SQL para eliminar el servicio
            query = "DELETE FROM servicios WHERE numero_serie = ? AND fecha_servicio = ?"
            parameters = (serial, selected_date)

            # Ejecutar la consulta para eliminar los datos
            self.run_query(query, parameters)

            # Mostrar un mensaje de éxito
            # print(f"Servicio eliminado exitosamente para el equipo con número de serie {serial}")

            # Actualizar la tabla de servicios en la interfaz de usuario
            self.populate_service_tree(serial, service_tree)

        except IndexError:
            print("Error: No se seleccionó ningún servicio para eliminar")
        except Exception as e:
            print(f"Error al eliminar el servicio: {e}")

    def add_service_request(self, client_name, serial):
        if not serial:
            print("Error: No se puede agregar un pedido de servicio sin un número de serie válido.")
            return

        print(f"Adding service request for serial: {serial}")  # Debug: verificar número de serie antes de abrir la ventana

        # Crear una ventana para ingresar el pedido de servicio
        request_window = Toplevel(self.wind)
        request_window.title(f'Agregar Pedido de Servicio para {client_name}')
        print(f"Adding service request for serial: {serial}")  # Debug: verificar número de serie antes de abrir la ventana

        if not serial:
            print("Error: No se puede agregar un pedido de servicio sin un número de serie válido.")
            return

        # Crear una ventana para ingresar el pedido de servicio
        request_window = Toplevel(self.wind)
        request_window.title(f'Agregar Pedido de Servicio para {client_name}')

        # Etiqueta y entrada para el problema manifestado
        Label(request_window, text='Problema Manifestado:').grid(row=0, column=0)
        problem_entry = Text(request_window, height=4, width=30)
        problem_entry.grid(row=0, column=1)

        # Botón para guardar el pedido de servicio
        Button(request_window, text='Guardar Pedido', command=lambda: self.save_service_request(
            client_name, serial, problem_entry.get("1.0", "end-1c"), request_window)).grid(row=1, columnspan=2, sticky=W + E)

    # def save_service_request(self, client_name, serial, problem_description, request_window):
    #     if not serial:
    #         print("Error: Número de serie no válido. No se puede guardar el pedido de servicio.")
    #         request_window.destroy()
    #         return

    #     print(f"Saving service request for serial: {serial}")  # Debug: verificar número de serie en save_service_request

    #     try:
    #         # Consulta para obtener información del cliente y del equipo
    #         query = "SELECT direccion, modelo FROM equipos WHERE serial = ?"
    #         parameters = (serial,)
    #         cursor = self.run_query(query, parameters)

    #         result = cursor.fetchone()  # Obtiene el primer resultado de la consulta

    #         if result:
    #             direccion, modelo = result  # Desempaqueta la tupla resultante

    #             # Crear el nombre del archivo
    #             filename = f"{client_name}_pedido_servicio.txt"

    #             # Escribir la información en el archivo
    #             with open(filename, "w") as file:
    #                 file.write(f"Cliente: {client_name}\n")
    #                 file.write(f"Dirección: {direccion}\n")
    #                 file.write(f"Modelo del Equipo: {modelo}\n")
    #                 file.write(f"Problema Manifestado: {problem_description}\n")

    #             print(f"Pedido de servicio guardado en el archivo {filename}")
    #             request_window.destroy()
    #         else:
    #             print(f"No se encontró información para el número de serie {serial}")
    #             request_window.destroy()

    #     except Exception as e:
    #         print(f"Error al guardar el pedido de servicio: {e}")


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
