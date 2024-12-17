# Proyecto 1

## Algoritmo A asterisco
### Importaciones de librerias y primeras configuraciones
Para el proyecto es necesario las librerias Pygames y PriorityQueue las cuales nos serviran para dibujar la cuadricula donde se dibujaran los nodos y asignar pesos prioritarios en los nodos.
Como primer paso se crea la ventana para visualizar los nodos, se le asigna un ancho y altura de igual distancia, se inicializa la ventana con el nombre "Algoritmo A*". Posteriormente se definen los colores que seran usados, la fuente para imprimir los datos del nodo. 

```python
import pygame
from queue import PriorityQueue

# Configuraciones iniciales
pygame.init()
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
AZUL = (57, 107, 170)
PURPURA = (128, 0, 128)

# Fuente
FUENTE = pygame.font.SysFont('arial', 32)
```

### Clase Nodo
La clase Nodo representa un nodo en la cuadricula por lo que en esta clase el nodo debe tener tanto propiedades como metodos que, las propiedades son utiles para definir la posicion, la posicion en la ventana, el color, el ancho del nodo y los nodos vecinos; mientras que los metodos tienen la funcion de obtener la posicion, cambiar estados (cambiar de un color a otro), dibujar el nodo actual, identificar a los vecinos e imprimir los calculos de peso y heuristica del nodo actual.

```python
class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []

    def get_pos(self): # 
        return self.fila, self.col

    def es_pared(self): #
        return self.color == NEGRO

    def es_inicio(self): #
        return self.color == NARANJA

    def es_fin(self): #
        return self.color == PURPURA

    def restablecer(self): #
        self.color = BLANCO

    def hacer_inicio(self): #
        self.color = GRIS

    def hacer_pared(self): #
        self.color = NEGRO

    def hacer_fin(self): # 
        self.color = AZUL

    def ponerlo_cerrado(self): #
        self.color = ROJO

    def ponerlo_abierto(self): 
        self.color = VERDE

    def camino(self):
        self.color = PURPURA

    def imprimir_calculos(self, ventana, calculo_g, Heuristica, calculo_f, camino):
        tecla = True
        while tecla:
            for event in pygame.event.get():
                imprimir_g = FUENTE.render(f"Peso: {int(calculo_g)}", True, NEGRO)
                imprimir_heuristica = FUENTE.render(f"Heurística: {int(Heuristica)}", True, NEGRO)
                imprimir_f = FUENTE.render(f"Costo: {int(calculo_f)}", True, NEGRO)

                ventana.blit(imprimir_g, (self.x + 5, self.y + 5))
                ventana.blit(imprimir_heuristica, (self.x + 5, self.y + 20))
                ventana.blit(imprimir_f, (self.x + 5, self.y + 35))

                pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        tecla = False
            
                        


    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
    
    def Alrededor_vecinos(self, grid):
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not grid[self.fila+1][self.col].es_pared(): # Abajo
            self.vecinos.append(grid[self.fila+1][self.col])

        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():  # Abajo-Derecha
            self.vecinos.append(grid[self.fila + 1][self.col + 1])

        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():  # Abajo-Izquierda
            self.vecinos.append(grid[self.fila + 1][self.col - 1])

        if self.fila > 0 and not grid[self.fila-1][self.col].es_pared(): # Arriba
            self.vecinos.append(grid[self.fila-1][self.col])

        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():  # Arriba-Derecha
            self.vecinos.append(grid[self.fila - 1][self.col + 1])

        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():  # Arriba-Izquierda
            self.vecinos.append(grid[self.fila - 1][self.col - 1])

        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared(): # Izquierda
            self.vecinos.append(grid[self.fila][self.col-1])

        if self.col < self.total_filas - 1 and not grid[self.fila][self.col+1].es_pared(): # Derecha
            self.vecinos.append(grid[self.fila][self.col+1])
```

El metodo imprimir_calculos anexa los calculos que se hacen del nodo actual a la posicion actual del nodo del cual se hizo el calculo, debido a la forma en que se imprimen los nodos no hay tiempo de visualizar los calculos, se añadio la funcionalidad de oprimir la tecla n cada vez que se hace un calculo del nodo actual por lo que para poder avanzar a los sigueintes calculos hay que oprimir la tecla n cada vez que se exploran mas nodos.
El metodo Alrededor_vecinos pone en una lista a los nodos vecinos tanto verticales, horizontales y diagonales; siempre se verifica que no sean nodos pared.
El metodo dibujar, dibuja el nodo con su respectivo color y posicion.

### Dibujado del grid
Para poder visualizar de mejor forma la cuadricula se implementaron 3 metodos que crean una cuadricula y dibujan una cuadricula.
El metodo crear_grid, crea un grid a apartir del numero de filas y ancho de la venta que anexa los nodos que tendra la ventana.
El metodo dibujar_grid crea lineas tanto verticales como horizontales de acuerdo al numero de filas y ancho de la ventana. 
El metodo dibujar manda llamar al metodo anterior asi como al metodo dibujar en la clase nodo.

