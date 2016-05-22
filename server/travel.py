import countries
import users
import logging


class Error(Exception):
    pass


class Manager(object):

    SessionId = 0;
    UsernameForSessionId = {}
    TravelCountries = {
    }

    def __init__(self):
        users.load_users()
        countries.load_countries()

    def login(self, username, password):
        logging.info("Loggin request for %s", username)
        user = users.get_user_for_credentials(username, password)
        if user is None:
            raise Error("Invalid username or password")
        Manager.SessionId += 1
        sessionId = Manager.SessionId
        Manager.UsernameForSessionId[sessionId] = username

        logging.info("Loggin request for %s - name %s, sessionId %s",
                username, user, sessionId)

        return sessionId, user

    def get_cities_for_country(self, sessionId, country):
        logging.info("[%s] Request for %s", sessionId, country)
        self._username_for_sessionId(sessionId)

        cities = countries.get_cities_for_country(country)
        logging.info("[%s] Country: %s, cities: %s",
                sessionId, country, ", ".join(cities))

        return cities

    def add_country(self, sessionId, country, cities):
        logging.info("[%s] Request for %s, cities %s",
                sessionId, country, ", ".join(cities))
        self._username_for_sessionId(sessionId)
        return countries.add_country(country, cities)

    def add_city_for_country(self, sessionId, country, city):
        logging.info("[%s] Request for %s, city %s",
                sessionId, country, city)
        self._username_for_sessionId(sessionId)
        return countries.add_city_for_country(country, city)

    def _username_for_sessionId(self, sessionId):
        """Check that the user is logged in."""
        try:
            return Manager.UsernameForSessionId[sessionId]
        except KeyError:
            raise Error("Invalid session Id")
