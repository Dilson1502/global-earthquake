import requests
import geopy.distance

def respuesta_api() -> dict:
    """llamar a la api de terremotos

    Returns:
        dict: un archivo json con todos los terremotos
    """
    api_url: str = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    response = requests.get(api_url)
    if response.status_code!=200:
        return None
    return response.json().get("features")
 
def filtrar_terremotos(terremotos:dict) -> dict:
    """funcion para filtrar la respuesta de la api, retorna únicamente título y coordenada

    Args:
        terremotos (dict): recibe todos los terremotos después de llamar a la api en formato json

    Returns:
        terremotos_dict: diccionario con la informacion filtrada (id, titulo y coordenada de cada terremoto)
    """
    terremotos_dict = {}
    for terremoto in terremotos:
        terremotos_dict[terremoto.get("id")] = {
            "titulo": terremoto.get("properties").get("title"),
            "coordenadas": (
                terremoto.get("geometry").get("coordinates")[1],
                terremoto.get("geometry").get("coordinates")[0],
            ),
        }

    return terremotos_dict

def leer_coordenadas_usuario() -> tuple:
    print(
        """"por favor ingresa latitud y logitud
        por ejemplo:
        user_lat = 40.730610
        user_lon = -73.935242
        """
    )
    while True:
        try:
            user_lat = float(input("Latitud: "))
            user_lon = float(input("Longitud: "))
        except ValueError as err:
            print("Tiene que ingresar un dat de tipo flotante, es decir, numeros decimales usando el punto como separador")
        else:
            return (user_lat,user_lon)


def hallar_terremotos_mas_cercanos(terremotos_dict:dict,coords_1:tuple) -> dict:
    distancias = {}
    for terremoto_id,terremoto in terremotos_dict.items():
        coords_2 = terremoto.get("coordenadas")
        distancia =  int(geopy.distance.geodesic(coords_1,coords_2).km)
        distancias[distancia] = terremoto_id

    distancias_ordenadas = sorted(distancias.items())[:10]
    terremotos_mas_cercanos = {id: distancia for distancia,id in distancias_ordenadas}
    return terremotos_mas_cercanos

def imprimir_terremotos(terremotos_mas_cercanos:dict, terremotos_dict:dict) -> str:
    for terremoto_id,terremoto_cercano in terremotos_mas_cercanos.items():
        titulo = terremotos_dict.get(terremoto_id).get("titulo")
        distancia = terremoto_cercano
        print(f"{titulo} || {distancia}")

def main() -> str:
    user_lat , user_lon = leer_coordenadas_usuario()
    terremotos =  respuesta_api()
    terremotos_filtrados = filtrar_terremotos(terremotos)
    terremotos_cercanos = hallar_terremotos_mas_cercanos(terremotos_filtrados,(user_lat , user_lon))
    imprimir_terremotos(terremotos_cercanos,terremotos_filtrados)

if __name__=='__main__':
    main()

    