```python
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()
```

### Funcion main y creacion de los nodos incio, fin y paredes
La funcion main es la que inicializa los eventos tanto de incio del algoritmo como de dibujar los nodos de incio, fin y paredes, asi como de restablecer nodos para borrar paredes o nodos inicio y fin.
Los controles para crear los nodos inicio y fin son el clic izquierdo y para borraralos o reestablecerlos el clic derecho. Las teclas para iniciar el algoritmo es la tecla i y para reiniciar los nodos la tecla r.
El metodo obtener_click_pos hace la traduccion de las coordenadas del mouse a las de el grid de la ventana que se creo.

```python
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.Alrededor_vecinos(grid)
                    a_asterisco(lambda: dibujar(ventana, grid, FILAS, ancho), ventana,  grid, inicio, fin)

                if event.key == pygame.K_r:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
            
            

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
```

### Funcion del Algoritmo Asterisco y metodos auxiliares
Como primer instancia se crean 2 metodos que ayudaran a dibujar los nodos camino que seran los nodos que indicaran el camino mas corto y el metodo Heuristica que determina la distancia entre 2 puntos de la cuadricula.

La funcion que contendra el algoritmo inicia con una lista  (lista_abierta) que contendra a los nodos ordenados por costo, teniendo como prioridad a los de menor coste,
La lista camino_nodos contendra los nodos padre de cada nodo que se ha explorado, que ayudara a construir mas tarde el camino de nodos.

Los calculos de la funcion F(n) y G(n) son incializados con un valor infinito y almacenados en las variables calculo_g y calculo_f, posteriormente calculo_g es puesto en 0 y calculo_f con la distancia del punto de origen y final. Tambien se crea una lista auxiliar para verificar si un nodo esta en la lista abierta.

Posteriormente se crea un bucle que se ejecutara mientras la lista_abierta no este vacia, se designara un nodo que contendra el nodo con menor coste y se removera de la copia de la lista para que no se compare consigo mismo. 

Si el nodo actual es igual al nodo final se dibujara el camino de nodos y terminara de ejecutar el algoritmo.

Se hace uso de un ciclo for para explorar a los nodos vecinos, se hace el calculo de la funcion G(n), se guarda en una variable temporal y a partir de este calculo se determina si el costo es menor, de ser asi actualizara la lista que contiene los nodos padre, los calculos de la funcion G(n) y F(n) y si los nodos vecinos no estan en la lista abierta se marca como un nodo que ya ha sido explorado.

Posteriormente se dibujara los calculos con los datos del nodo actual.

``` python
def Heuristica(p1, p2): # Funcion Heuristica
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) # La distancia entre 2 puntos


def mejor_camino(camino_nodos, datos, nodo_actual, dibujar):
    while nodo_actual in camino_nodos:
        nodo_actual = camino_nodos[nodo_actual]
        nodo_actual.camino()
        print("Nodo:", nodo_actual.get_pos())
        dibujar()

    for dato in datos:
        print(dato)


def a_asterisco(dibujar, ventana, grid, incio, fin):
    contador = 0
    lista_abierta = PriorityQueue()
    lista_abierta.put((0, contador, incio))
    datos = []
    camino_nodos = {} # La lista del mejor camino
    calculo_g = {nodo: float("inf") for fila in grid for nodo in fila}
    calculo_g[incio] = 0
    calculo_f = {nodo: float("inf") for fila in grid for nodo in fila}
    calculo_f[incio] = Heuristica(incio.get_pos(), fin.get_pos())

    lista_abierta_copia = {incio}

    while not lista_abierta.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        nodo_actual = lista_abierta.get()[2]
        lista_abierta_copia.remove(nodo_actual)

        if nodo_actual == fin:
            mejor_camino(camino_nodos, datos, fin, dibujar)
            fin.hacer_fin()
            return True
        
        for vecino in nodo_actual.vecinos:
            calculo_g_tmp = calculo_g[nodo_actual]+1
            
            if calculo_g_tmp < calculo_g[vecino]:
                camino_nodos[vecino] = nodo_actual
                calculo_g[vecino] = calculo_g_tmp
                calculo_f[vecino] = calculo_g_tmp + Heuristica(vecino.get_pos(), fin.get_pos())
                datos.append((calculo_g_tmp, Heuristica(nodo_actual.get_pos(), fin.get_pos()), calculo_g_tmp + Heuristica(vecino.get_pos(), fin.get_pos())))
                if vecino not in lista_abierta_copia:
                    contador += 1
                    lista_abierta.put((calculo_f[vecino], contador, vecino))
                    lista_abierta_copia.add(vecino)
                    vecino.ponerlo_abierto()
        
        nodo_actual.imprimir_calculos(
            ventana, 
            calculo_g[nodo_actual], 
            Heuristica(nodo_actual.get_pos(), fin.get_pos()), 
            calculo_f[nodo_actual],
            camino_nodos
        )
        dibujar()

        if nodo_actual != incio:
            nodo_actual.ponerlo_cerrado()

    return False
```
