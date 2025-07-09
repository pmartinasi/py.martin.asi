from decimal import Decimal, getcontext
from typing import List
import time
import random
from staticmap import StaticMap, CircleMarker
from typing import Tuple

# Establecer precisión decimal adecuada
getcontext().prec = 10

def calculate_percentage(part: float, total: float) -> float:
    """
    Calcula el porcentaje que representa 'part' con respecto a 'total'.

    Parámetros:
        part (float): La parte (cantidad parcial).
        total (float): El total.

    Retorna:
        float: El porcentaje correspondiente (entre 0 y 100).

    Lanza:
        ValueError: Si el total es 0 para evitar división por cero.
    """
    if total == 0:
        raise ValueError("El total no puede ser 0.")
    return (part / total) * 100
    
def random_timer(min_seconds: float = 0.01, max_seconds: float = 5.0):
    """
    Pausa la ejecución por un tiempo aleatorio entre min_seconds y max_seconds.

    Parámetros:
        min_seconds (float): Tiempo mínimo en segundos.
        max_seconds (float): Tiempo máximo en segundos.
    """
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Delay hasta la siguiente imagen: {delay:.2f} segundos...")
    time.sleep(delay)
def generate_decimal_range(start_val, end_val, step_val) -> List[Decimal]:
    """
    Genera una lista de valores decimales entre start_val y end_val, ambos incluidos,
    con un paso de step_val. Siempre recorre de menor a mayor.

    Parámetros:
        start_val (str | float): Valor inicial
        end_val (str | float): Valor final
        step_val (str | float): Paso

    Retorna:
        List[Decimal]: Lista de valores decimales
    """
    # Convertir a Decimal
    a = Decimal(str(start_val))
    b = Decimal(str(end_val))
    step = Decimal(str(step_val))

    # Asegurar que start sea menor que end
    start = min(a, b)
    end = max(a, b)

    if step <= 0:
        raise ValueError("El paso debe ser un número positivo mayor que cero.")

    # Calcular el número de pasos (incluyendo el final)
    num_steps = int((end - start) / step) + 1

    # Generar los valores
    return [start + step * i for i in range(num_steps)]

def create_static_map(width: int, height: int) -> StaticMap:
    """
    Crea una instancia de StaticMap con el tamaño especificado.
    """
    return StaticMap(width, height)

def add_marker_to_map(map_obj: StaticMap, coordinates: Tuple[float, float], color: str = 'red', size: int = 0):
    """
    Agrega un marcador circular al mapa dado.
    
    Parámetros:
        map_obj: instancia de StaticMap
        coordinates: tupla (lon, lat)
        color: color del marcador
        size: tamaño del marcador
    """
    marker = CircleMarker(coordinates, color, size)
    map_obj.add_marker(marker)

def render_and_save_map(map_obj: StaticMap, zoom: int, filename: str):
    """
    Renderiza el mapa con el zoom especificado y lo guarda como imagen.
    
    Parámetros:
        map_obj: instancia de StaticMap
        zoom: nivel de zoom (18 o 19 típicamente)
        filename: nombre del archivo de salida
    """
    image = map_obj.render(zoom=zoom)
    image.save(filename)

# ---------------------
# Ejemplo de uso
if __name__ == "__main__":
    start_time = time.time()
    lats = generate_decimal_range('40.620000', '40.670000', '0.000250')
    lons = generate_decimal_range('-4.718000', '-4.643000', '0.000250')
    num_image = 0
    cont = 0
    for lat in lats:
        for lon in lons:
            num_image = num_image + 1
            elapsed_time = time.time() - start_time
            print(f"Inicializando... T = {elapsed_time:.4f} s")
    for lat in lats:
        for lon in lons:
            cont = cont + 1
            #Parámetros del mapa
            width = 900
            height = 900
            zoom = 19
            filename = 'mapa_' + str(lat) + '-' + str(lon) + '.png'
            
            # Crear mapa
            mapa = create_static_map(width, height)
            
            # Agregar marcador
            add_marker_to_map(mapa, (float(lon), float(lat)))
            # Renderizar y guardar
            render_and_save_map(mapa, zoom, filename)
            
            #marca de tiempo
            elapsed_time = time.time() - start_time
            
            print("Mapa creado: " + str(width) +"x"+ str(height) + "px. " +str(lat) + ", " + str(lon) + ". T=" + str(round(elapsed_time, 1)) + "s. " + str(cont) + "/" + str(num_image) + " imagenes generadas. " + str(round(calculate_percentage(cont, num_image), 1)) + "%. " )
            #random_timer()


