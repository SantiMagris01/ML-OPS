from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI()

df = pd.read_csv("movies_modificado.csv")

@app.get('/')
def read_root():
    return {'message' : 'API para consultar datos de Peliculas'}

@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma: str):
    df_filtrado = df[df['original_language'] == idioma]
    cantidad_pelicualas = len(df_filtrado)
    return {'Idioma' : idioma, 'Cantidad de peliculas' : cantidad_pelicualas}


@app.get('/peliculas_duracion/{pelicula}')

def peliculas_duracion(pelicula: str):
    pelicula_filtrada = df[df['title'] == pelicula]
    
    if not pelicula_filtrada.empty:
        duracion = pelicula_filtrada['runtime'].values[0]
        anio = pelicula_filtrada['release_year'].values[0]

        duracion = int(duracion) if not np.isnan(duracion) else None
        anio = int(anio) if not np.isnan(anio) else None

        respuesta = {
            'pelicula': pelicula,
            'duracion': duracion,
            'anio': anio
        }
    else:
        respuesta = {
            'pelicula': pelicula,
            'duracion': None,
            'anio': None
        }

    return respuesta


@app.get('/franquicia/{franquicia}')
def franquicia(franquicia : str):
    franquicica_filtrada = df[df['collection_name'] == franquicia]
    cantidad = len(franquicica_filtrada)
    ganancia_total = franquicica_filtrada['revenue'].sum()
    ganacia_promedio = ganancia_total/cantidad

    return {'Franquicia' : franquicia, 'Cantidad' : cantidad, 'Ganancia Total' : ganancia_total, 'Ganancia Promedio' : ganacia_promedio}




@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    
    pais_filtrado = df[df['production_countries_names'].apply(lambda x: pais in x)]
    cantidad = len(pais_filtrado)

    return {'Pais' : pais, 'Cantidad de Peliculas' : cantidad}


@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora : str):
    productora_filtrada = df[df['production_companies_names'].apply(lambda x: productora in x)]
    cantidad = len(productora_filtrada)
    revenue = productora_filtrada['revenue'].sum()

    respuesta = {
        'productora' : productora,
        'cantidad' : cantidad,
        'revenue' : revenue
    }

    return respuesta


@app.get('/get_director/{director}')
def get_director(director:str):
    director_filtrado = df[df['director_name'] == director]
    retorno_total_director = director_filtrado['return'].sum()
    peliculas = []

    for index, row in director_filtrado.iterrows():
        pelicula = {
            'nombre' : row['title'],
            'fecha de lanzamiento' : row['release_date'],
            'retorno individual' : row['return'],
            'costo': row['budget'],
            'ganancia': row['revenue']
        }
        peliculas.append(pelicula)
    return {'director' : director, 'Retorno total del director' : retorno_total_director}, peliculas
