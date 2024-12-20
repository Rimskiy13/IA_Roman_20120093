import os

def renombrar_imagenes(carpeta, numero_inicial):

    extensiones_validas = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff','webm']
    
    try:
        archivos = os.listdir(carpeta)
        
        
        imagenes = [archivo for archivo in archivos if os.path.splitext(archivo)[1].lower() in extensiones_validas]
        
        if not imagenes:
            print("No se encontraron imágenes en la carpeta especificada.")
            return

        
        for indice, imagen in enumerate(imagenes):
            
            nueva_imagen = f"img_{numero_inicial + indice:04d}{os.path.splitext(imagen)[1]}"
            
            
            ruta_vieja = os.path.join(carpeta, imagen)
            ruta_nueva = os.path.join(carpeta, nueva_imagen)
            
            
            os.rename(ruta_vieja, ruta_nueva)
            print(f"Renombrado: {imagen} -> {nueva_imagen}")
        
        print(f"Renombradas {len(imagenes)} imágenes exitosamente.")
    
    except Exception as e:
        print(f"Error al renombrar las imágenes: {e}")


carpeta = r"C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/Carritos/imagenes_pinterest/Volkswagen Jetta N"  

renombrar_imagenes(carpeta, 1)
