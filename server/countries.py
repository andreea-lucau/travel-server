_countries = {}


class Error(Exception):
    pass


def load_countries():
    global _countries
    _countries = {
            "Ireland": set(["Dublin", "Cork", "Galway", "Sligo",]),
            "Romania": set(["Bucharest", "Cluj", "Iasi", "Suceava"]),
    }


def get_cities_for_country(country):
    return list(_countries.get(country, []))


def add_country(country, cities):
    if country in _countries:
        raise Error("Country already exists")

    _countries[country] = set(cities)
    return True

def add_city_for_country(country, city):
    if country not in _countries:
        _countries[country] = set()
    _countries[country].add(city)

    return True
