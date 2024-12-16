# Proyecto 1

## Algoritmo A asterisco
### Importaciones de librerias y primeras configuraciones
Para el proyecto es necesario las librerias Pygames y PriorityQueue las cuales nos serviran para dibujar la cuadricula donde se dibujaran los nodos y asignar pesos prioritarios en los nodos.
Como primer paso se crea la ventana para visualizar los nodos, se le asigna un ancho y altura de igual distancia, se inicializa la ventana con el nombre "Algoritmo A*". Posteriormente se definen los colores que seran usados, la fuente para imprimir los datos del nodo. 

### Clase Nodo
La clase Nodo representa un nodo en la cuadricula por lo que en esta clase el nodo debe tener tanto propiedades como metodos que, las propiedades son utiles para definir la posicion, la posicion en la ventana, el color, el ancho del nodo y los nodos vecinos; mientras que los metodos tienen la funcion de obtener la posicion, cambiar estados (cambiar de un color a otro), dibujar el nodo actual, identificar a los vecinos e imprimir los calculos de peso y heuristica del nodo actual.

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
