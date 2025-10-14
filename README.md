# Evaluacion-2
=================================================
  PROYECTO: PLANIFICADOR DE RUTAS AVANZADO
=================================================
Asignatura: Telepresencia y Entornos Innovadores de Colaboración Humana

== DESCRIPCIÓN ==

Este es un script de Python que utiliza la API de Graphhopper para calcular rutas de viaje. El programa solicita al usuario un punto de partida y un destino, permite seleccionar el medio de transporte (auto, bicicleta o a pie) y devuelve la distancia total, la duración estimada del viaje y las instrucciones detalladas paso a paso en español.

== REQUISITOS ==

- Python 3.x
- Librería 'requests' de Python.

Para instalar la librería 'requests', ejecute el siguiente comando en su terminal:
pip install requests

== CONFIGURACIÓN OBLIGATORIA ==

Antes de ejecutar el script, es fundamental configurar su propia API Key de Graphhopper.

1.  Abra el archivo del script con un editor de texto.
2.  Busque la siguiente línea:
    API_KEY = "esta en la pagina"
3.  Reemplace el valor entre comillas por su propia API Key válida.
4.  Guarde el archivo.

**Nota:** Puede obtener una API Key gratuita registrándose en el sitio web de Graphhopper. Sin una clave válida, el script no funcionará.

== INSTRUCCIONES DE EJECUCIÓN ==

1.  Abra una terminal o línea de comandos.
2.  Navegue a la carpeta donde guardó el archivo del script.
3.  Ejecute el script con el siguiente comando (reemplace 'nombre_del_script.py' con el nombre real de su archivo):
    python3 nombre_del_script.py

4.  Siga las instrucciones que aparecen en pantalla:
    - Ingrese el punto de partida (ej: Plaza de Armas, Santiago, Chile).
    - Ingrese el punto de destino (ej: Costanera Center, Providencia, Chile).
    - Seleccione el número correspondiente al medio de transporte que desea usar.
    - Para salir del programa, puede escribir 's' o 'salir' cuando se le pida el punto de partida o el destino.
