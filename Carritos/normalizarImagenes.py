import os
from skimage.io import imread, imsave
from skimage.transform import resize
import numpy as np

def normalize_images(input_folder, output_folder, target_size=(128, 128)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Recorrer las imágenes en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            try:
                image = imread(input_path)
                
                if image.ndim < 2:
                    print(f"Imagen no válida (menos de 2D): {filename}")
                    continue
                
                image_resized = resize(
                    image, 
                    target_size, 
                    anti_aliasing=True, 
                    preserve_range=True
                )
                
                image_resized = np.clip(image_resized, 0, 255).astype(np.uint8)
                
                imsave(output_path, image_resized)
                print(f"Procesada: {filename} -> Guardada en {output_folder}")
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")
    
    print(f"Todas las imágenes han sido normalizadas y guardadas en: {output_folder}")


# Ejemplo de uso
input_folder = "C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/Carritos/imagenes_pinterest/Volkswagen Jetta"
output_folder = "C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/Carritos/imagenes_pinterest/Volkswagen Jetta N"
normalize_images(input_folder, output_folder)