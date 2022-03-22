
import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3


class Producto():
    # Ruta Base de datos
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestion de Productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')


    # Creacion del contenedor Frame principal
        frame = LabelFrame( self.ventana, text = "Registrar un nuevo Producto", font=('Times New Roman', 18, "bold"))
        frame.grid(row = 0, column = 0, columnspan = 5, pady = 20)

    # Label
        self.etiqueta_nombre = Label(frame, text="Nombre: ",font=('Times New Roman', 16))
        self.etiqueta_nombre.grid(row=1, column=0)

    # Entry (caja de texto)
        self.nombre = Entry(frame)
        self.nombre.focus() # Para el raton vaya a este Entry desde el inicio
        self.nombre.grid(row=1, column=1)
    # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ",font=('Times New Roman', 16))
        self.etiqueta_precio.grid(row=2, column=0)
    # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1, pady=10)
    # Label Cateogoría
        self.etiqueta_categoria= Label(frame, text="Categoria: ",font=('Times New Roman', 16))
        self.etiqueta_categoria.grid(row=3, column=0)
    # Entry Categoría
        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1, pady=10)

    #Boton Guardar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Times New Roman', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=4, columnspan=2, sticky=W + E)

    # Boton Editar y Eliminar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Times New Roman', 14, "bold"))
        boton_eliminar = ttk.Button(text='ELIMINAR', command = self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=6, column=0,columnspan=2, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR',command = self.edit_producto,style='my.TButton')
        boton_editar.grid(row=6, column=2,columnspan=2, sticky=W + E)

    # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red',font=('Times New Roman', 14))
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

    # Tabla de Productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Times New Roman',14))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
    # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#1','#2','#3'), style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=4)
        self.tabla['show'] = 'headings'
        self.tabla.heading('#1', text='Nombre',anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#2', text='Precio', anchor = CENTER) # Encabezado 1
        self.tabla.heading('#3', text='Categoria', anchor=CENTER)  # Encabezado 2


        self.get_productos()



    def db_consulta(self,consulta, parametros=()) :
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        for fila in registros_db:
            print(fila)
            self.tabla.insert('',0,text = fila[1], values = (fila[1],fila[2], fila[3]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?,?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio'
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio'
        elif self.validacion_nombre()  and self.validacion_precio() and self.validacion_categoria()==False:
            print("La categoría es obligatoria")
            self.mensaje['text'] = 'La cateogoría es obligatoria'
        else:
            print("El nombre y el precio son obligatorios")
            self.mensaje['text'] = 'No has introducido el precio, nombre o categoría'
        self.get_productos() #Actualizar el contenido y ver los cambios.

    def del_producto(self):
        # Debug
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())['text'])
        #print(self.tabla.item(self.tabla.selection())['values'])
        #print(self.tabla.item(self.tabla.selection())['values'][0])
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,)) # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos() # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        old_precio = self.tabla.item(self.tabla.selection())['values'][1]# El 1 es debido a que el precio
        # esta dentro de una lista
        categoria= self.tabla.item(self.tabla.selection())['values'][2]
        self.ventana_editar = Toplevel()  # Para crear la ventana precio
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')
        #Frame
        frame_ep= LabelFrame(self.ventana_editar, text="Editar el siguiente producto: ",font=('Times New Roman', 18, "bold"))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
        #Nombre Antigui
        self.etiqueta_nombre_antiguo=Label(frame_ep, text="Nombre Antiguo:",font=('Times New Roman', 14))
        self.etiqueta_nombre_antiguo.grid(row=2,column=0)
        self.input_nombre_antiguo=Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)
        #Nombre Nuevo
        self.etiqueta_nombre_nuevo=Label(frame_ep,text="Nombre Nuevo:",font=('Times New Roman', 14))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        #Introducimos nombre
        self.input_nombre_nuevo=Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()
        # Precio Antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio Antiguo:",font=('Times New Roman', 14))
        self.etiqueta_precio_antiguo.grid(row=4, column=0)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)
        #Precio Nuevo
        self.etiqueta_precio_nuevo=Label(frame_ep,text="Precio Nuevo:",font=('Times New Roman', 14))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        #Introducimos precio
        self.input_precio_nuevo=Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)
        #Categoria Antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria Antigua:", font=('Times New Roman', 14))
        self.etiqueta_categoria_antigua.grid(row=6, column=0)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria),
                                          state='readonly')
        self.input_categoria_antigua.grid(row=6, column=1)
        # Categirua Nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría Nueva:", font=('Times New Roman', 14))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        # Introducimos categoría
        self.input_categoria_nueva = Entry(frame_ep)
        self.input_categoria_nueva.grid(row=7, column=1)
        # Boton Actualizar Producto
        st = ttk.Style()
        st.configure('my.TButton', font=('Times New Roman', 14, "bold"))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton',
                                           command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                     self.input_nombre_antiguo.get(),
                                                                                     self.input_precio_nuevo.get(),
                                                                                     self.input_precio_antiguo.get(),
                                                                                     self.input_categoria_nueva.get(),
                                                                                     self.input_categoria_antigua.get()))

        self.boton_actualizar.grid(row=8, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre,  nuevo_precio, antiguo_precio, nueva_categoria, antigua_categoria):
        producto_modificado = False
        query = "UPDATE producto SET nombre=?, precio=?, categoria=? WHERE nombre=? AND precio=? AND categoria=?"

        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '':
            parametros = (nuevo_nombre, antiguo_precio,nueva_categoria, antiguo_nombre, antiguo_precio,antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '':
            parametros = (antiguo_nombre,nuevo_precio,nueva_categoria, antiguo_nombre, antiguo_precio,antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '':
            parametros = (nuevo_nombre,nuevo_precio,antigua_categoria, antiguo_nombre, antiguo_precio,antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '':
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        if (producto_modificado):
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text']="El producto {} ha sido modificado". format(antiguo_nombre)
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje['text'] = "El producto {} NO ha sido modificado".format(antiguo_nombre)




if __name__ == '__main__':
    root = Tk()
    app = Producto(root)
    root.mainloop()
