"""Extracts destination names from json/airports.json
and creates python file with code-to-name dictionary.

https://support.travelpayouts.com/hc/ru/articles/203956163#11

json format examples:
{
    "time_zone":"America/Lima",
    "name":"Андауайлас",
    "flightable":true,
    "coordinates":{
        "lon":-73.355835,"lat":-13.716667
    },
    "code":"ANS",
    "name_translations":{
        "en":"Andahuaylas"},
    "country_code":"PE",
    "city_code":"ANS"
}

{
    "time_zone":"Pacific/Port_Moresby",
    "name":"Кикори",
    "coordinates":{
        "lon":144.26666,
        "lat":-7.483333},
    "code":"KRI",
    "cases":{
        "vi":"в Кикори",
        "tv":"Кикори",
        "ro":"Кикори",
        "pr":"Кикори",
        "da":"Кикори"},
    "name_translations":{
        "en":"Kikori"},
    "country_code":"PG"
}
"""

import json


def create_code_to_name_dict(source_file):
    """Creates code-to-name dictionary from airports.json file
    in format {'code': ('russian_name', 'english_name')}
    """

    with open(source_file, 'r', encoding='utf-8') as json_file:
        entries = json.loads(json_file.read())
        result_dict = {}

        for entry in entries:
            result_dict[entry['code']] = (entry['name'], entry['name_translations']['en'])

        return result_dict


def write_dict_to_file(filename, dictionary):
    """Creates a file and writes given dictionary to the file."""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('CODE_TO_NAME = ')
        f.write(str(dictionary))


if __name__ == "__main__":
    dictionary = create_code_to_name_dict('json/cities.json')
    write_dict_to_file('iata_converters.py', dictionary)
