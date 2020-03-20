import sys
import requests


def get_coor(address):
    geocoder_request = f"""http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"""
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = \
            json_response["response"]["GeoObjectCollection"]["featureMember"][
                0][
                "GeoObject"]
        return ','.join(toponym["Point"]["pos"].split())
    return False


def create_image(coors):
    response = None
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coors}&spn=0.002,0.002&l=sat"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return