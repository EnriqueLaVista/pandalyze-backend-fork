from flask import Blueprint
import folium
import pandas as pd

map_bp = Blueprint("map_bp", __name__)

def generate_dynamic_palette(dataframe, category_col):
    """
    Crea una paleta de colores e íconos únicos para cada categoría en una columna.
    """
    if category_col not in dataframe.columns:
        return {}

    categories = dataframe[category_col].unique()
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'lightgray', 'black']
    icons = ['info-sign']
    
    palette = {}
    for i, category in enumerate(categories):
        color = colors[i % len(colors)]
        icon = icons[i % len(icons)]
        palette[category] = {'color': color, 'icon': icon}
        
    return palette

def generate_map(dataframe, lat_col, long_col, title_col):
    """
    Crea un mapa Folium con colores dinámicos basados en la columna del título.
    """
    required_cols = [lat_col, long_col, title_col]
    for col in required_cols:
        if col not in dataframe.columns:
            columnas_disponibles = ", ".join(dataframe.columns)
            raise KeyError(f"La columna '{col}' no se encuentra en el DataFrame. Las columnas disponibles son: {columnas_disponibles}")

    palette = generate_dynamic_palette(dataframe, title_col)

    tiles = "https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png"
    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>'
    )
    
    map_center = [-38.416097, -63.616672]
    folium_map = folium.Map(
        location=map_center,
        zoom_start=4,
        tiles=tiles,  
        attr=attr    
    )

    for _, row in dataframe.iterrows():
        try:
            category_value = row[title_col]
            marker_style = palette.get(category_value, {'color': 'gray', 'icon': 'question-sign'})

            folium.Marker(
                location=[float(row[lat_col]), float(row[long_col])],
                popup=f"<strong>{category_value}</strong>",
                tooltip=category_value,
                icon=folium.Icon(color=marker_style['color'], icon=marker_style['icon'], prefix='glyphicon')
            ).add_to(folium_map)
        except (ValueError, TypeError):
            continue
    
    return folium_map