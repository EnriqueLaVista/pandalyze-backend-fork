from flask import Blueprint
import folium
import pandas as pd

map_bp = Blueprint("map_bp", __name__)

def get_color(genus):
    if genus == 'Puma': return 'blue'
    if genus == 'Leopardus': return 'green'
    return 'red'

def generate_map(dataframe, lat_col, long_col, title_col):
    """
    Crea un mapa base (lienzo) y añade marcadores para cada fila del DataFrame.
    """
    required_cols = [lat_col, long_col, title_col, 'genus']
    for col in required_cols:
        if col not in dataframe.columns:
            columnas_disponibles = ", ".join(dataframe.columns)
            raise KeyError(f"La columna '{col}' no se encuentra en el DataFrame. Las columnas disponibles son: {columnas_disponibles}")

    # Coordenadas fijas para centrar el mapa en Argentina.
    map_center = [-38.416097, -63.616672]
    folium_map = folium.Map(location=map_center, zoom_start=4)

    # Iteramos sobre cada fila del CSV (cada avistamiento de felino)
    for _, row in dataframe.iterrows():
        try:
            marker_color = get_color(row['genus'])
            
            # Usamos los nombres de columna (lat_col, long_col) para obtener
            # las coordenadas de cada fila y colocar un marcador.
            folium.Marker(
                location=[float(row[lat_col]), float(row[long_col])],
                popup=str(row[title_col]),
                tooltip=str(row[title_col]),
                icon=folium.Icon(color=marker_color, icon="paw", prefix="fa")
            ).add_to(folium_map)
        except (ValueError, TypeError):
            continue
    
    return folium_map

