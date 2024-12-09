import flet as ft
import sqlite3
import webbrowser 

# Conexión a la base de datos
def crear_conexion():
    conexion = sqlite3.connect('usuarios.db')
    return conexion

# Crear la tabla de usuarios si no existe
def crear_tabla():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Guardar los datos del usuario en la base de datos
def guardar_datos(nombre, edad):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conexion.commit()
    conexion.close()

# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(usuario, contrasena):
    if usuario == "admin" and contrasena == "1234":
        return True
    return False

    # Función para enviar mensaje personalizado a WhatsApp
def enviar_whatsapp(carrito):
    # Crear el mensaje con los detalles del carrito
    mensaje = "\n".join([f"{p['nombre']} - ${p['precio']}" for p in carrito])
    url = f"https://wa.me/595982323178?text={mensaje}"
    webbrowser.open(url)  # Abrir la URL de WhatsApp en el navegador

# Función para mostrar la interfaz de la tienda
def mostrar_tienda(page):
    productos = [
        {"nombre": "Remera", "precio": 35.00, "imagen": "C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\camisa.jpg"},
        {"nombre": "Pantalón", "precio": 50.00, "imagen": "C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\pantalon.jpg"},
        {"nombre": "Nike Air Force 1", "precio": 120.00, "imagen": "C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\zapatos.jpg"},
    ]
    carrito = []
    carrito_container = ft.Column()

    # Agregar producto al carrito
    def agregar_a_carrito(producto):
        carrito.append(producto)
        actualizar_carrito()

    # Actualizar carrito
    def actualizar_carrito():
        carrito_container.controls.clear()
        if carrito:
            carrito_text = "\n".join([f"{p['nombre']} - ${p['precio']}" for p in carrito])
            carrito_container.controls.append(ft.Text(f"Carrito:\n{carrito_text}", color=ft.colors.BLACK))
        else:
            carrito_container.controls.append(ft.Text("Carrito vacío.", color=ft.colors.BLACK))
        page.update()

    # Crear la lista de productos
    productos_container = ft.Row(wrap=True, spacing=10, run_spacing=10)

    for producto in productos:
        productos_container.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                       ft.Image(src=producto["imagen"], width=80, height=80, fit=ft.ImageFit.CONTAIN),
                    ft.Text(producto["nombre"], color=ft.colors.BLACK),
                    ft.Text(f"${producto['precio']}", color=ft.colors.BLACK),
                    ft.ElevatedButton("Agregar", on_click=lambda e, p=producto: agregar_a_carrito(p), bgcolor=ft.colors.GREEN_500),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(10),
                bgcolor=ft.colors.WHITE,
                border_radius=ft.border_radius.all(5),
            )
        )


   # Cambiar interfaz a la tienda
    page.controls.clear()
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\fondo1.jpg",
                    fit=ft.ImageFit.COVER,
                    opacity=0.8
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text("JP Store", size=34, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                                bgcolor=ft.colors.WHITE,
                                opacity=0.7,
                                padding=ft.padding.all(10),
                                border_radius=ft.border_radius.all(5)
                            ),
                            productos_container,
                            ft.Divider(),
                            carrito_container,
                            ft.ElevatedButton("Finalizar compra", on_click=lambda e: enviar_whatsapp(carrito), bgcolor=ft.colors.BLUE_500),
                            ft.ElevatedButton("Limpiar carrito", on_click=lambda e: [carrito.clear(), actualizar_carrito()], bgcolor=ft.colors.RED_500),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=100)
                )
            ]
        )
    )
    actualizar_carrito()


