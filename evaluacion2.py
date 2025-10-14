import requests
import urllib.parse

# --- URL y llave de la API de Graphhopper ---
route_url = "https://graphhopper.com/api/1/route?"
key = "b23c8ce2-0bdd-4dbb-b2c0-9d8d6d0b957b" # Ojo, esta es una llave de ejemplo, idealmente usa la tuya.

def geocoding(location, key):
  """
  Función para obtener las coordenadas (latitud, longitud) de una ubicación.
  """
  while not location.strip():
    location = input("Por favor, ingresa una ubicación válida: ")

  geocode_url = "https://graphhopper.com/api/1/geocode?"
  url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

  try:
    respuesta = requests.get(url)
    respuesta.raise_for_status() # Lanza un error si la respuesta no es 2xx
    json_data = respuesta.json()

    if json_data.get("hits"):
      hit = json_data["hits"][0]
      lat = hit["point"]["lat"]
      lng = hit["point"]["lng"]
      nombre = hit.get("name", "Sin nombre")
      pais = hit.get("country", "")
      estado = hit.get("state", "")

      # Formatea el nombre completo de la ubicación
      partes_loc = [nombre, estado, pais]
      nueva_loc = ", ".join(filter(None, partes_loc))

      print(f"URL de Geocodificación para '{nueva_loc}':\n{url}")
      return respuesta.status_code, lat, lng, nueva_loc
    else:
      print(f"No se encontraron resultados para '{location}'.")
      return respuesta.status_code, None, None, location

  except requests.exceptions.RequestException as e:
    print(f"Error de conexión con la API de Geocodificación: {e}")
    return None, None, None, location


def traducir_instruccion(texto_instruccion):
  """
  Traduce las instrucciones de navegación de inglés a español.
  Se pueden añadir más traducciones si es necesario.
  """
  traducciones = {
      "Turn left": "Gira a la izquierda",
      "Turn right": "Gira a la derecha",
      "Continue": "Continúa",
      "Head": "Dirígete",
      "Destination": "Destino",
      "roundabout": "rotonda",
      "onto": "hacia",
      "street": "calle",
      "road": "camino",
      "arrive": "llegar",
      # Puedes seguir agregando más traducciones aquí
  }

  for en, es in traducciones.items():
    # Usamos .lower() para que la traducción no sea sensible a mayúsculas/minúsculas
    texto_instruccion = texto_instruccion.replace(en, es).replace(en.lower(), es)
  
  return texto_instruccion.capitalize() # Ponemos la primera letra en mayúscula

# --- Inicio del programa principal ---
print("---------------------------------------------")
print("Perfiles de vehículo disponibles:")
print("---------------------------------------------")
print("auto, bicicleta, a pie")
print("---------------------------------------------")

perfiles = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}

while True:
  vehiculo_input = input("Ingresa un perfil de vehículo (o 's' para salir): ").lower().strip()
  if vehiculo_input in ["s", "salir"]:
    print("¡Chao, nos vemos!")
    break

  vehiculo = perfiles.get(vehiculo_input)
  if not vehiculo:
    vehiculo = "car" # Valor por defecto
    print("Perfil no válido. Se usará 'auto' por defecto.")

  loc1 = input("Ubicación de inicio (o 's' para salir): ").strip()
  if loc1.lower() in ["s", "salir"]:
    print("¡Chao, nos vemos!")
    break
  
  status_orig, lat_orig, lng_orig, nom_orig = geocoding(loc1, key)
  if status_orig != 200:
    print("--- No se pudo encontrar la ubicación de inicio. Inténtalo de nuevo. ---")
    continue

  loc2 = input("Destino (o 's' para salir): ").strip()
  if loc2.lower() in ["s", "salir"]:
    print("¡Chao, nos vemos!")
    break

  status_dest, lat_dest, lng_dest, nom_dest = geocoding(loc2, key)
  if status_dest != 200:
    print("--- No se pudo encontrar el destino. Inténtalo de nuevo. ---")
    continue

  print("-------------------------------------------------")

  # --- Construcción de la URL para la API de rutas ---
  op = f"&point={lat_orig},{lng_orig}"
  dp = f"&point={lat_dest},{lng_dest}"
  params_ruta = {
      "key": key,
      "vehicle": vehiculo,
      "locale": "es", # Pedimos instrucciones en español si es posible
      "instructions": "true",
      "calc_points": "true",
      "points_encoded": "false" # Para facilitar la lectura de los datos
  }
  paths_url = route_url + urllib.parse.urlencode(params_ruta) + op + dp

  try:
    response = requests.get(paths_url)
    response.raise_for_status()
    paths_data = response.json()

    print(f"Estado de la API de Rutas: {response.status_code}")
    print(f"URL de la API de Rutas:\n{paths_url}")
    print("-------------------------------------------------")
    print(f"Indicaciones de viaje de '{nom_orig}' a '{nom_dest}' en {vehiculo_input}")
    print("-------------------------------------------------")

    if "paths" in paths_data:
      path = paths_data["paths"][0]
      distancia_km = path["distance"] / 1000
      distancia_millas = distancia_km / 1.60934

      tiempo_ms = path["time"]
      hr = int(tiempo_ms / 3600000)
      minutos = int((tiempo_ms % 3600000) / 60000)
      seg = int((tiempo_ms % 60000) / 1000)

      print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
      print(f"Duración del viaje: {hr:02d}:{minutos:02d}:{seg:02d}")
      print("-------------------------------------------------")
      print("Instrucciones paso a paso:")

      instrucciones = path.get("instructions", [])
      if instrucciones:
        for i, instruccion in enumerate(instrucciones):
          texto = instruccion.get("text", "")
          texto_es = traducir_instruccion(texto)
          dist_km = instruccion.get("distance", 0) / 1000
          dist_millas = dist_km / 1.60934
          print(f"{i+1}. {texto_es} ({dist_km:.2f} km)")
          print("---")
      else:
        print("No se encontraron instrucciones para esta ruta.")
      print("-------------------------------------------------")
    else:
      print("Error al obtener la ruta.")
      print(f"Mensaje: {paths_data.get('message', 'Sin mensaje')}")
      print("-------------------------------------------------")

  except requests.exceptions.RequestException as e:
    print(f"Error de conexión con la API de Rutas: {e}")
    print("-------------------------------------------------")
