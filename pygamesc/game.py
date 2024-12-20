import pygame
import random
import sys
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.models import Sequential

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------- CONFIGURACIÓN DEL JUEGO ----------------------------------------

pygame.init()

# Pantalla y colores
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Esquiva la Bala Estilo IA")
BLANCO, NEGRO = (255, 255, 255), (0, 0, 0)

# Variables globales
jugador = None
bala = None
nave = None
menu_activo = True
fondo = None
pausa = False
modo_auto, modo_arbol = False, False
datos_modelo = []
fuente = pygame.font.SysFont('Arial', 24)
intervalo_salto_red = 1
contador_salto_red = 0

# Gravedad y salto
salto, en_suelo = False, True
salto_altura, gravedad = 15, 1

# Modelos entrenados
modelo_entrenado, modelo_entrenado_arbol = None, None

# ---------------------------------------- CARGA DE IMÁGENES ----------------------------------------

# Imágenes
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
bala_img = pygame.image.load('assets/sprites/purple_ball.png')

jugador_frames = [
    pygame.image.load(f'assets/sprites/mono_frame_{i}.png') for i in range(1, 5)
]

# Escalar fondo
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# ---------------------------------------- SPRITES Y VARIABLES ----------------------------------------

# Rectángulos
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Animación del jugador
current_frame = 0
frame_speed = 7
frame_count = 0

# Bala
bala_disparada = False
velocidad_bala = -10

# Fondo en movimiento
fondo_x1, fondo_x2 = 0, w

# ---------------------------------------- FUNCIONES DEL JUEGO ----------------------------------------

# Función: Manejar el salto
def manejar_salto():
    global salto, salto_altura, en_suelo, jugador
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto, en_suelo, salto_altura = False, True, 15

# Función: Disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-15, -5)
        bala_disparada = True

# Función: Reiniciar la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

# Función: Actualizar el juego
def update():
    global bala, velocidad_bala, fondo_x1, fondo_x2, frame_count, current_frame

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w: fondo_x1 = w
    if fondo_x2 <= -w: fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar nave y bala
    pantalla.blit(nave_img, (nave.x, nave.y))
    if bala_disparada: bala.x += velocidad_bala
    if bala.x < 0: reset_bala()
    pantalla.blit(bala_img, (bala.x, bala.y))

    # Verificar colisión
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        if not modo_arbol and not modo_auto:  
            fit_red()
            fit_arbol()
        reiniciar_juego()

# Función: Reiniciar el juego
def reiniciar_juego():
    global menu_activo, jugador, bala, bala_disparada, nave, salto, en_suelo
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto, en_suelo = False, True
    mostrar_menu()

# ---------------------------------------- FUNCIONES DEL MODELO ----------------------------------------

# Función: Guardar Datos
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función: Pausar juego
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función: Entrenar Red Neuronal
def fit_red():
    global modelo_entrenado, datos_modelo
    if len(datos_modelo) < 2:
        print("No se puede entenar por falta de datos.")
        return

    datos = np.array(datos_modelo)
    x, y = datos[:, :2], datos[:, 2].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    modelo = Sequential([
        Input(shape=(x.shape[1],)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(len(np.unique(y)), activation='softmax')
    ])
    modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    modelo.fit(x_train, y_train, epochs=100, batch_size=32, verbose=1)
    loss, acc = modelo.evaluate(x_test, y_test, verbose=0)
    print(f"Modelo Red Neuronal - Precisión: {acc:.2f}, Pérdida: {loss:.2f}")
    modelo_entrenado = modelo

# Función: Decidir salto usando Red Neuronal
def salto_red():
    global modelo_entrenado, salto, en_suelo
    if modelo_entrenado is None: return

    try:
        distancia = abs(jugador.x - bala.x)
        entrada = np.array([[velocidad_bala, distancia]]) 
    except AttributeError as e:
        print(f"Error en la entrada: {e}")
        return
    
    try:
        prediccion = modelo_entrenado.predict(entrada, verbose=0)
        clase_predicha = np.argmax(prediccion)  

        if clase_predicha == 1 and en_suelo:  
            salto = True
            en_suelo = False
    except Exception as e:
        print(f"Error en la predicción: {e}")

# Función: Entrenar Árbol de DecisiónB
def fit_arbol():
    global modelo_entrenado_arbol, datos_modelo

    if len(datos_modelo) < 2:
        print("No se puede entenar por falta de datos.")
        return
    
    dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])
    X, y = dataset[['Velocidad', 'Distancia']], dataset['Salto']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)
    modelo = DecisionTreeClassifier(max_depth=5, random_state=44)
    modelo.fit(X_train, y_train)
    acc = modelo.score(X_test, y_test)
    print(f"Árbol de Decisión - Precisión: {acc:.2f}")
    modelo_entrenado_arbol = modelo

