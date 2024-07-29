###########################################################################################################################
#                                                                                                                         #
#                                               EJERCÍCIO 12 - ÁRBOL AVL                                                  #
#                                                                                                                         #
# · Descripción: Implementar un árbol AVL que mantenga el equilibrio al insertar y eliminar elementos.                    #
# · Puntos clave: Árboles binarios balanceados, rotaciones.                                                               #
# · Aplicación práctica: En bases de datos, utilizar árboles AVL para mantener índices balanceados mejora el -            #
#   rendimiento de las operaciones de búsqueda, inserción y eliminación.                                                  #
#                                                                                                                         #
###########################################################################################################################

# ················ Importes ················ #

import tkinter as tk
from tkinter import messagebox

#··········································· #

# ============================================= Classe Para Crear Los Nodos ============================================= #

class Node:

    # ----------------------------------------- Iniciar los nodos del árbol --------------------------------------------- #

    def __init__(self, key, height = 1, left = None, right = None): # <------------------------- Definición de parámetros #

        self.key    = key         # · LLave 
        self.height = height      # · Altura 
        self.left   = left        # · Izquierda 
        self.right  = right       # · Derecha

    # ------------------------------------------------------------------------------------------------------------------- #

# ============================================ Classe Para Manipular El Árbol =========================================== #

class AVLTree:

    # --------------------------------- Obtener la altura del nodo en el árbol AVL -------------------------------------- #

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # -------------------------------------- Calcular el factor de equilibrio  ------------------------------------------ #

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right) 

    # -------------------------------------------- Rotación a la Derecha ------------------------------------------------ #

    def right_rotate(self, z):
        y        = z.left  # <----------------------------------------------------- 'y' es el hijo izquierdo del nodo 'z' #
        T3       = y.right # <-------------------------------------------------------- 'T3' es el subárbol derecho de 'y' #
        y.right  = z       
        z.left   = T3 
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y # <-------------------------------------------------- Retorna 'y' como la nueva raíz del subárbol rotado #

    # ------------------------------------------ Rotación a la Izquierda ------------------------------------------------ #

    def left_rotate(self, z):
        y        = z.right # <------------------------------------------------------- 'y' es el hijo derecho del nodo 'z' #
        T2       = y.left  # <------------------------------------------------------ 'T2' es el subárbol izquierdo de 'y' #
        y.left   = z
        z.right  = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y # <-------------------------------------------------- Retorna 'y' como la nueva raíz del subárbol rotado #

    # ------------------------------------ Insertar una nueva clave en el árbol ----------------------------------------- #

    def insert(self, node, key):
        if not node: # <------------------------ Si el nodo actual es None, crea y retorna un nuevo nodo con la clave key #
            return Node(key) 
        if key < node.key:
            node.left = self.insert(node.left, key)   # <--------------------------------- Inserción en el lado Izquierdo #
        elif key > node.key:
            node.right = self.insert(node.right, key) # <--------------------------------- Inserción en el lado Derecho   #
        else:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right)) # <- Actualizar la altura del nodo #
        balance     = self.get_balance(node)

        # -----------> Balancear El Árbol <------------------------------------------------- #

        if balance > 1 and key < node.left.key:           # · Desbalance a la Izquierda    · #
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:         # · Desbalance a la Derecha      · #
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:           # · Desbalance Izquierda-Derecha · #
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:         # · Desbalance Derecha-Izquierda · #
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        # ---------------------------------------------------------------------------------- #

        return node

    # ----------------------------- Encontrar el nodo con el valor mínimo en un subárbol -------------------------------- #

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current  

    # ----------------------------------------- Borrar una clave en el árbol -------------------------------------------- #

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # ----------------------------------------- Buscar una clave en el árbol -------------------------------------------- #

    def search(self, node, key, path = None):
        if path is None:
            path = []
        if not node or node.key == key:
            if node:
                path.append(node.key)
            return node, path
        path.append(node.key)
        
        if key < node.key:
            return self.search(node.left, key, path) 
        else:
            return self.search(node.right, key, path)

# ============================================ Clase Para Renderizar El Árbol =========================================== #

