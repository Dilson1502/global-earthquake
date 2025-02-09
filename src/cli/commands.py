def leer_coordenadas_usuario() -> tuple:
    print(
        """"Enter latitud and longitude, with dots instead of commas,
        as the example:
        user_lat = 40.730610
        user_lon = -73.935242
        """
    )
    while True:
        try:
            user_lat = float(input("Latitud: "))
            user_lon = float(input("Longitud: "))
        except ValueError as err:
            print(f"""{err}: You must enter a float, decimal values with dots instead of commas.""")
        else:
            return (user_lat, user_lon)
        
if __name__ == "__main__":
    """Drive program."""
    user_lat, user_long = leer_coordenadas_usuario()