def salto_arbol():
    global modelo_entrenado_arbol, salto, en_suelo

    # Validar que el modelo está entrenado
    if modelo_entrenado_arbol is None:
        print("Modelo no entrenado. No se puede decidir.")
        return

    # Validar que las variables necesarias existen
    try:
        distancia = abs(jugador.x - bala.x)
        entrada = pd.DataFrame([[velocidad_bala, distancia]], columns=['Velocidad', 'Distancia'])
    except AttributeError as e:
        print(f"Error al calcular la entrada: {e}")
        return

    # Realizar la predicción
    try:
        prediccion = modelo_entrenado_arbol.predict(entrada)[0]
        if prediccion == 1 and en_suelo and distancia < 100:
            salto = True
            en_suelo = False
            print("Saltar")
        else:
            print("No saltar")
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")

# ---------------------------------------- MENÚ Y BUCLE PRINCIPAL ----------------------------------------

# Función: Mostrar menú
def mostrar_menu():
    global menu_activo, modo_auto, modo_arbol, datos_modelo, modelo_entrenado, modelo_arbol_entrenado
    pantalla.fill(NEGRO)
    texto = [
        "Presiona una tecla:",
        "\"M\" Manual", "\"A\" Automático", "\"T\" Árbol", "\"G\" Graficar dataset", "\"Q\" Salir"
    ]

    x = w // 20
    y_inicial = h // 18  
    espaciado = h // 15

    for i, t in enumerate(texto):
        render = pygame.font.SysFont('Arial', 24).render(t, True, BLANCO)
        pantalla.blit(render, (w // 20, h // 18 + i * h // 15))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m: menu_activo, modo_auto, modo_arbol = False, False, False
                elif evento.key == pygame.K_a: menu_activo, modo_auto, modo_arbol = False, True, False
                elif evento.key == pygame.K_t: menu_activo, modo_auto, modo_arbol = False, False, True
                elif evento.key == pygame.K_q: pygame.quit(); exit()
                elif evento.key == pygame.K_g:
                    if datos_modelo:
                        x = [d[0] for d in datos_modelo]  # Velocidad
                        y = [d[1] for d in datos_modelo]  # Distancia
                        z = [d[2] for d in datos_modelo]  # Salto

                        
                        fig = plt.figure()
                        ax = fig.add_subplot(111, projection='3d')
                        ax.scatter(x, y, z, c='r', marker='o')
                        ax.set_xlabel('Velocidad')
                        ax.set_ylabel('Distancia')
                        ax.set_zlabel('Salto')

                        
                        plt.show()
# Bucle principal
def main():
    global salto, en_suelo, bala_disparada, contador_salto_red
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_r:  # Presiona 'p' para pausar el juego
                    reiniciar_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto or modo_arbol:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            if modo_auto:         
                
                if contador_salto_red >= intervalo_salto_red:
                    salto_red()
                    contador_salto_red = 0  # Reiniciar el contador
                else:
                    contador_salto_red += 1

                if salto:
                    manejar_salto()
            
            if modo_arbol:         
                
                if contador_salto_red >= intervalo_salto_red:
                    salto_arbol()
                    contador_salto_red = 0  # Reiniciar el contador
                else:
                    contador_salto_red += 1

                if salto:
                    manejar_salto()


            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