class AVLTreeInterface:

    def __init__(self, root): # <------------------------------------------------------------------------- Inicialización #
        self.tree = AVLTree()
        self.root_node = None

        self.root = root

        self.root.title("Visualización del Árbol AVL")                                   # · Título de la interfaz      · #
        self.root.resizable(False, False)                                                # · Bloqueo de escala          · #

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width = 800, height = 500, bg = 'white')     # · Ancho y Altura             · #
        self.canvas.pack()

        self.controls = tk.Frame(self.root)
        self.controls.pack()

        # ------------------------------------------------ BOTONES ------------------------------------------------------ #

        # ---------------------------------------------------------------------------> Botón de Insertar <--------------- #
        self.insert_label = tk.Label(self.controls, text="Insertar:")
        self.insert_label.grid(row=0, column=0)
        self.insert_entry = tk.Entry(self.controls)
        self.insert_entry.grid(row=0, column=1)
        self.insert_button = tk.Button(self.controls, text="Insertar", command=self.insert_key)
        self.insert_button.grid(row=0, column=2)
        # --------------------------------------------------------------------------------------------------------------- #

        # -----------------------------------------------------------------------------> Botón de Borrar <--------------- #
        self.delete_label = tk.Label(self.controls, text="Borrar:")
        self.delete_label.grid(row=1, column=0)
        self.delete_entry = tk.Entry(self.controls)
        self.delete_entry.grid(row=1, column=1)
        self.delete_button = tk.Button(self.controls, text="Borrar", command=self.delete_key)
        self.delete_button.grid(row=1, column=2)
        # --------------------------------------------------------------------------------------------------------------- #

        # -----------------------------------------------------------------------------> Botón de Buscar <--------------- #
        self.search_label = tk.Label(self.controls, text="Buscar:")
        self.search_label.grid(row=2, column=0)
        self.search_entry = tk.Entry(self.controls)
        self.search_entry.grid(row=2, column=1)
        self.search_button = tk.Button(self.controls, text="Buscar", command=self.search_key)
        self.search_button.grid(row=2, column=2)
        # --------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------- Insertar Clave En El Interfaz ------------------------------------------- #

    def insert_key(self):
        try:
            key = int(self.insert_entry.get())
            self.root_node = self.tree.insert(self.root_node, key)
            self.insert_entry.delete(0, tk.END)
            self.update_canvas()
        except ValueError:
            messagebox.showerror("Entrada no válida", "Ingrese un número entero válido.")

    # ------------------------------------------ Borrar Clave En El Interfaz -------------------------------------------- #

    def delete_key(self):
        try:
            key = int(self.delete_entry.get())
            self.root_node = self.tree.delete(self.root_node, key)
            self.delete_entry.delete(0, tk.END)
            self.update_canvas()
        except ValueError:
            messagebox.showerror("Entrada no válida", "Ingrese un número entero válido.")

    # ------------------------------------------- Buscar Clave En El Interfaz ------------------------------------------- #

    def search_key(self):
        try:
            key = int(self.search_entry.get())
            node, path = self.tree.search(self.root_node, key)
            self.search_entry.delete(0, tk.END)
            if node:
                messagebox.showinfo("Resultado de Búsqueda", f"Key {key} encontrado. Camino: {' -> '.join(map(str, path))}")
                self.update_canvas(path)
            else:
                messagebox.showinfo("Resultado de Búsqueda", f"Key {key} no encontrado.")
        except ValueError:
            messagebox.showerror("Entrada no válida", "Ingrese un número entero válido.")

    # ------------------------------------------ Update del Canvas (Interfaz) ------------------------------------------- #

    def update_canvas(self, path=None):
        self.canvas.delete("all")
        if self.root_node:
            self.draw_node(self.root_node, 400, 50, 200, path)

    # ----------------------------------------------- Dibujar los Nodos ------------------------------------------------- #

    def draw_node(self, node, x, y, dx, path, highlight=False):
        if node:
            color = "lightgreen" if highlight else "lightblue"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="blue", width=2)
            self.canvas.create_text(x, y, text=str(node.key))
            if node.left:
                self.canvas.create_line(x, y, x-dx, y+50)
                self.draw_node(node.left, x-dx, y+50, dx//2, path, node.left.key in path if path else False)
            if node.right:
                self.canvas.create_line(x, y, x+dx, y+50)
                self.draw_node(node.right, x+dx, y+50, dx//2, path, node.right.key in path if path else False)

# ======================================================================================================================= #

# ····· Crear Instancia de la Interfaz Gráfica ····· #

if __name__ == "__main__":
    root = tk.Tk()
    app = AVLTreeInterface(root)
    root.mainloop()

#··················································· #