def main(page: ft.Page):
    page.title = "Gestión de Usuarios"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Crear la tabla si no existe
    crear_tabla()

    # Crear los componentes de la interfaz con fondos transparentes
    nombre_input = ft.TextField(
        label="Nombre",
        width=300,
        bgcolor="#FFFFFFA0",
        border_color="#FFFFFFA0",
        color=ft.colors.BLACK  # Cambiar el color del texto del campo a negro
    )
    edad_input = ft.TextField(
        label="Edad",
        width=300,
        bgcolor="#FFFFFFA0",
        border_color="#FFFFFFA0",
        color=ft.colors.BLACK  # Cambiar el color del texto del campo a negro
    )

    mensaje_container = ft.Column()

    # Guardar datos
    def guardar_click(e):
        mensaje_container.controls.clear()
        nombre = nombre_input.value
        edad = edad_input.value

        if nombre and edad.isdigit():
            edad = int(edad)
            guardar_datos(nombre, edad)
            if edad >= 18:
                mostrar_tienda(page)  # Mostrar tienda si es mayor de edad
            else:
                mensaje_container.controls.append(ft.Text(f"{nombre} es menor de edad.", color=ft.colors.BLACK))
            nombre_input.value = ""
            edad_input.value = ""
        else:
            mensaje_container.controls.append(ft.Text("Por favor, ingrese un nombre válido y una edad.", color=ft.colors.RED))
        page.update()

    guardar_button = ft.ElevatedButton("Guardar", on_click=guardar_click, bgcolor=ft.colors.BLUE_500)
    limpiar_button = ft.ElevatedButton("Limpiar", on_click=lambda e: [nombre_input.clear(), edad_input.clear(), mensaje_container.controls.clear(), page.update()], bgcolor=ft.colors.RED_500)

    usuario_input = ft.TextField(
        label="Usuario",
        width=300,
        bgcolor="#FFFFFFA0",
        border_color="#FFFFFFA0",
        color=ft.colors.BLACK
    )
    contrasena_input = ft.TextField(
        label="Contraseña",
        width=300,
        bgcolor="#FFFFFFA0",
        border_color="#FFFFFFA0",
        color=ft.colors.BLACK,
        password=True  # Campo para contraseña
    )

    mensaje_login = ft.Column()

    def login_click(e):
        mensaje_login.controls.clear()
        usuario = usuario_input.value
        contrasena = contrasena_input.value

        if verificar_credenciales(usuario, contrasena):
            page.controls.clear()
            page.add(
                ft.Stack(
                    [
                        ft.Image(
                            src="C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\fondo.jpg",
                            fit=ft.ImageFit.COVER,
                            opacity=0.8
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("Gestión de Usuarios", size=30, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                                        bgcolor=ft.colors.WHITE,
                                        opacity=0.7,
                                        padding=ft.padding.all(10),
                                        border_radius=ft.border_radius.all(5)
                                    ),
                                    nombre_input,
                                    edad_input,
                                    guardar_button,
                                    limpiar_button,
                                    mensaje_container,
                                ]
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=100)
                        )
                    ]
                )
            )
        else:
            # Si las credenciales son incorrectas, mostramos un mensaje de error
            mensaje_login.controls.append(ft.Text("Usuario o contraseña incorrectos.", color=ft.colors.RED))
            page.update()

    login_button = ft.ElevatedButton("Iniciar sesión", on_click=login_click, bgcolor=ft.colors.GREEN_500, color=ft.colors.WHITE)

    # Contenedor principal de contenido para login con el título actualizado
    login_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Iniciar sesión", size=30, color=ft.colors.BLACK),
                bgcolor=ft.colors.WHITE,
                opacity=0.7,
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(5)
            ),
            usuario_input,
            contrasena_input,
            login_button,
            mensaje_login
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Estructura de la página con imagen de fondo y contenido centrado más abajo
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="C:\\Users\\Owner\\OneDrive\\Documents\\ExamenFinal\\fondo.jpg",
                    fit=ft.ImageFit.COVER,
                    opacity=0.8
                ),
                ft.Container(
                    content=login_content,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=100)
                )
            ]
        )
    )

# Inicializar la aplicación
ft.app(target=main)



































