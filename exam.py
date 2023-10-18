import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk
import re
import os

ventana_registro = None  # Variable global para la ventana de registro
ventana_inicio = None  # Variable global para la ventana de inicio de sesión
ventana_plataforma = None  # Variable global para la ventana de la plataforma
nombre_de_usuario_actual = "" # Variable de usuario
ventana_formulario = None

# ------------------------------------Cargar a los usuarios en el archivo txt------------------------------------
def cargar_usuarios():
    usuarios = {}
    try:
        with open("DATA/usuarios.txt", "r") as file:
            for line in file:
                if ":" in line:
                    nombre_apellido, dpi, telefono, usuario, contrasena = line.strip().split(":")
                    usuarios[usuario] = contrasena
    except FileNotFoundError:
        pass
    return usuarios
# ----------------------------------Proceso de Registro---------------------------------------------
def registrar_usuario(ventana_registro):
    global nombre_entry, apellido_entry, dpi_entry, telefono_entry, usuario_entry, email_entry, contrasena_entry, confirmar_contrasena_entry
    usuarios = cargar_usuarios()
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dpi = dpi_entry.get()
    telefono = telefono_entry.get()
    usuario = usuario_entry.get()
    email = email_entry.get()
    contrasena = contrasena_entry.get()
    confirmar_contrasena = confirmar_contrasena_entry.get()

    for usuario_guardado, datos in usuarios.items():
        nombre_apellido_guardado, *_ = datos.split(",")
        if nombre + apellido == nombre_apellido_guardado:
            messagebox.showerror("Error", "Nombre y Apellido ya están registrados.")
            return

    if not re.match(r"^\d{13}$", dpi):
        messagebox.showerror("Error", "El DPI debe contener 13 dígitos numéricos.")
        return

    if not re.match(r"^\d{8}$", telefono):
        messagebox.showerror("Error", "El Teléfono debe contener 8 dígitos numéricos.")
        return

    if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!?)(@#$%^/&+-=])", contrasena):
        messagebox.showerror("Error", "La contraseña no cumple con los requisitos.")
        return

    if contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
    else:
        with open("DATA/usuarios.txt", "a") as file:
            file.write(f"{nombre + apellido}:{dpi}:{telefono}:{usuario}:{contrasena}\n")
        messagebox.showinfo("Registro Exitoso", "Registro exitoso.")
        # Cierra la ventana de registro
        if ventana_registro:
            ventana_registro.destroy()

# ---------------------------Datos del Administrador------------------------------------
def cargar_administrador():
    administrador = {}
    try:
        with open("DATA/administrador.txt", "r") as file:
            for line in file:
                usuario, contrasena = line.strip().split(":")
                administrador[usuario] = contrasena
    except FileNotFoundError:
        pass
    return administrador

#----------------------------------------Ventana de Plataforma---------------------------------------------------------
def abrir_ventana_plataforma():
    global ventana_plataforma, ventana_inicio

    if ventana_plataforma is not None:
        ventana_plataforma.destroy()  # Cerrar la ventana existente si ya está abierta

    ventana_plataforma = tk.Toplevel()
    ventana_plataforma.title("Plataforma")
    ventana_plataforma.geometry("600x600")

    frame_superior = tk.Frame(ventana_plataforma, bg="#2980B9")  # Frame para el botón
    frame_superior.pack(fill="x")

    cerrar_sesion_button = tk.Button(frame_superior, text="Cerrar Sesión", command=confirmar_cerrar_sesion)  # Botón arriba del Frame
    cerrar_sesion_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    contenido_principal = tk.Label(ventana_plataforma, text="")  # Texto arriba del frame
    contenido_principal.pack()

    usuario_info = tk.Label(ventana_plataforma, text="Bienvenido, " + nombre_de_usuario_actual)  # Mostrar Usuario
    usuario_info.place(relx=1.0, rely=0.0, anchor="ne", x=-30, y=10)

    # Agregar un botón en la parte inferior de la ventana
    boton_abajo = tk.Button(ventana_plataforma, text="Seleccionar Curso", font=("Arial", 20), command=abrir_ventana_cursos)
    boton_abajo.pack(side="bottom", pady=20)
    # Botón "Mis cursos"
    boton_mis_cursos = tk.Button(ventana_plataforma, text="Mis cursos", command=mostrar_mis_cursos)
    boton_mis_cursos.pack()
#-------------------------------Cursos-----------------------------------
def cursos_asignados():
    cursos_asignados = {}
    with open("Cursos/cursos.txt", "r") as archivo_cursos:
        for linea in archivo_cursos:
            partes = linea.strip().split(":")
            if len(partes) >= 2:
                nombre_usuario = partes[0]
                cursos = partes[1].split(",")  # Suponemos que los cursos están separados por comas
                cursos_asignados[nombre_usuario] = cursos
    return cursos_asignados

def abrir_ventana_cursos():
    ventana_cursos = tk.Toplevel()
    ventana_cursos.title("Selección de Curso")
    ventana_cursos.geometry("200x400")
    ventana_cursos.resizable(0,0)

 # Leer la lista de cursos desde el archivo "Cursos.txt"
    with open("Cursos/cursos.txt", "r") as archivo_cursos:
        lista_cursos = [line.strip() for line in archivo_cursos]
#----------------------------------------------Listado de los Cursos----------------------------------
    def seleccionar_curso():
        curso_seleccionado = lista_cursos_listbox.get(tk.ACTIVE)
        ventana_cursos.destroy()
        abrir_formulario(curso_seleccionado)

    lista_cursos_listbox = tk.Listbox(ventana_cursos)
    for curso in lista_cursos:
        lista_cursos_listbox.insert(tk.END, curso)
    lista_cursos_listbox.pack(padx=20, pady=20)

    seleccionar_button = tk.Button(ventana_cursos, text="Seleccionar Curso", command=seleccionar_curso)
    seleccionar_button.pack(pady=10)
    # Botón "Mis cursos" 
    boton_mis_cursos = tk.Button(ventana_plataforma, text="Mis cursos", command=mostrar_mis_cursos)
    boton_mis_cursos.pack()

# Función para mostrar los cursos asignados al usuario actual
def mostrar_mis_cursos():
    cursos_del_usuario = cursos_asignados.get(nombre_de_usuario_actual, [])

    if cursos_del_usuario:
        ventana_mis_cursos = tk.Toplevel()
        ventana_mis_cursos.title("Mis Cursos")

        cursos_label = tk.Label(ventana_mis_cursos, text="Cursos Asignados:")
        cursos_label.pack()

        for curso in cursos_del_usuario:
            curso_label = tk.Label(ventana_mis_cursos, text=curso)
            curso_label.pack()

    else:
        messagebox.showinfo("Mis Cursos", "No tienes cursos asignados.")

def abrir_formulario(curso_seleccionado):
    ventana_formulario = tk.Toplevel()
    ventana_formulario.title(f"Formulario de Inscripción - {curso_seleccionado}")
    ventana_formulario.geometry("300x300")
    ventana_formulario.resizable(0,0)

    nombre_label = tk.Label(ventana_formulario, text="Nombre:")
    nombre_label.pack()
    nombre_entry = tk.Entry(ventana_formulario)
    nombre_entry.pack()

    apellido_label = tk.Label(ventana_formulario, text="Apellido:")
    apellido_label.pack()
    apellido_entry = tk.Entry(ventana_formulario)
    apellido_entry.pack()

    nov_label = tk.Label(ventana_formulario, text="NOV:")
    nov_label.pack()
    nov_entry = tk.Entry(ventana_formulario)
    nov_entry.pack()

    def guardar_datos():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        nov = nov_entry.get()

        if nombre and apellido and nov:
            with open("Cursos/asignación.txt", "a") as archivo:
                archivo.write(f"Nombre: {nombre}, Apellido: {apellido}, NOV: {nov}\n")
            ventana_formulario.destroy()

    guardar_button = tk.Button(ventana_formulario, text="Guardar Datos", command=guardar_datos)
    guardar_button.pack(pady=10)

def confirmar_cerrar_sesion():
    # Mostrar un cuadro de diálogo de confirmación
    respuesta = messagebox.askyesno("Cerrar Sesión", "¿Quieres cerrar sesión?")

    if respuesta:
        # Cerrar sesión
        if ventana_plataforma:
            ventana_plataforma.destroy()

nombre_de_usuario_actual = "Usuario Actual"  # Solo para fines de demostración

# --------------------------Procesar el inicio de sesion de un usuario--------------------------------------
def iniciar_sesion_usuario():
    global ventana_inicio, nombre_de_usuario_actual 
    usuarios = cargar_usuarios()
    usuario = usuario_inicio.get()
    contrasena = contrasena_inicio.get()

    if usuario in usuarios and usuarios[usuario] == contrasena:
        global nombre_de_usuario_actual
        nombre_de_usuario_actual = usuario
        messagebox.showinfo("Inicio de Sesión Exitoso", "Inicio de sesión exitoso.")
        abrir_ventana_plataforma() 
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
#------------------------------------Ventana de administración-----------------------------------
def abrir_ventana_administracion():
    ventana_administracion = tk.Toplevel(ventana)
    ventana_administracion.title("Administración")
    ventana_administracion.geometry("300x400")
    ventana_administracion.configure(bg="#F2F3F4")  # Color
    ventana_administracion.resizable(0,0) # No permitir cambiar tamaño
    #Cargar la Imagen
    imagen_administracion = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/Ingeniero.png")
    imagen_administracion = imagen_administracion.resize((200, 200))
    imagen_administracion = ImageTk.PhotoImage(imagen_administracion)
    imagen_administracion_label = tk.Label(ventana_administracion, image=imagen_administracion)
    imagen_administracion_label.image = imagen_administracion
    imagen_administracion_label.pack()
    # Agregar un botón para "Nuevo Curso"
    boton_nuevo_curso = tk.Button(ventana_administracion, text="Nuevo Curso", command=crear_nuevo_curso)
    boton_nuevo_curso.pack()

    # Agregar un botón para "Editar Curso"
    boton_editar_curso = tk.Button(ventana_administracion, text="Editar Curso", command=editar_curso)
    boton_editar_curso.pack()

    # Agregar un botón para "Eliminar Curso"
    boton_eliminar_curso = tk.Button(ventana_administracion, text="Eliminar Curso", command=eliminar_curso)
    boton_eliminar_curso.pack()

    # Agregar un botón para "Nuevo Profesor"
    boton_nuevo_profesor = tk.Button(ventana_administracion, text="Nuevo Profesor", command=agregar_profesor)
    boton_nuevo_profesor.pack()

    # Agregar un botón para "Desbloquear Contraseñas"
    boton_desbloquear_contrasenas = tk.Button(ventana_administracion, text="Desbloquear Contraseñas", command=ver_solicitudes_desbloqueo)
    boton_desbloquear_contrasenas.pack()
    
    ventana_administracion.mainloop
# --------------------------------------------------Crear Curso--------------------------------------------------
def crear_nuevo_curso():
    # Crear una ventana para el formulario de nuevo curso
    ventana_curso = tk.Toplevel()
    ventana_curso.title("Nuevo Curso")
    ventana_curso.geometry("200x450")
    ventana_curso.configure(bg="#E5E7E9")  # Color
    ventana_curso.resizable(0,0) # No permitir cambiar tamaño
    #Cargar la Imagen
    imagen_curso = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/curso.png")
    imagen_curso = imagen_curso.resize((200, 200))
    imagen_curso = ImageTk.PhotoImage(imagen_curso)
    imagen_curso_label = tk.Label(ventana_curso, image=imagen_curso)
    imagen_curso_label.image = imagen_curso
    imagen_curso_label.pack()
    # Crear etiquetas y campos de entrada para ingresar información del curso
    etiqueta_costo = tk.Label(ventana_curso, text="Costo:")
    etiqueta_costo.pack()
    costo_entry = tk.Entry(ventana_curso)
    costo_entry.pack()
    
    etiqueta_horario = tk.Label(ventana_curso, text="Horario:")
    etiqueta_horario.pack()
    horario_entry = tk.Entry(ventana_curso)
    horario_entry.pack()
    
    etiqueta_codigo = tk.Label(ventana_curso, text="Código:")
    etiqueta_codigo.pack()
    codigo_entry = tk.Entry(ventana_curso)
    codigo_entry.pack()
    
    etiqueta_cupo = tk.Label(ventana_curso, text="Cupo:")
    etiqueta_cupo.pack()
    cupo_entry = tk.Entry(ventana_curso)
    cupo_entry.pack()
    
    etiqueta_catedratico = tk.Label(ventana_curso, text="Catedrático:")
    etiqueta_catedratico.pack()
    catedratico_entry = tk.Entry(ventana_curso)
    catedratico_entry.pack()
    
    # Función para guardar la información del curso en el archivo "Cursos"
    def guardar_curso():
        costo = costo_entry.get()
        horario = horario_entry.get()
        codigo = codigo_entry.get()
        cupo = cupo_entry.get()
        catedratico = catedratico_entry.get()
        
        # Validar que todos los campos estén llenos
        if not costo or not horario or not codigo or not cupo or not catedratico:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        # Guardar la información en el archivo "Cursos"
        with open("Cursos/cursos.txt", "a") as file:
            file.write(f"{codigo}:{costo}:{horario}:{cupo}:{catedratico}\n")
        
        messagebox.showinfo("Curso Creado", "El curso ha sido creado y guardado.")
        ventana_curso.destroy()
    
    # Agregar un botón para guardar el curso
    boton_guardar_curso = tk.Button(ventana_curso, text="Guardar Curso", command=guardar_curso)
    boton_guardar_curso.pack()
# ------------------------------------------------------Agregar un Profesor------------------------------------------
def agregar_profesor():
    # Crear una ventana para el formulario de nuevo profesor
    ventana_profesor = tk.Toplevel()
    ventana_profesor.title("Nuevo Profesor")
    ventana_profesor.geometry("200x500")
    ventana_profesor.configure(bg="#E5E7E9")  # Color
    ventana_profesor.resizable(0,0) # No permitir cambiar tamaño
    #Cargar la Imagen
    imagen_profesor = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/curso.png")
    imagen_profesor = imagen_profesor.resize((200, 200))
    imagen_profesor = ImageTk.PhotoImage(imagen_profesor)
    imagen_profesor_label = tk.Label(ventana_profesor, image=imagen_profesor)
    imagen_profesor_label.image = imagen_profesor
    imagen_profesor_label.pack()

    # Crear etiquetas y campos de entrada para ingresar información del profesor
    etiqueta_nombre = tk.Label(ventana_profesor, text="Nombre:")
    etiqueta_nombre.pack()
    nombre_entry = tk.Entry(ventana_profesor)
    nombre_entry.pack()

    etiqueta_apellido = tk.Label(ventana_profesor, text="Apellido:")
    etiqueta_apellido.pack()
    apellido_entry = tk.Entry(ventana_profesor)
    apellido_entry.pack()

    etiqueta_dpi = tk.Label(ventana_profesor, text="DPI:")
    etiqueta_dpi.pack()
    dpi_entry = tk.Entry(ventana_profesor)
    dpi_entry.pack()

    etiqueta_contrasena = tk.Label(ventana_profesor, text="Contraseña:")
    etiqueta_contrasena.pack()
    contrasena_entry = tk.Entry(ventana_profesor, show="*")
    contrasena_entry.pack()

    etiqueta_confirmar_contrasena = tk.Label(ventana_profesor, text="Confirmar Contraseña:")
    etiqueta_confirmar_contrasena.pack()
    confirmar_contrasena_entry = tk.Entry(ventana_profesor, show="*")
    confirmar_contrasena_entry.pack()

    # Función para registrar al nuevo profesor
    def registrar_profesor():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        dpi = dpi_entry.get()
        contrasena = contrasena_entry.get()
        confirmar_contrasena = confirmar_contrasena_entry.get()

        # Validaciones similares a las del registro de estudiantes
        if not nombre or not apellido or not dpi or not contrasena or not confirmar_contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not re.match(r"^\d{13}$", dpi):
            messagebox.showerror("Error", "El DPI debe contener 13 dígitos numéricos.")
            return

        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!?)(@#$%^/&+-=])", contrasena):
            messagebox.showerror("Error", "La contraseña no cumple con los requisitos.")
            return

        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
        else:
            with open("DATA/profesores.txt", "a") as file:
                file.write(f"{nombre} {apellido}:{dpi}:{contrasena}\n")
            messagebox.showinfo("Registro Exitoso", "Registro exitoso.")
            ventana_profesor.destroy()

    # Agregar un botón para registrar al profesor
    boton_registrar_profesor = tk.Button(ventana_profesor, text="Registrar Profesor", command=registrar_profesor)
    boton_registrar_profesor.pack()
# -------------------------------Ver las solicitudes y seleccione una para desbloquear--------------------------------
def ver_solicitudes_desbloqueo():
    # Leer y mostrar las solicitudes disponibles
    solicitudes = []
    with open("Cursos/solicitud.txt", "r") as file:
        solicitud_actual = None
        for line in file:
            if line.startswith("Solicitud de "):
                solicitud_actual = {"usuario": line[12:].strip(), "mensaje": ""}
            elif solicitud_actual is not None:
                solicitud_actual["mensaje"] += line
            elif line.strip() == "":
                solicitudes.append(solicitud_actual)
    
    print("Solicitudes de desbloqueo disponibles:")
    for i, solicitud in enumerate(solicitudes):
        print(f"{i+1}. De: {solicitud['usuario']}")

    if not solicitudes:
        print("No hay solicitudes disponibles.")
        return

    # Administrador selecciona una solicitud para desbloquear
    seleccion = input("Seleccione el número de solicitud para desbloquear (o 'q' para salir): ")
    if seleccion == 'q':
        return

    try:
        seleccion = int(seleccion)
        if 1 <= seleccion <= len(solicitudes):
            solicitud_seleccionada = solicitudes[seleccion - 1]
            print(f"Mensaje de {solicitud_seleccionada['usuario']}:\n{solicitud_seleccionada['mensaje']}")
            accion = input("¿Desea desbloquear la cuenta de este estudiante? (Sí/No): ").lower()
            if accion == 'si':
                # Implementar la lógica para desbloquear la cuenta del estudiante aquí
                print(f"La cuenta de {solicitud_seleccionada['usuario']} ha sido desbloqueada.")
                # Opción para eliminar la solicitud de desbloqueo del archivo
        else:
            print("Selección no válida.")
    except ValueError:
        print("Selección no válida.")
# ----------------------------------Editar Cursos------------------------------------
def editar_curso():
    # Mostrar la lista de cursos y permitir la edición
    ventana_edicion_curso = tk.Toplevel()
    ventana_edicion_curso.title("Editar Curso")
    ventana_edicion_curso.geometry("200x500")

    # Crear una lista de cursos a partir del archivo "cursos.txt"
    cursos = []
    try:
        with open("Cursos/cursos.txt", "r") as file:
            for line in file:
                codigo, costo, horario, cupo, catedratico = line.strip().split(":")
                cursos.append((codigo, costo, horario, cupo, catedratico))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de cursos.")

    # Función para guardar los cambios en el archivo "cursos.txt"
    def guardar_cambios():
        # Guardar los cursos editados en el archivo "cursos.txt"
        with open("Cursos/cursos.txt", "w") as file:
            for curso in cursos:
                codigo, costo, horario, cupo, catedratico = curso
                file.write(f"{codigo}:{costo}:{horario}:{cupo}:{catedratico}\n")
        messagebox.showinfo("Cambios Guardados", "Los cambios en los cursos han sido guardados.")
        ventana_edicion_curso.destroy()

    # Crear una lista de cursos en un widget Listbox
    lista_cursos = tk.Listbox(ventana_edicion_curso, selectmode=tk.SINGLE)
    for curso in cursos:
        lista_cursos.insert(tk.END, curso[0])  # Mostrar el código del curso

    lista_cursos.pack()

    # Función para cargar los detalles del curso seleccionado
    def cargar_curso_seleccionado(event):
        seleccion = lista_cursos.curselection()
        if seleccion:
            indice = seleccion[0]
            codigo, costo, horario, cupo, catedratico = cursos[int(indice)]
            codigo_entry.delete(0, tk.END)
            codigo_entry.insert(0, codigo)
            costo_entry.delete(0, tk.END)
            costo_entry.insert(0, costo)
            horario_entry.delete(0, tk.END)
            horario_entry.insert(0, horario)
            cupo_entry.delete(0, tk.END)
            cupo_entry.insert(0, cupo)
            catedratico_entry.delete(0, tk.END)
            catedratico_entry.insert(0, catedratico)

    lista_cursos.bind("<<ListboxSelect>>", cargar_curso_seleccionado)

    # Crear etiquetas y campos de entrada para la edición de detalles del curso
    etiqueta_codigo = tk.Label(ventana_edicion_curso, text="Código:")
    etiqueta_codigo.pack()
    codigo_entry = tk.Entry(ventana_edicion_curso)
    codigo_entry.pack()

    etiqueta_costo = tk.Label(ventana_edicion_curso, text="Costo:")
    etiqueta_costo.pack()
    costo_entry = tk.Entry(ventana_edicion_curso)
    costo_entry.pack()

    etiqueta_horario = tk.Label(ventana_edicion_curso, text="Horario:")
    etiqueta_horario.pack()
    horario_entry = tk.Entry(ventana_edicion_curso)
    horario_entry.pack()

    etiqueta_cupo = tk.Label(ventana_edicion_curso, text="Cupo:")
    etiqueta_cupo.pack()
    cupo_entry = tk.Entry(ventana_edicion_curso)
    cupo_entry.pack()

    etiqueta_catedratico = tk.Label(ventana_edicion_curso, text="Catedrático:")
    etiqueta_catedratico.pack()
    catedratico_entry = tk.Entry(ventana_edicion_curso)
    catedratico_entry.pack()

    # Agregar un botón para guardar los cambios
    boton_guardar_cambios = tk.Button(ventana_edicion_curso, text="Guardar Cambios", command=guardar_cambios)
    boton_guardar_cambios.pack()

# -----------------------------------------Eliminar un curso------------------------------------------
def eliminar_curso():
    # Crear una ventana para mostrar la lista de cursos y permitir la eliminación
    ventana_eliminacion_curso = tk.Toplevel()
    ventana_eliminacion_curso.title("Eliminar Curso")
    ventana_eliminacion_curso.geometry("200x500")

    # Crear una lista de cursos a partir del archivo "cursos.txt"
    cursos = []
    try:
        with open("Cursos/cursos.txt", "r") as file:
            for line in file:
                codigo, costo, horario, cupo, catedratico = line.strip().split(":")
                cursos.append((codigo, costo, horario, cupo, catedratico))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de cursos.")

    # Función para guardar los cambios en el archivo "cursos.txt"
    def guardar_cambios():
        # Guardar los cursos en el archivo "cursos.txt" excluyendo los cursos eliminados
        with open("Cursos/cursos.txt", "w") as file:
            for curso in cursos:
                codigo, costo, horario, cupo, catedratico = curso
                file.write(f"{codigo}:{costo}:{horario}:{cupo}:{catedratico}\n")
        messagebox.showinfo("Cursos Eliminados", "Los cursos seleccionados han sido eliminados.")
        ventana_eliminacion_curso.destroy()

    # Crear una lista de cursos en un widget Listbox
    lista_cursos = tk.Listbox(ventana_eliminacion_curso, selectmode=tk.MULTIPLE)
    for curso in cursos:
        lista_cursos.insert(tk.END, curso[0])  # Mostrar el código del curso

    lista_cursos.pack()

    # Función para cargar los cursos seleccionados para eliminar
    def cargar_cursos_seleccionados(event):
        seleccion = lista_cursos.curselection()
        cursos_seleccionados = [cursos[int(indice)] for indice in seleccion]
        cursos.clear()
        for curso in cursos_seleccionados:
            cursos.append(curso)

    lista_cursos.bind("<<ListboxSelect>>", cargar_cursos_seleccionados)

    # Agregar un botón para eliminar los cursos seleccionados
    boton_eliminar_cursos = tk.Button(ventana_eliminacion_curso, text="Eliminar Cursos", command=guardar_cambios)
    boton_eliminar_cursos.pack()

# -------------------------Procesar el inicio de sesion del administrador----------------------------------
def iniciar_sesion_administrador():
    global admin_usuario, admin_contrasena
    admin_usuario = admin_usuario_entry.get()
    admin_contrasena = admin_contrasena_entry.get()

    administrador = cargar_administrador()

    if admin_usuario in administrador and administrador[admin_usuario] == admin_contrasena:
        messagebox.showinfo("Inicio de Sesión como Administrador Exitoso", "Inicio de sesión como administrador exitoso.")
        abrir_ventana_administracion()  # Abre la ventana de administración aquí
    else:
        messagebox.showerror("Error", "Nombre de administrador o contraseña incorrectos.")
#-------------------------------------------Inicio de Sesión---------------------------------
def iniciar_sesion_usuario():
    global ventana_inicio, nombre_de_usuario_actual 
    usuarios = cargar_usuarios()
    usuario = usuario_inicio.get()
    contrasena = contrasena_inicio.get()

    if usuario in usuarios and usuarios[usuario] == contrasena:
        global nombre_de_usuario_actual
        nombre_de_usuario_actual = usuario
        messagebox.showinfo("Inicio de Sesión Exitoso", "Inicio de sesión exitoso.")
        abrir_ventana_plataforma() 
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

#------------------------------------Registro------------------------------------------------
def abrir_ventana_registro():
    global ventana_registro  # Ventana de Registro Global
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registro de Usuario") # Titulo
    ventana_registro.geometry("400x600") #Tamaño
    ventana_registro.configure(bg="#E5E7E9")  # Color
    ventana_registro.resizable(0,0) # No permitir cambiar tamaño
    #Cargar la Imagen
    imagen_registro = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/logo_3.jpg")
    imagen_registro = imagen_registro.resize((400, 170))
    imagen_registro = ImageTk.PhotoImage(imagen_registro)
    imagen_registro_label = tk.Label(ventana_registro, image=imagen_registro)
    imagen_registro_label.image = imagen_registro
    imagen_registro_label.pack()

    global nombre_entry, apellido_entry, dpi_entry, telefono_entry, usuario_entry, email_entry, contrasena_entry, confirmar_contrasena_entry

    frame_registro = tk.Frame(ventana_registro)
    frame_registro.pack(pady=20)

    nombre_label = tk.Label(frame_registro, text="Nombre:")
    nombre_label.pack()
    nombre_entry = tk.Entry(frame_registro)
    nombre_entry.pack()

    apellido_label = tk.Label(frame_registro, text="Apellido:")
    apellido_label.pack()
    apellido_entry = tk.Entry(frame_registro)
    apellido_entry.pack()

    dpi_label = tk.Label(frame_registro, text="DPI:")
    dpi_label.pack()
    dpi_entry = tk.Entry(frame_registro)
    dpi_entry.pack()

    telefono_label = tk.Label(frame_registro, text="Teléfono:")
    telefono_label.pack()
    telefono_entry = tk.Entry(frame_registro)
    telefono_entry.pack()

    usuario_label = tk.Label(frame_registro, text="Nombre de Usuario:")
    usuario_label.pack()
    usuario_entry = tk.Entry(frame_registro)
    usuario_entry.pack()

    email_label = tk.Label(frame_registro, text="Correo Electrónico:")
    email_label.pack()
    email_entry = tk.Entry(frame_registro)
    email_entry.pack()

    contrasena_label = tk.Label(frame_registro, text="Contraseña:")
    contrasena_label.pack()
    contrasena_entry = tk.Entry(frame_registro, show="*")
    contrasena_entry.pack()

    confirmar_contrasena_label = tk.Label(frame_registro, text="Confirmar Contraseña:")
    confirmar_contrasena_label.pack()
    confirmar_contrasena_entry = tk.Entry(frame_registro, show="*")
    confirmar_contrasena_entry.pack()

    registro_button = tk.Button(frame_registro, text="Registrarse", command=lambda: registrar_usuario(ventana_registro))
    registro_button.config(font=("Helvetica", 10), height=2, width=15)  # Cambiar el tipo de letra y el tamaño
    registro_button.pack()

#------------------------------------Administrador------------------------------------
def abrir_ventana_administrador():
    ventana_admin = tk.Toplevel(ventana)
    ventana_admin.title("Inicio de Sesión como Administrador")
    ventana_admin.geometry("460x450")
    ventana_admin.resizable(0,0)
    ventana_admin.configure(bg="#ECF0F1")  # Color de Fondo
    imagen_admin = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/logo_2.jpg")
    imagen_admin = imagen_admin.resize((500, 200))
    imagen_admin = ImageTk.PhotoImage(imagen_admin)
    imagen_admin_label = tk.Label(ventana_admin, image=imagen_admin)
    imagen_admin_label.image = imagen_admin 
    imagen_admin_label.pack()

    global admin_usuario_entry, admin_contrasena_entry

    frame_admin = tk.Frame(ventana_admin)
    frame_admin.pack(pady=20)

    admin_usuario_label = tk.Label(frame_admin, text="Usuario Administrador:")
    admin_usuario_label.pack()
    admin_usuario_entry = tk.Entry(frame_admin)
    admin_usuario_entry.pack()

    admin_contrasena_label = tk.Label(frame_admin, text="Contraseña Administrador:")
    admin_contrasena_label.pack()
    admin_contrasena_entry = tk.Entry(frame_admin, show="*")
    admin_contrasena_entry.pack()

    iniciar_sesion_admin_button = tk.Button(frame_admin, text="Iniciar Sesión como Administrador", command=iniciar_sesion_administrador)
    iniciar_sesion_admin_button.pack()

# ----------------------------Ventana Principal Inicio de Sesion/Registro/Administrador----------------------------
ventana = tk.Tk()
ventana.title("Inicio de Sesión y Registro")
ventana.geometry("460x450")
ventana.resizable(0,0)
ventana.configure(bg="#ECF0F1")  # Color de Fondo
ancho_ventana = 500
alto_ventana = 500
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
x = (ancho_pantalla / 2) - (ancho_ventana / 2)
y = (alto_pantalla / 2) - (alto_ventana / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{int(x)}+{int(y)}")
imagen_principal = Image.open("C:/Users/Pc/Desktop/Proyecto IPC/Imagenes/logo.jpg")
imagen_principal = imagen_principal.resize((500, 200))
imagen_principal = ImageTk.PhotoImage(imagen_principal)
imagen_principal_label = tk.Label(ventana, image=imagen_principal)
imagen_principal_label.pack()

frame_inicio = tk.Frame(ventana)
frame_inicio.pack(pady=20)

usuario_inicio_label = tk.Label(frame_inicio, text="Usuario", font=("Arial", 10))
usuario_inicio_label.pack()
usuario_inicio = tk.Entry(frame_inicio)
usuario_inicio.pack()

contrasena_inicio_label = tk.Label(frame_inicio, text="Contraseña", font=("Arial", 10))
contrasena_inicio_label.pack()
contrasena_inicio = tk.Entry(frame_inicio, show="*")
contrasena_inicio.pack()

iniciar_sesion_button = tk.Button(frame_inicio, text="Iniciar Sesión", command=iniciar_sesion_usuario)
iniciar_sesion_button.config(font=("Helvetica", 10), height=2, width=15)  # Cambiar el tipo de letra y el tamaño
iniciar_sesion_button.pack()

# Botones de Registro y Administrador
registro_button = tk.Button(ventana, text="Registrarse", command=abrir_ventana_registro)
registro_button.pack()

admin_button = tk.Button(ventana, text="Iniciar Sesión como Administrador", command=abrir_ventana_administrador)
admin_button.pack()

ventana.mainloop()
